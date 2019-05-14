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
	connected_with_company:["make_new_connection","deposit","new_connection_fee",
		"the_status_of_the_connection_is_correct","no_other_connection_before",
		"there_is_an_appropriate_line_nearby","the_meter_position_will_be_as_per_the_company_policy",
		"meter_state"
	],
	not_connected_with_company:["make_new_connection","no_other_connection_before",
		"there_is_an_appropriate_line_nearby","the_meter_position_will_be_as_per_the_company_policy",
		"deposit","new_connection_fee"
	],
	all:["septic_tank","ventilated_improved_pit_latrine",
		"other_traditional_pit_latrine","premises_to_be_charged_sewer_services",
		"pour_flush_to_sewer","flush_to_sewer","other_specify",
		"make_new_connection","deposit","new_connection_fee",
		"the_status_of_the_connection_is_correct","no_other_connection_before",
		"there_is_an_appropriate_line_nearby","the_meter_position_will_be_as_per_the_company_policy",
		"meter_state","make_new_connection","no_other_connection_before",
		"there_is_an_appropriate_line_nearby","the_meter_position_will_be_as_per_the_company_policy",
	]
}

var read_only_edit = {
	issue_meter:["meter_serial_no","meter_size_or_type","initial_reading",
		"issue_date","issued_by","received_date","received_by"
	],
	make_new_connection:["deposit","new_connection_fee"],
	all:["meter_serial_no","meter_size_or_type","meter_size_or_type",
	"initial_reading","issue_date","meter_serial_no","meter_size_or_type",
	"initial_reading","issue_date","issued_by","received_date","received_by",
	"deposit","new_connection_fee"
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
	var temporary_list = []
	if (frm.doc.type_of_sanitation == "Sewered") {
		var selected_fields = field_to_hide_unhide["sewered_fields"]
		for(var i = 0; i < selected_fields.length;i++){
			temporary_list.push(selected_fields[i])
		}

	}
	else if (frm.doc.type_of_sanitation == "Onsite") {
		var selected_fields = field_to_hide_unhide["onsite_fields"]
		for(var i = 0; i < selected_fields.length;i++){
			temporary_list.push(selected_fields[i])
		}
	}
	else if (frm.doc.type_of_sanitation == "None") {
		var selected_fields = field_to_hide_unhide["other"]
		for(var i = 0; i < selected_fields.length;i++){
			temporary_list.push(selected_fields[i])
		}
	}

	if(frm.doc.connection_with_company == "Connected"){
		var selected_fields = field_to_hide_unhide["connected_with_company"]
		for(var i = 0; i < selected_fields.length;i++){
			temporary_list.push(selected_fields[i])
		}
	}
	else if(frm.doc.connection_with_company == "Not Connected" ){
		var selected_fields = field_to_hide_unhide["not_connected_with_company"]
		for(var i = 0; i < selected_fields.length;i++){
			temporary_list.push(selected_fields[i])
		}
	}
	hide_unhide_fields(frm, field_to_hide_unhide["all"], false)
	hide_unhide_fields(frm, temporary_list, true)
}

// function that hides or unhides fields when a certain field is clicked
function toogle_read_only(frm){
	// make all fields read only
	var all_fields = read_only_edit["all"]
	for(var i = 0; i< all_fields.length;i++ ){
		// toogle_fields(all_fields[i],false)
		frm.set_df_property(all_fields[i],"read_only",1);
	}

	if(frm.doc.issue_meter == 1){
		var fields_to_toggle = read_only_edit["issue_meter"]
		for(var i = 0; i< fields_to_toggle.length;i++ ){
			// toogle_fields(fields_to_toggle[i],true)
			frm.set_df_property(fields_to_toggle[i],"read_only",0);
		}
	}	

	if(frm.doc.make_new_connection == 1){
		var fields_to_toggle = read_only_edit["make_new_connection"]
		for(var i = 0; i< fields_to_toggle.length;i++ ){
			// toogle_fields(fields_to_toggle[i],true)
			frm.set_df_property(fields_to_toggle[i],"read_only",0);
		}
	}
}

/* end of the general functions section
// =================================================================================================
/* This section  contains functions that are triggered by the form action refresh or
reload etc to perform various action*/

frappe.ui.form.on('Survey Data', {
	refresh: function(frm) {
		// hide unhide fields
		hide_unhide_on_refresh(frm)
		// enable or disable fields
		toogle_read_only(frm)
	}
});

// functionality triggered by clicking on the type of sanitation field
frappe.ui.form.on("Survey Data", "type_of_sanitation", function (frm) {
	frm.refresh()
})

// functionality triggered by clicking on the issue meter button
frappe.ui.form.on("Survey Data", "issue_meter", function (frm) {
	frm.refresh()
})

// functionality triggered by clicking on the make new connection button
frappe.ui.form.on("Survey Data", "make_new_connection", function (frm) {
	frm.refresh()
})

// functionality triggered by clicking on the connection with company
frappe.ui.form.on("Survey Data", "connection_with_company", function (frm) {
	frm.refresh()
})
