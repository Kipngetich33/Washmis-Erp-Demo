// Copyright (c) 2019, Paul Karugu and contributors
// For license information, please see license.txt


// The section below contains custom scripts for Item
// ================================================================================================
/* This section contains code from the general functions section
which are called is the form triggered functions section*/

// global variables
var required_fields = {customer: ["billing_period"],
						billing_period:["new_readings"],
						new_reading:["adjust_readings"],
						all:["billing_period","new_readings","adjust_readings"]
					}

function hide_unhide_on_refresh(frm,required_fields){
	// hide all fields
	hide_unhide_fields(frm,required_fields["all"],false)
	if(frm.doc.customer){
		// hide_unhide_fields(frm,required_fields["all"],false)
		hide_unhide_fields(frm,required_fields["customer"],true)
	}

	if(frm.doc.billing_period){
		// hide_unhide_fields(frm,required_fields["all"],false)
		hide_unhide_fields(frm,required_fields["billing_period"],true)
	}

	if(frm.doc.new_readings){
		// hide_unhide_fields(frm,required_fields["all"],false)
		hide_unhide_fields(frm,required_fields["new_readings"],true)
	}
	
}


/*function that hides fields ,called on refresh*/
function hide_unhide_fields(frm,list_of_fields,hide_or_unhide){
	for(var i = 0; i < list_of_fields.length; i++){
		frm.toggle_display(list_of_fields[i],hide_or_unhide)
	}
}

// function that fills territory fields based on a customer
function fill_territory_fields(customer_name,frm){
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			'doctype': 'Customer',
			'filters': {'name': customer_name},
			'fieldname': ["area","zone","route","previous_reading"]
		},
		callback: function(r) {
			if (!r.exc) {
				// fill territory fields
				frm.set_value("area", r.message.area)
				frm.set_value("zone", r.message.zone)
				frm.set_value("route", r.message.route)
				frm.set_value("customer_previous_readings", r.message.previous_reading)
			}
		}
	});
}

// function that fills billing period related fields
function fill_billing_period_related_fields(customer_name,billing_period,frm){
	
	// get related reading sheet
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			parent:"Reading Sheet",
			doctype: 'Meter Reading Sheet',
			filters: {'parenttype':"Reading Sheet",'customer_name':customer_name,
				"billing_period":billing_period
			},
			'fieldname': ["parent","current_manual_readings"]
		},
		callback: function(r) {
			if (!r.exc) {
				// fill billing period related fields
				// fill territory fields
				frm.set_value("reading_sheet_to_amend", r.message.parent)
				frm.set_value("previous_reading_sheet_value", r.message.current_manual_readings)
			}
		}
	});

	// get related sales invoice
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			doctype: 'Sales Invoice',
			filters: {'type_of_invoice':"Bill",'customer_name':customer_name,
				"billing_period":billing_period
			},
			'fieldname': ["name","net_total"]
		},
		callback: function(r) {
			if (!r.exc) {
				// fill billing period related fields
				frm.set_value("sales_invoice_to_amend", r.message.name)
				frm.set_value("previous_invoice_amount", r.message.net_total)
			}
		}
	});
}


// function that fills new readings related fields
function new_readings_related_fields(customer_name,billing_period,frm){
	// set new customer and reading sheet values
	// frm.set_value("new_previous_customer_reading", frm.doc.new_readings)
	// frm.set_value("new_reading_sheet_value", frm.doc.new_readings)

	// calculat and set sales invoice value
	// frappe.call({
	// 	method: 'frappe.client.get_value',
	// 	args: {
	// 		'doctype': 'Sal',
	// 		'filters': {'name': customer_name},
	// 		'fieldname': ["area","zone","route","previous_reading"]
	// 	},
	// 	callback: function(r) {
	// 		if (!r.exc) {
	// 			// fill territory fields
	// 			frm.set_value("area", r.message.area)
	// 			frm.set_value("zone", r.message.zone)
	// 			frm.set_value("route", r.message.route)
	// 			frm.set_value("customer_previous_readings", r.message.previous_reading)
	// 		}
	// 	}
	// });
}

// * end of the general functions section
// =================================================================================================

/* refresh in order to hide/unhide the correct fields*/
frappe.ui.form.on("Meter Readings Adjustment","customer",function(frm){ 
	if(frm.doc.customer){
		// fill territory fields
		fill_territory_fields(frm.doc.customer,frm)
		frm.refresh()
	}
	else{
		// no customer was selected ( do nothing)
	}
	
})

/* refresh in order to hide/unhide the correct fields*/
frappe.ui.form.on("Meter Readings Adjustment","billing_period",function(frm){ 
	if(frm.doc.billing_period){
		// fill territory fields
		fill_billing_period_related_fields(frm.doc.customer,frm.doc.billing_period,frm)
		frm.refresh()
	}
	else{
		// no billing period was selected ( do nothing)
	}
})

/* refresh in order to hide/unhide the correct fields*/
frappe.ui.form.on("Meter Readings Adjustment","new_readings",function(frm){ 
	if(frm.doc.billing_period){
		// fill territory fields
		new_readings_related_fields(frm.doc.customer,frm.doc.billing_period,frm)
		frm.refresh()
	}
	else{
		// no billing period was selected ( do nothing)
	}
})

// function that initiates the reading sheet adjustmet process
frappe.ui.form.on("Meter Readings Adjustment", "adjust_readings", function(frm) {
	cur_frm.save();
})


// function that runs on refresh
frappe.ui.form.on("Meter Readings Adjustment", "refresh", function(frm) {
	console.log("Refreshing !")
	hide_unhide_on_refresh(frm,required_fields)
})