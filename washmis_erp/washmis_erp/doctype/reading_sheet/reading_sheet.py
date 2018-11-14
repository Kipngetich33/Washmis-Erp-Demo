# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ReadingSheet(Document):
	print "*****************Reading Sheet***********************"

	def on_update(self):
		print "*****************Reading Sheet Updated***********************"

		# checks
		# (i) Check that a system value for route exist else create one
		# (ii)Ensure that previous reading  match the previous readings
		#  in the the previous reading period
		# (iii) Ensure that all customers have account numbers

		# get the last reading sheet tracker number
		last_reading_sheet = frappe.get_list("System Values",
		fields=["name","target_document", "int_value","target_record"],
		filters = {
			"target_document": "Reading Sheet",
			"target_record":self.route,
		})

		# (i) Check that a system value for route exist else create one
		if(len(last_reading_sheet)>0):
			new_system_value = frappe.get_doc("System Values", last_reading_sheet[0].name)
			new_system_value.int_value = self.tracker_number
			new_system_value.save()
		else:
			# create a new system value for the route
			new_system_value = frappe.get_doc({'doctype': 'System Values'})
			new_system_value.target_document = "Reading Sheet"
			new_system_value.target_record = self.route
			new_system_value.int_value = 1
			new_system_value.description = self.billing_period
			new_system_value.insert()
		
		# (ii)Ensure that previous reading  match the previous readings
		#  in the the previous reading period
		

