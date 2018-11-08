# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ReadingSheet(Document):
	print "****************************************"
	
	pass

	def on_update(self):
		last_reading_sheet = frappe.get_list("System Values",
		fields=["target_document", "int_value","target_record"],
		filters = {
			"target_document": "Reading Sheet",
			"target_record":self.route,
		})

		print("****************************************")
		print "this is the response"
		print last_reading_sheet
		print type(last_reading_sheet)

		if(len(last_reading_sheet)>0):
			# update value
			print last_reading_sheet[0]["int_value"]
		else:
			# create a new document


			 
		
