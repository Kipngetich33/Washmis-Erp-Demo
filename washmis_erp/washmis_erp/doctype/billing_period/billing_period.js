// Copyright (c) 2018, Paul Karugu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Billing Period', 'start_date_of_billing_period', function(frm) {
		var isLeap = (year) => new Date(year, 1, 29).getDate() === 29;
		var selected_month = frm.doc.start_date_of_billing_period.slice(5,7)
		var selected_year = frm.doc.start_date_of_billing_period.slice(0,4)
		var days_to_add = 0
		var months_with_30_days = ['04','06','09','11']
	
		if(selected_month == '02'){
			if(isLeap(selected_year)){
				days_to_add += 28	
			}
			else{
				days_to_add += 27
			}
		}
		else if(months_with_30_days.includes(selected_month)){
			days_to_add += 29
		}
		else{
			days_to_add += 30
		}
		var set_end = frappe.datetime.add_days(frm.doc.start_date_of_billing_period, +days_to_add)
		cur_frm.set_value("end_date_of_billing_period", set_end)
});

