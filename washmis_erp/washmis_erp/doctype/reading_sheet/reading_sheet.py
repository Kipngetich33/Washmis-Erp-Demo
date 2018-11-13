# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ReadingSheet(Document):
	print "*****************start***********************"
	pass

	def on_update(self):
		pass
	# 	last_reading_sheet = frappe.get_list("System Values",
	# 	fields=["name","target_document", "int_value","target_record"],
	# 	filters = {
	# 		"target_document": "Reading Sheet",
	# 		"target_record":self.route,
	# 	})

	# 	print("*******************on update*********************")
	# 	print "this is the response"
	# 	print last_reading_sheet
	# 	print type(last_reading_sheet)

	# 	if(len(last_reading_sheet)>0):
	# 		system_value_document = last_reading_sheet[0]
	# 		print (last_reading_sheet)
	# 		new_system_value = frappe.get_doc("System Values", last_reading_sheet[0].name)
	# 		new_system_value.int_value = last_reading_sheet[0].int_value +1
	# 		new_system_value.save()
			
	# 		# set the value of tracker for reading sheet
	# 		self.tracker_number = new_system_value.int_value
	# 		self.save()
			
			
	# 	else:
	# 		# create a new system value for the route
	# 		new_system_value = frappe.get_doc({'doctype': 'System Values'})
	# 		new_system_value.target_document = "Reading Sheet"
	# 		new_system_value.target_record = self.route
	# 		new_system_value.int_value = 1
	# 		new_system_value.insert()

	# 		# set the value of tracker for reading sheet
	# 		self.tracker_number = new_system_value.int_value
	# 		# self.save()
