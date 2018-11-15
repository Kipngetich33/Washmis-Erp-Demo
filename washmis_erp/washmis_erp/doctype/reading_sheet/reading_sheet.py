# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ReadingSheet(Document):
	def validate(self):
		pass
		# print "*******************Validating*******************************"
		# print "self.route"
		# print self.route 
		# print self.billing_period

		# get the last billing_period from the system values
		# last_reading_sheet = frappe.get_list("System Values",
		# fields=["name","target_document", "int_value","target_record"],
		# filters = {
		# 	"target_document": "Reading Sheet",
		# 	"target_record":self.route,
		# })
		# last_reading_sheet = get_last_reading_sheet(self)
		
		# if(len(last_reading_sheet)>0):
		# 	# system value for the route exist
		# 	name_of_billing_period = last_reading_sheet[0].description
		# 	print "name of period"
		# 	print name_of_billing_period
		# 	# get the date and rank of billing period
		# 	# billing_period = get_date_and_rank(name_of_billing_period)
		# 	billing_period = get_date_and_rank("January")
		# 	if(len(billing_period)>0):
		# 		print "billing period"
		# 		print billing_period				
		# 	else:
		# 		frappe.throw(_("The Selected Billing Period Does Not Exist"))
				
			
		# else:
		# 	# system value for the route exist does 
		# 	print "Last System values does not exist"
		# 	pass

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
		



# the section below is the general functions section

def get_last_reading_sheet(self):
	'''
	Function that gets the system values of the last reading sheet
	for a specific route
	'''
	last_reading_sheet = frappe.get_list("System Values",
			fields=["name","target_document", "int_value","target_record"],
			filters = {
				"target_document": "Reading Sheet",
				"target_record":self.route,
			})
	return last_reading_sheet


def get_date_and_rank(name_of_billing_period):
	'''
	function that returns the date and the rank of a
	billing period parsed
	'''
	requested_billing_period = frappe.get_list("Billing Period",
			fields=["name","period_rank", "start_date_of_billing_period","end_date_of_billing_period"],
			filters = {
				"name": name_of_billing_period,
			})
	return requested_billing_period