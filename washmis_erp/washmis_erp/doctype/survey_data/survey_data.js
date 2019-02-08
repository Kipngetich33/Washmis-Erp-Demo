// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt

/* section below contains general functions*/
// =================================================================================================

// global variables

var field_to_hide_unhide = {
	sewered_fields:["pour_flush_to_sewer","flush_to_sewer"],
	onsite_fields:["septic_tanks","ventilated_improved_pit_latrine",
		"other_traditional_pit_latrine",
		"premises_to_be_charged_sewer_services"
	],
	other:["other_specify"],
	all:["septic_tank","ventilated_improved_pit_latrine",
		"other_traditional_pit_latrine","premises_to_be_charged_sewer_services",
		"pour_flush_to_sewer","flush_to_sewer","other_specify"
	]
}

/*function that hides fields ,called on refresh*/
function hide_unhide_fields(frm, list_of_fields, hide_or_unhide) {
	for (var i = 0; i < list_of_fields.length; i++) {
		frm.toggle_display(list_of_fields[i], hide_or_unhide)
	}
}


// function that hides or unhides certain fields on refresh
function hide_unhide_on_refresh(frm) {
	console.log("On refresh")
	if (frm.doc.type_of_sanitation == "Sewered") {
		hide_function(frm, field_to_hide_unhide, "sewered_fields")
	}
	else if (frm.doc.type_of_sanitation == "OnSite") {
		hide_function(frm, field_to_hide_unhide, "onsite_fields")
	}
	else if (frm.doc.type_of_sanitation == "None") {
		hide_function(frm, field_to_hide_unhide, "other")
	}
	else {
		hide_function(frm, field_to_hide_unhide, "none")
	}

	function hide_function(frm, field_to_hide_unhide, selected_option) {
		var hide_fields = field_to_hide_unhide["all"]
		var unhide_fields = field_to_hide_unhide[selected_option]
		if (selected_option == "none") {
			hide_unhide_fields(frm, hide_fields, false)
		}
		else {
			hide_unhide_fields(frm, hide_fields, false)
			hide_unhide_fields(frm, unhide_fields, true)
		}
	}
}



/* end of the general functions section
// =================================================================================================
/* This section  contains functions that are triggered by the form action refresh or
reload to perform various action*/

/* end of the form triggered functions section
// =================================================================================================
/*function that acts when the readings field under meter reading sheet is
filled*/


frappe.ui.form.on('Survey Data', {
	refresh: function(frm) {
		hide_unhide_on_refresh(frm)

	}
});

//function that sets the customer name read_only on save
// frappe.ui.form.on("Survey Data", "refresh", function(frm) { 
// 	// use the __islocal value of doc, to check if the doc is saved or not 
// 	frm.set_df_property("customer_name", "read_only", frm.doc.__islocal ? 0 : 1); 
// });

// function that returns to task on save 
// frappe.ui.form.on("Survey Data", { after_save: function(frm){
// 	console.log("returning")
// 	frappe.set_route("Form", "Task","TASK-2018-00032")
// }});

frappe.ui.form.on("Survey Data", "type_of_sanitation", function (frm) {
	console.log("clicked")
	frm.refresh()

})
