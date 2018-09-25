// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Non Revenue Capture', {
	refresh: function(frm) {

	}
});

function getMonth(monthStr){
    return new Date(monthStr+'-1-01').getMonth()+1
}

frappe.ui.form.on("Non Revenue Capture", "dma", function(frm){ 
	frm.set_value("dma_and_billing_period",frm.doc.dma + frm.doc.billing_period);
});
frappe.ui.form.on("Non Revenue Capture", "route_and_billing_period", function(frm){
var billed_consumption=0
var routeandperiod = frm.doc.route_and_billing_period;
frappe.call({
            "method": "frappe.client.get",
            args: {
                doctype: "Meter Reading Capture",
                name: routeandperiod
            },
            callback: function (data) {

frappe.model.with_doc("Meter Reading Capture",routeandperiod,  function() {
var tabletransfer = frappe.model.get_doc("Meter Reading Capture", routeandperiod)
        $.each(tabletransfer.table_17, function(index, row)
{
if (row.dma==frm.doc.dma){
billed_consumption = (billed_consumption * 1) + (row.consumption *1)
}
   });
frm.set_value("billed_water",billed_consumption);

   })
}
 });
});

frappe.ui.form.on("Non Revenue table", "reading", function(frm, cdt, cdn){
var row = locals[cdt][cdn];
var minreading=0;
var maxreading=0;
frm.doc.non_revenue_table.forEach(function(row){ 
if (row.date==frm.doc.billing_period_start_date){
minreading=row.reading
}
if (row.date==frm.doc.billing_period_end_date){
maxreading=row.reading
}
frm.set_value("water_supplied", (maxreading - minreading));
frm.set_value("nrw", (((frm.doc.water_supplied - frm.doc.billed_water)/frm.doc.water_supplied)*100));
});
});

frappe.ui.form.on("Non Revenue Capture", "billing_period", function(frm){ 
frm.set_value("dma_and_billing_period",frm.doc.dma + frm.doc.billing_period);
frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Billing Period",
				filters: {"Name":frm.doc.billing_period}    
			},
			callback: function(r) {
frm.set_value("billing_period_start_date",r.message.start_date_of_billing_period);
frm.set_value("billing_period_end_date",r.message.end_date_of_billing_period);
frappe.model.clear_table(frm.doc, "non_revenue_table");
var str = frm.doc.billing_period;
var n = str.length;
var n1 = str.indexOf(" ");
var maxvalues = str.substr(0, n1);
var cur_month=getMonth(maxvalues);
var date = new Date(), y = date.getFullYear(), m = cur_month;
var firstDay = new Date(y, m-1, 1);
var lastDay = new Date(y, m , 0);
var noofdaysinmonth= frappe.datetime.get_day_diff(lastDay,firstDay) + 1
var i;
for (i = 0; i < noofdaysinmonth; i++) { 
  cur_frm.grids[0].grid.add_new_row(null,null,false);
    var newrow = cur_frm.grids[0].grid.grid_rows[cur_frm.grids[0].grid.grid_rows.length - 1].doc;
newrow.date=frappe.datetime.add_days(firstDay, +i)
newrow.billing_period=frm.doc.billing_period
}
cur_frm.refresh
();
}
});
});
