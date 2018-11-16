# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ReadingSheet(Document):
	print "*******************Validating*******************************"
	def validate(self):
		'''
		checks:
			(i) Ensure that Reading sheets are saved in the right order
				i.e a January Reading Sheet Should come before february
			(ii)
		'''

		# get system value saved for a specific route
		last_system_values = get_last_system_value(self.route)
		
		# get the rank of the billing period in last system value
		rank_of_last_period = get_period(last_system_values.description).period_rank
		rank_of_current_period = get_period(self.billing_period).period_rank
		
		#the ranks of current billing period should be greater than that 
		# of previous by 1
		can_create_sheet = compare_period_ranks(rank_of_current_period,rank_of_last_period)

		if(can_create_sheet):
			# the billing period rank is correct so continue
			pass

		print "********test section**********"
		# frappe.throw("Pause")
		

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
			print "this is the name"
			print last_reading_sheet[0].name

			new_system_value = frappe.get_doc("System Values", last_reading_sheet[0].name)
			new_system_value.int_value = self.tracker_number
			new_system_value.description = self.billing_period
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
		


# ================================================================================
# the section below is the general functions section

def get_last_system_value(route):
	'''
	Function that gets the system values of the last reading sheet
	for a specific route
	'''
	last_system_value = frappe.get_list("System Values",
			fields=["int_value","name","description"],
			filters = {
				"target_document": "Reading Sheet",
				"target_record":route,
			})
	if(len(last_system_value)>0):
		return last_system_value[0]
	else:
		frappe.throw("System Values for Period: {} Does not Exist".format(route))


def get_period(name_of_billing_period):
	'''
	function that returns the billing period values when the
	name of the period's name is provided
	'''
	requested_period_values = frappe.get_list("Billing Period",
			fields=["period_rank","name"],
			filters = {
				"name": name_of_billing_period,
			})

	if(len(requested_period_values)>0):
		return requested_period_values[0]
	else:
		frappe.throw("Billing Period named {} Does not Exist".format(name_of_billing_period))


def compare_period_ranks(rank_of_current_period,rank_of_last_period):
	'''
	function that checks if the current billing period ranks is 
	greater than  the previous one by only 1

	reason:
		(i) should be greater only by one to ensure that the period
			is the next month and not more than 1 month ahead
			eg. if last_period was January the next should be Feb 
			and not March or beyond
	'''
	if(rank_of_current_period > rank_of_last_period+1):
		frappe.throw("Please Create Reading Sheet for the Previous First")
	elif(rank_of_current_period == rank_of_last_period+1):
		return True
	elif(rank_of_current_period < rank_of_last_period+1):
		frappe.throw("Reading Sheet for Given Period Has Already Been Created")


