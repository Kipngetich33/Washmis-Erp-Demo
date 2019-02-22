# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from calendar import monthrange

class BillingPeriod(Document):
	'''
	This is the Billing Period Doctype controller 
	class
	'''
	def run_functions(self,function_to_run):
		'''
		function that runs all other validation function 
		of the class reading sheet
		args:
			validate function and its arguments
		}
		'''
		if_value = function_to_run()
		if(if_value["status"]):
			return True
		else:
			frappe.throw(if_value["message"])

	def validate(self):
		'''
		Function that validates each billing period
		'''
		# validate fields
		self.run_functions(self.check_field_are_filled)
		self.run_functions(self.validate_start_and_end_dates)

	def check_field_are_filled(self):
		'''
		Function that ensures that all required fields are
		filled:
		args:
			mandatory fields
		output:
			{"status":True/False,"Message":only if the status is false}
		'''	
		if(self.billing_period == None):
			return {"status":False,"message":"The {} field is mandatory".format("Billing Period Name")}
		elif(self.start_date_of_billing_period == None):
			return {"status":False,"message":"The {} field is mandatory".format("Start Date of Billing Period")}
		elif(self.end_date_of_billing_period == None):
			return {"status":False,"message":"The {} field is mandatory".format("End Date of Billing Period")}
		else:
			return {"status":True}

	def validate_start_and_end_dates(self):
		'''
		Functions that validates the start and end date 
		of each billing period
		'''
		start_date=  self.start_date_of_billing_period
		# get the correct end date based on the given month and year
		correct_end_date = monthrange(int(start_date[0:4]),int(start_date[5:7]))[1]
		
		# start dates should be first
		if(self.start_date_of_billing_period[8:10]!= "01"):
			return {"status":False, "message":"The Start Date Should be 1st of the Month"}
		elif(self.end_date_of_billing_period[8:10]!= str(correct_end_date)):
			return {"status":False, "message":"The End Date Should be {} of the Month".format(str(correct_end_date))}
		else:
			return {"status":True}



		
	
		


 
