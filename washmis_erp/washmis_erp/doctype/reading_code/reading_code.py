# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ReadingCode(Document):
	'''
	Class that test the Reading Code class objects
	'''
	def run_functions(self,if_value):
		'''
		function that runs all other validation function 
		of the class reading sheet
		args:
			validate function and its arguments
		}
		'''
		if(if_value):
			pass
		else:
			frappe.throw(if_value["message"])

	def validate(self):
		#check name validity
		self.run_functions(validate_name(self.name))


def validate_name(given_name):
	'''
	Function that checks that a name
	has more than one character
	args:
		name
	output:
		{"status":True/False, message:"message(only if status is false")
	'''
	if(len(given_name)<=1):
		# frappe.throw("Cannot Save")
		return {"status":False, "message":"Name must be more than 1 letter"}
	else:
		return {"status":True}

def validate_reading_quality(reading_quality_good,reading_quality_bad):
	'''
	Function that validates the reading quality
	to ensure that users click only one (good or bad)
	'''
	if(reading_quality_good == 1 and reading_quality_bad == 0):
		return {"status":True}
	elif(reading_quality_good == 0 and reading_quality_bad == 1):
		return {"status":True}
	else:
		return {"status":False,"message":"You can only select one Reading Quality (Good or Bad)"}
	

