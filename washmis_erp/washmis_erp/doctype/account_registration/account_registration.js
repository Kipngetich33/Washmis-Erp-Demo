// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Account Registration', {
	refresh: function(frm) {

	}
});


/* the code below is custom scripts*/
frappe.ui.form.on("Account Registration", "make_deposit_invoice", function(frm) {
	frappe.route_options = {"customer": frm.doc.customer_name,"type_of_invoice":"Deposit"}
	frappe.set_route("Form", "Sales Invoice","New Sales Invoice 1")
});


frappe.ui.form.on("Account Registration", "make_new_connection_fees_invoice", function(frm) {
	frappe.route_options = {"customer": frm.doc.customer_name,"type_of_invoice":"New Connection Fee"}
	frappe.set_route("Form", "Sales Invoice","New Sales Invoice 1")
});


frappe.ui.form.on("Account Registration", "new_account_no", function(frm){ 
	cur_frm.clear_table("accounts"); 
	cur_frm.grids[0].grid.add_new_row(null,null,false);
	var newrow = cur_frm.grids[0].grid.grid_rows[cur_frm.grids[0].grid.grid_rows.length - 1].doc;
	newrow.account=cur_frm.doc.new_account_no;
	cur_frm.refresh_field("accounts") 
});


frappe.ui.form.on("Account Registration", {
	onload: function (frm) {
	cur_frm.clear_table("accounts"); 
	cur_frm.grids[0].grid.add_new_row(null,null,false);
	var newrow = cur_frm.grids[0].grid.grid_rows[cur_frm.grids[0].grid.grid_rows.length - 1].doc;
newrow.account=cur_frm.doc.new_account_no;
cur_frm.refresh_field("accounts")
	},
});
	
