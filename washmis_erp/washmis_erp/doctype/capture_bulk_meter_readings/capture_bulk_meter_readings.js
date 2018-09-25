// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Capture Bulk Meter Readings', {
	refresh: function(frm) {

	}
});

// custom scripts below
frappe.ui.form.on("Capture Bulk Meter Readings", "process_non_revenue_water", function(frm) {
	frappe.route_options = {"dma": frm.doc.bulk_meter_name}
	frappe.set_route("Form", "Non Revenue Capture","New Non Revenue Capture 1")
	});
	
	frappe.ui.form.on("Capture Bulk Meter Readings", "capture_monthly_readings", function(frm) {
	var child = cur_frm.add_child("table_8");
	cur_frm.refresh_field("table_8")
	});
	frappe.ui.form.on("Bulk Meter Readings Details", "reading_date",function(frm,cdt, cdn){
	var cur_grid =frm.get_field("table_8").grid;
	var cur_doc = locals[cdt][cdn];
	var cur_row = cur_grid.get_row(cur_doc.name);
	cur_row.toggle_view();
	
	}
	);
	
	frappe.ui.form.on("Capture Bulk Meter Readings", "prepare_book", function(frm) {
	});
	
	frappe.ui.form.on("Capture Bulk Meter Readings", "receive_readings_from_loggers", function(frm) {
	//cur_frm.get_field("table_8").grid.set_multiple_add("table_8");
	});
	