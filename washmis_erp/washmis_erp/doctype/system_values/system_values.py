# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SystemValues(Document):
	'''
	This is the controller class for meter reading 
	Adjustment
	'''
	def validate(self):
		'''
		checks:
		'''
		pass

	def on_update(self):
		'''
		Function that runs when the document is saved
		'''
		# check if a duplicate system value exists
		# check_duplicate(self)
		
	def on_trash(self):
		pass

def check_duplicate(self):
	'''
	Check for duplicate system values
	'''
	system_values_list = frappe.get_list("System Values",
		fields=["name"],
		filters = {
			"target_document":self.target_document,
			"target_record":self.target_record
	})
	frappe.throw("pause")

	# if(self.name == system_values_list[0].name):
	# 	pass
	# else:
	# 	frappe.throw("There is already Similar System Values Document")
	