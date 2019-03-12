// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt

// ================================================================================================
/* This section contains code from the general functions section
which are called is the form triggered functions section*/


// function that allows users to confirm from an alert
function confirm_redirect_to_reading_sheet(){
	frappe.confirm(
		"No Reading Sheet Matches Selected Route and Billing Period, Would You Like To Create a new Reading Sheet?",
		function(){
			// redirect to reading sheet
			frappe.route_options = {
				"redirected_from_meter_reading_capture":"True",
				"billing_period":cur_frm.doc.billing_period,
				"route":cur_frm.doc.route,
				
			}
			frappe.set_route("Form", "Reading Sheet","New Reading Sheet 1")
		}
	)
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


// functions that gets the readings of customers from
// reading sheet
function get_customer_readings(route,billing_period){
	// get customers for route and billing period
	frappe.call({
		method: "frappe.client.get_list",
		args: 	{
				doctype: "Reading Sheet",
				filters: {
					route:route,
					billing_period:billing_period
				},
		fields:["*"]
		},
		callback: function(response) {	
			if(response.message.length == 0){
				alert_message("No reading Sheet Exists for selected Route and Billing Periond")
			}
			else if(response.message.length > 0){
				// call a function to get customers in reading sheet
				
				retrive_customer_details(response.message)
		
					
			}
			else{
				alert_message("Something went wrong while retrieving Reading Sheets")
			}


			
		}	
	});
}


function retrive_customer_details(current_reading_sheet){
	console.log("name")
	frappe.call({
		method: "frappe.client.get_list",
		args: 	{
				parent:"Reading Sheet",
				doctype: "Meter Reading Sheet",
				filters: {
					parent:current_reading_sheet[0]["name"],
					billing_period:current_reading_sheet[0]["billing_period"]
				},
			fields:["*"]
		},
		callback: function(response) {

			if(response.message.length == 0){
				alert_message("No customers exists for selected Route and biling period")
			}
			else if(response.message.length > 0){
				cur_frm.clear_table("meter_reading_sheet"); 
				cur_frm.refresh_fields();
				$.each(response.message || [], function(i, v){
					// create rows 
					cur_frm.grids[0].grid.add_new_row(null,null,false);
					var newrow = cur_frm.grids[0].grid.grid_rows[cur_frm.grids[0].grid.grid_rows.length - 1].doc;
					
					// // set values from customer
					newrow.customer_name = v.customer_name
					newrow.system_no = v.system_no
					newrow.account_no= v.account_no
					newrow.dma=v.dma	
					newrow.meter_number=v.meter_serial_no
					newrow.walk_no=v.walk_no	
					newrow.reading_date=v.reading_date
					newrow.tel_no=v.tel_no
					newrow.type_of_customer = v.type_of_customer
					newrow.bill_category= v.bill_category
					newrow.type_of_bill= v.type_of_bill
					newrow.reading_code=v.reading_code
					newrow.comments=v.comments
					newrow.reading_sheet_no = v.reading_sheet_no
					newrow.billing_period=v.billing_period
					newrow.route=cur_frm.doc.route
					newrow.meter_reader=v.meter_reader
					newrow.previous_manual_reading=v.previous_manual_reading
					newrow.current_manual_readings = v.current_manual_readings
					newrow.manual_consumption = v.manual_consumption
					cur_frm.refresh_fields();
				})
				
			}
			else{
				alert_message("Something went wrong while retriving customer details from reading sheet")
			}
		
		}
	})
}


/* end of the general functions section
// =================================================================================================
/* This section  contains functions that are triggered by the form action refresh or
reload to perform various action*/

/* function that generates sales when the finish capture button is clicked*/
function finish_capture(){
	frappe.ui.form.on("Meter Reading Capture", "finish_capture", function(frm) {
		cur_frm.save();/* save the form first*/
		// alert_message("This functionality is under development")
		// alert_message("Document Saved")
		
		// the code below is used to set root options in order to loop through sales 
		// invoices
		/*
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
		*/
	});
}

/* function that is called when send to mobile button is clicked*/
frappe.ui.form.on("Meter Reading Capture", "send_to_a_mobile_device", function(frm) {
	console.log("this functionality is not yet fully developed")
});

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
	finish_capture() /* function that creates sales invoice when finish capture button is clicked*/
	
});


/* function that sets the billing period and get customer details when 
billling period is filled*/
frappe.ui.form.on("Meter Reading Capture", "billing_period", function(){ 
	if (cur_frm.doc.route && cur_frm.doc.billing_period){
		cur_frm.set_value("route_and_billing_period",cur_frm.doc.route +' '+ cur_frm.doc.billing_period)
		// get customer details and readings from reading sheet
		get_customer_readings(cur_frm.doc.route,cur_frm.doc.billing_period)
	}
});

// function that sets the route and get customer details when route if filled
frappe.ui.form.on("Meter Reading Capture", "route", function(){ 
	if (cur_frm.doc.route && cur_frm.doc.billing_period){
		cur_frm.doc.route_and_billing_period=cur_frm.doc.route +' '+ cur_frm.doc.billing_period
		// get customer details and readings from reading sheet
		get_customer_readings(cur_frm.doc.route,cur_frm.doc.billing_period)
	}
});
/* end of the form triggered functions section*/
// =================================================================================================
