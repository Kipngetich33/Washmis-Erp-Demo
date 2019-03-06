# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SurveyData(Document):
	'''
	This is the controller class for Survey
	Data
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

		# Uncheck the check fields
		self.issue_meter = 0
		self.make_new_connection = 0

		# add all the current details to the child table
		create_survey_data_item(self)
		
	def on_trash(self):
		pass


def create_survey_data_item(self):
	'''
	Function that creates a child data item i.e the 
	Survey data item from the current document
	'''
	