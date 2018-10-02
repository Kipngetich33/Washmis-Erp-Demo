// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Survey Data', {
	refresh: function(frm) {
		

	}
});

//function that sets the customer name read_only on save
// frappe.ui.form.on("Survey Data", "refresh", function(frm) { 
// 	// use the __islocal value of doc, to check if the doc is saved or not 
// 	frm.set_df_property("customer_name", "read_only", frm.doc.__islocal ? 0 : 1); 
// });

// function that returns to task on save 
frappe.ui.form.on("Survey Data", { after_save: function(frm){
	console.log("returning")
	frappe.route_options = {"Priority":"High"}
	frappe.set_route("Form", "Task","TASK-2018-00030")
}});

