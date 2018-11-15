// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt

// ================================================================================================
/* This section contains code from the general functions section
which are called is the form triggered functions section*/


// function that sends the saved reading shee to meter reading capture
function send_to_meter_reading_capture(){
	// when the send to meter reading button is clicked
	frappe.ui.form.on("Reading Sheet", "send_to_meter_reading_capture", function() {
		cur_frm.save(); /* save the form first */
		// redirect to meter reading capture
		frappe.route_options = {
			"billing_period":cur_frm.doc.billing_period,
			"route":cur_frm.doc.route,
		}
		frappe.set_route("Form", "Meter Reading Capture","New Meter Reading Sheet 1")
	})
}


/* function that saves the form when the save reading sheet button is clicked*/
function save_reading_sheet(){
	frappe.ui.form.on("Reading Sheet", "save_reading_sheet", function() {
		cur_frm.save();
	})
}

// function set tracker number
function set_tracker_number(route,billing_period){
	frappe.call({
		method: "frappe.client.get_list",
		args: {
			doctype: "System Values",
			filters: {"target_document":"Reading Sheet","target_record":route},
			fields:["name","int_value","description"]
		},
		callback: function(response) {
			if(response.message.length){
				// add one to the existing system value for a new reading on route and 
				// billing period
				if(response.message[0].description == billing_period){
					cur_frm.set_value("tracker_number",response.message[0].int_value+1)
				}
				else{
					cur_frm.set_value("tracker_number",response.message[0].int_value+1)
				}
			}
			else{
				// if the system value does not exist set value to 0
				// set the value using get_last_reading_sheet.py on save
				cur_frm.set_value("tracker_number",1)
			}
		}
	})
}

// function that track sheet by saving new system values
function track_with_system_values(target_doctype,route,billing_period){
	frappe.call({
		"method": "frappe.client.set_value",
		"args": {
			"doctype": "System Values",
			"name": "target_document",
			"fieldname": "target_document",
			"value": "Route and Billing Period"
		}
	});
}


// function that makes the field passed as a parameter readonly
function make_field_readonly(given_field){
	cur_frm.set_df_property(given_field,"read_only", 1);
}


// function that alerts a message provided to it as parameter
function alert_message(message_to_print){
	msgprint(message_to_print)
}


// function that filter the route to be selected from territory
function filter_territoty(){
	cur_frm.set_query("route", function() {
		return {
			"filters": {
				"type_of_territory": "route"
			}
		}
	});
}

// function that get customer with customer number
function get_customer_with_no(system_no){
	frappe.call({
		method: "frappe.client.get",
		args: {
			doctype: "Customer",
			filters: {"system_no":system_no} 
		},
		callback: function(response) {
			// create rows
			cur_frm.grids[0].grid.add_new_row(null,null,false);
			var newrow = cur_frm.grids[0].grid.grid_rows[cur_frm.grids[0].grid.grid_rows.length - 1].doc;
			
			// set values from customer
			newrow.customer_name = response.message.customer_name
			newrow.system_no = response.message.system_no
			// check if accounts exists then set
			if(response.message.accounts.length>0){
				newrow.account_no= response.message.accounts[0].account
			}
			newrow.dma=response.message.dma	
			newrow.meter_number=response.message.meter_serial_no
			newrow.walk_no=response.message.walk_no	
			newrow.reading_date=cur_frm.doc.reading_date
			newrow.tel_no=response.message.tel_no
			newrow.balance_bf=response.message.outstanding_balances
			newrow.type_of_customer = response.message.customer_type
			newrow.bill_category="Periodical"
			newrow.type_of_bill="Actual"
			newrow.reading_code="Normal Reading"
			newrow.comments="Normal"
			newrow.reading_sheet_no = cur_frm.doc.tracker_number
			newrow.billing_period=cur_frm.doc.billing_period
			newrow.route=cur_frm.doc.route
			newrow.meter_reader=cur_frm.doc.meter_reader
			newrow.previous_manual_reading=response.message.previous_reading
		}
	})
}


// function that add customer in a given route and billing period
function get_customers_by_route(){
	// get customers from a specific route
	frappe.call({
		method: "frappe.client.get_list",
		args: 	{
				doctype: "Customer",
				filters: {
					route:cur_frm.doc.route,
					status:"Active"
				},
		fields:"system_no"
		},

		callback: function(r) {	
			cur_frm.clear_table("meter_reading_sheet"); 
			cur_frm.refresh_fields();
			$.each(r.message || [], function(i, v){	
				get_customer_with_no(v.system_no)
			});
			cur_frm.refresh_fields();
		}
	});
}


// function that calculates manual consumption
function set_manual_consumption(){
	frappe.ui.form.on("Meter Reading Sheet", "current_manual_readings", function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.current_manual_readings){
			if(d.estimated_consumption){
				// do nothing for now 
			}
			else{
				frappe.model.set_value(cdt, cdn, "manual_consumption", (d.current_manual_readings - d.previous_manual_reading));
			}
		}
	});
} 


/*function that set type of bill as either actual or estimated*/
function set_bill_type(){
	// acts when the current manual reading field  is clicked
	frappe.ui.form.on("Meter Reading Sheet", "current_manual_readings", function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "type_of_bill", "Actual");
	});

	// acts when the estimated_consumption field is clicked
	frappe.ui.form.on("Meter Reading Sheet", "estimated_consumption", function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "type_of_bill", "Estimated");
	});
}


/* end of the general functions section
// =================================================================================================
/* This section  contains functions that are triggered by the form action refresh or
reload to perform various action*/

/* function that generates sales when the export as excel sheet button is clicked*/
frappe.ui.form.on("Meter Reading Capture", "export_as_csv_file", function(frm) {
	frappe.route_options = {"reference_doctype":"Meter Reading Capture","file_type":"Excel"}
	frappe.set_route("Form", "Data Export","New Data Export 1");
	// frappe.model.set_value("reference_doctype", "Meter Reading Capture")
	// cur_frm.save();
});

/*this is the refresh function triggered by refreshing the form*/
// frappe.ui.form.on("Reading Sheet", "refresh", function() {
frappe.ui.form.on("Reading Sheet", "refresh",function(){

	// make field route_and_billing_period readonly
	make_field_readonly("route_and_billing_period")
	filter_territoty()/*filter territory by route*/
	set_manual_consumption() /* sets the value of the manual consumption*/ 
	set_bill_type()/* sets type of bill as estimated/actual*/
	save_reading_sheet() /* saves form when the save reading sheet button is clicked*/
	send_to_meter_reading_capture()/* function that set route options to meter reading capture*/
});


/*this is the before save function that saves the values to 
System Values doctype to track the records*/
frappe.ui.form.on("Reading Sheet", { after_save: function(){
	console.log("after save")
	// track_with_system_values("Reading Sheet",cur_frm.doc.route,cur_frm.doc.billing_period)
}});


// test section
// function that runs when the billing field is clicked
frappe.ui.form.on("Reading Sheet", "billing_period", function(){ 
	if (cur_frm.doc.route && cur_frm.doc.billing_period){
		console.log("inside billing function")
		cur_frm.set_value("route_and_billing_period",cur_frm.doc.route +' '+ cur_frm.doc.billing_period)
		// add customers in that route to the meter reading sheet
		get_customers_by_route()
		set_tracker_number(cur_frm.doc.route,cur_frm.doc.billing_period)
	}
});

// function that runs when the route field is clicked
// when the route field is clicked
frappe.ui.form.on("Reading Sheet", "route", function(){
	if (cur_frm.doc.route && cur_frm.doc.billing_period){

		// check if form has been redirected
		if(cur_frm.doc.redirect_from_meter_reading_capture == "True"){
			// do nothing
		}
		else{
			cur_frm.doc.route_and_billing_period=cur_frm.doc.route +' '+ cur_frm.doc.billing_period
			// add customers in that route to the meter reading sheet
			get_customers_by_route()
			set_tracker_number(cur_frm.doc.route,cur_frm.doc.billing_period)
		}
		console.log("inside route function")
		
	}
});
// end of test section

/* end of the form triggered functions section*/
// =================================================================================================