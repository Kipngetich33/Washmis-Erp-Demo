// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Consumption Adjustment Capture', {
	refresh: function(frm) {

	}
});


frappe.ui.form.on("Consumption Adjustment Capture", "billing_zone", function(frm){ 

	frappe.call({
				method: "frappe.client.get_list",
				args: 	{
						 doctype: "Territory",
									 filters: {
				'parent_territory':["=", frm.doc.billing_zone]},
	
	},
	
				callback: function(r) {
	cur_frm.clear_table("table_2"); 
	cur_frm.refresh_fields();
	 $.each(r.message || [], function(i, v)
	 {	
	
	cur_frm.grids[0].grid.add_new_row(null,null,false);
	  //  cur_frm.refresh();
		var newrow = cur_frm.grids[0].grid.grid_rows[cur_frm.grids[0].grid.grid_rows.length - 1].doc;
	newrow.route=v.name
	cur_frm.refresh();
	}
	)						
	
				}
			});
	
	
	
	var child = cur_frm.add_child("table_2"); 
	child.doctype= "Reading Book Details"
	child.name= "New Reading Book Details 1"
	frappe.call({
		"method": "frappe.client.get_list",
		args: {
			doctype:"Territory",
			 filters: {
				'parent_territory':["=", frm.doc.billing_zone]},
				},
				callback: function (data) {
	
		$.each(frm.doc.table_2 || [], function(i, v) {
		// frappe.model.set_value(v.doctype, v.name, "route", data.message[i].name)
	//frm.refresh_field('table_2');
				})
			}
			
		});
		});
	
	
	frappe.ui.form.on("Consumption Adjustment Capture", "process_draft_sales_invoice", function(frm) {
	
	frappe.set_route("Form", "Sales Invoice","New Sales Invoice 1")
	
	}
	);
	
	frappe.ui.form.on("Consumption Adjustment Capture", "adjust_consumption", function(frm) {
	frappe.set_route("List", "Capture Readings","List")
	}
	);
	