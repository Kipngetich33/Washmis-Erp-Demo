// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt


/*function that acts when the readings field under meter reading sheet is
filled*/
frappe.ui.form.on("Meter Reading Sheet", "readings", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if(d.readings){
		if(d.estimated_consumption){
			// do nothing for now 
		}
		else{
			frappe.model.set_value(cdt, cdn, "consumption", (d.readings - d.previous_reading));
		}
	}
});


/*function that acts when the estimated consumption field under meter reading sheet is
filled*/
frappe.ui.form.on("Meter Reading Sheet", "estimated_consumption", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "consumption", d.estimated_consumption);
	frappe.model.set_value(cdt, cdn, "readings", );
});


/* function that generates sales when the finish capture button is clicked*/
frappe.ui.form.on("Meter Reading Capture", "finish_capture", function(frm) {
	// saved the form 
	cur_frm.save();

	var x=0
	frm.doc.table_17.forEach(function(row){ 
		frappe.route_options = {"previous_reading":row.previous_reading,
								"current_reading":row.readings,"consumption":row.consumption,
								"type_of_bill":row.type_of_bill,
								"billing_period":frm.doc.billing_period,"type_of_invoice":"bill",
								"customer":row.customer_name
							}
		frappe.set_route("Form", "Sales Invoice","New Sales Invoice 1")
		x=1
	})

});

// current test section
/* function that generates sales when the export as excel sheet button is clicked*/
frappe.ui.form.on("Meter Reading Capture", "export_as_csv_file", function(frm) {
	frappe.route_options = {"reference_doctype":"Meter Reading Capture","file_type":"Excel"}
	frappe.set_route("Form", "Data Export","New Data Export 1");
	// frappe.model.set_value("reference_doctype", "Meter Reading Capture")
	// cur_frm.save();
});


frappe.ui.form.on("Meter Reading Sheet", "table_17", function(frm, cdt, cdn) {
	var z = locals[cdt][cdn];

	if(z.previous_reading && z.readings) {
		consumption = frappe.consumed_quantity.get_diff(z.readings, z.previous_reading);
		frappe.model.set_value(cdt, cdn, "consumption", consumption);
	}
});

/*function that sets the route_and_billing_period fields when a billing 
period is chosen*/
frappe.ui.form.on("Meter Reading Capture", "billing_period", function(frm){ 
	cur_frm.set_value("route_and_billing_period",frm.doc.route + frm.doc.billing_period)
});

/*function that sets the route_and_billing_period fields when a route is chosen*/
frappe.ui.form.on("Meter Reading Capture", "route", function(frm){ 
	frm.doc.route_and_billing_period=frm.doc.route + frm.doc.billing_period
	frappe.call({
				method: "frappe.client.get_list",
				args: 	{
						doctype: "Customer",
						filters: {
							'route':["=", cur_frm.doc.route]
						},
				},

				callback: function(r) {	
					cur_frm.clear_table("table_17"); 
					cur_frm.refresh_fields();
					$.each(r.message || [], function(i, v){	
						cur_frm.grids[0].grid.add_new_row(null,null,false);
						var newrow = cur_frm.grids[0].grid.grid_rows[cur_frm.grids[0].grid.grid_rows.length - 1].doc;
						newrow.customer_name=v.name
						var cust_naming=v.name
					});

					frm.doc.table_17.forEach(function(row){ 
						frappe.call({
							method: "frappe.client.get",
							args: {
								doctype: "Customer",
								filters: {"customer_name":row.customer_name}    
							},
							callback: function(r) {
								$.each(frm.doc.table_17 || [], function(i, v) {
									row.account_no=r.message.new_account_no
									row.dma=r.message.dma	
									row.meter_number=r.message.meter_serial_no
									row.previous_reading=r.message.initial_reading
									row.walk_no=r.message.walk_no	
									row.reading_date=frm.doc.reading_date
									row.tel_no=r.message.tel_no
									row.balance_bf=r.message.outstanding_balances
									row.bill_category="Periodical"
									row.type_of_bill="Actual"
									row.reading_code="Normal Reading"
									row.comments="Normal"
									row.billing_period=frm.doc.billing_period
									row.meter_reader=frm.doc.meter_reader
									frm.refresh_field('table_17');
								})
							}
						})
					});
				}
	});
});


//frappe.ui.form.on(“Meter Reading Capture”, “onload”, function(frm,cdt, cdn){
 //$(".grid-add-row").hide();

//});

//Expand first row
//frappe.ui.form.on("Meter Reading Sheet", "customer_name",function(frm,cdt, cdn){
//	    $(".btn-open-row").trigger('click');   
//	});

//Expand current row
//frappe.ui.form.on("Meter Reading Sheet", "customer_name", function(frm,cdt, cdn) {
//var cur_grid =frm.get_field("table_17").grid;
//var cur_doc = locals[cdt][cdn];
//var cur_row = cur_grid.get_row(cur_doc.name);
//cur_row.toggle_view();
//});


/*function that sets the route query fields */
frappe.ui.form.on("Meter Reading Capture", "refresh", function(frm) {
	
	// sets the value of the country/territory query field
	cur_frm.set_query("route", function() {
		return {
			"filters": {
				"type": "route"
			}
		}
	});
});


/*function that set type of bill as either actual or estimated*/
frappe.ui.form.on("Meter Reading Sheet", "readings", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "type_of_bill", "Actual");
});


/*function that set type of bill as either actual or estimated*/
frappe.ui.form.on("Meter Reading Sheet", "estimated_consumption", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "type_of_bill", "Estimated");
});
