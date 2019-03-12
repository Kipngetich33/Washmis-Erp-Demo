# -*- coding: utf-8 -*-
# Copyright (c) 2019, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# python std lib import
import ast

# frappe import
import frappe
from frappe.model.document import Document

class TestingMaps(Document):

	def validate(self):
		'''
		checks:
		'''
		pass

	
	def on_update(self):
		'''
		Function that runs when the document is saved
		'''
		print "*"*80
		
		# convert geolocation string to a python dictionary
		geo_location = ast.literal_eval(self.test_locations)
		geo_location["features"][0]["properties"]["Description"] = "Test Project"
		print geo_location
		# frappe.throw("pause")

	def on_trash(self):
		pass
