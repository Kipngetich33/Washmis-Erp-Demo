// Copyright (c) 2019, Paul Karugu and contributors
// For license information, please see license.txt

/* section below contains general functions*/
// =================================================================================================

// global variables

var field_to_hide_unhide = {
	hours:["hours"],
	days:["days"],
	all:["hours","days"]
}

/*function that hides fields ,called on refresh*/
function hide_unhide_fields(frm, list_of_fields, hide_or_unhide) {
	for (var i = 0; i < list_of_fields.length; i++) {
		frm.toggle_display(list_of_fields[i], hide_or_unhide)
	}
}

// function that hides or unhides certain fields on refresh
function hide_unhide_on_refresh(frm) {
	if (frm.doc.average_turn_around_time == "Hours") {
		hide_function(frm, field_to_hide_unhide, "hours")
	}
	else if (frm.doc.average_turn_around_time == "Days") {
		hide_function(frm, field_to_hide_unhide, "days")
	}
	else {
		hide_function(frm, field_to_hide_unhide, "none")
	}

	// check whether to show if_yes_which_task_does_this_task_come_after field
	if(frm.doc.does_this_task_require_to_be_handled_after_another_task == "Yes"){
		frm.toggle_display("if_yes_which_task_does_this_task_come_after", true)
	}
	else{
		frm.toggle_display("if_yes_which_task_does_this_task_come_after", false)
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

// function that alerts a message provided to it as parameter
function alert_message(message_to_print){
	msgprint(message_to_print)
}

/* end of the general functions section
// =================================================================================================
/* This section  contains functions that are triggered by the form action refresh or
reload etc to perform various action*/

frappe.ui.form.on('Common Tasks', {
	refresh: function(frm) {
		// hide unhide fields
		hide_unhide_on_refresh(frm)
	}
});


// functionality triggered by filling the does_this_task_require_to_be_handled_after_another_task
frappe.ui.form.on("Common Tasks", "does_this_task_require_to_be_handled_after_another_task", function (frm) {
	frm.refresh()
	// clear the unselected field
	frm.doc.total_time_to_finish_task = ""
	frm.doc.if_yes_which_task_does_this_task_come_after = ""
})

// functionality triggered by clicking on the Average Turn Around Time button
frappe.ui.form.on("Common Tasks", "average_turn_around_time", function (frm) {
	console.log("triggered avarage")
	frm.refresh()

	// clear the unselected field
	frm.doc.days = ""	
	frm.doc.hours = ""
	frm.doc.total_time_to_finish_task = ""

	if(frm.doc.hours){
		console.log("still exists")
	}
})

// functionality triggered by filling the hours field
frappe.ui.form.on("Common Tasks", "hours", function (frm) {
	calcuate_total_turnaround_time(frm)
	frm.refresh()
})

// functionality triggered by filling the days field
frappe.ui.form.on("Common Tasks", "days", function (frm) {
	calcuate_total_turnaround_time(frm)
	frm.refresh()
})

// functionality triggered by clicking does_this_task_require_to_be_handled_after_another_task
frappe.ui.form.on("Common Tasks", "if_yes_which_task_does_this_task_come_after", function (frm) {
	calcuate_total_turnaround_time(frm)
	frm.refresh()
})
