// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt

// ================================================================================================
/* This section contains code from the general functions section
which are called is the form triggered functions section*/

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
				cur_frm.grids[0].grid.add_new_row(null,null,false);
				var newrow = cur_frm.grids[0].grid.grid_rows[cur_frm.grids[0].grid.grid_rows.length - 1].doc;
				newrow.system_no = v.system_no
			});

			cur_frm.doc.meter_reading_sheet.forEach(function(row){ 
				frappe.call({
					method: "frappe.client.get",
					args: {
						doctype: "Customer",
						filters: {"system_no":row.system_no}    
					},
					callback: function(r) {

						$.each(cur_frm.doc.meter_reading_sheet || [], function(i, v) {
							// customer details
							row.customer_name = r.message.customer_name
							row.account_no= r.message.accounts[0].account
							row.dma=r.message.dma	
							row.meter_number=r.message.meter_serial_no
							row.walk_no=r.message.walk_no	
							row.reading_date=cur_frm.doc.reading_date
							row.tel_no=r.message.tel_no
							row.balance_bf=r.message.outstanding_balances
							row.type_of_customer = r.message.customer_type

							// to be set on form
							row.bill_category="Periodical"
							row.type_of_bill="Actual"
							row.reading_code="Normal Reading"
							row.comments="Normal"
							row.billing_period=cur_frm.doc.billing_period
							row.meter_reader=cur_frm.doc.meter_reader
							cur_frm.refresh_field('meter_reading_sheet');

							// the value from the code below should be moved to a different doctype
							row.previous_reading=r.message.initial_reading
						})
					}
				})
			});
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


/* function that generates sales when the finish capture button is clicked*/
function finish_capture(){
	frappe.ui.form.on("Meter Reading Capture", "finish_capture", function(frm) {
		cur_frm.save();/* save the form first*/
		
		
		if(cur_frm.doc.meter_reading_sheet.length>0){
			var x=0
			cur_frm.doc.meter_reading_sheet.forEach(function(row){ 
				frappe.route_options = {
					"previous_reading":row.previous_manual_reading,
					"current_reading": row.current_manual_readings,
					"consumption":row.manual_consumption,
					"type_of_bill":row.type_of_bill,
					"billing_period":cur_frm.doc.billing_period,
					"type_of_invoice":"bill",
					"customer":row.customer_name,
					"tariff_category":row.type_of_customer,
					"from_finish_capture":"true"
				}
				frappe.set_route("Form", "Sales Invoice","New Sales Invoice 1")
				x=1
			})
		}
		else{
			alert_message("No Active Customer for "+ cur_frm.doc.route_and_billing_period)
		}
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
frappe.ui.form.on("Meter Reading Capture", "refresh", function() {
	
	// make field route_and_billing_period readonly
	make_field_readonly("route_and_billing_period")
	filter_territoty()/*filter territory by route*/
	set_manual_consumption() /* sets the value of the manual consumption*/ 
	set_bill_type()/* sets type of bill as estimated/actual*/
	finish_capture() /* function that creates sales invoice when finish capture button is clicked*/
	
});


/* function that sets the billing period and get customer details when 
billling period is filled*/
frappe.ui.form.on("Meter Reading Capture", "billing_period", function(){ 
	if (cur_frm.doc.route && cur_frm.doc.billing_period){
		cur_frm.set_value("route_and_billing_period",cur_frm.doc.route +' '+ cur_frm.doc.billing_period)
		console.log("succefully askin for customers")
		
		// add customers in that route to the meter reading sheet
		// get_customers_by_route()
	}
});

// function that sets the route and get customer details when route if filled
frappe.ui.form.on("Meter Reading Capture", "route", function(){ 
	if (cur_frm.doc.route && cur_frm.doc.billing_period){
		cur_frm.doc.route_and_billing_period=cur_frm.doc.route +' '+ cur_frm.doc.billing_period
		console.log("succefully askin for customers")

		// add customers in that route to the meter reading sheet
		// get_customers_by_route()
	}
});
/* end of the form triggered functions section*/
// =================================================================================================
