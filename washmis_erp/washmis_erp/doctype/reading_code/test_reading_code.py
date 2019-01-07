# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
import frappe.defaults
from reading_code import validate_name,validate_reading_quality


class TestReadingCode(unittest.TestCase):
	'''
	Class that tests the Reading Code Doctype 
	functionality
	'''
	def setUp(self):
		'''
		function runs at the beggining of every test
		'''
		self.test_code = frappe.get_doc({
				"doctype": "Reading Code",
				"name1":"test_reading_code",
			})

	
	def tearDown(self):
		'''
		Destroy the test data after each test
		'''
		# frappe.delete_doc("Reading Code","test_reading_code")
		pass

	def test_validate_name(self):
		'''
		Function that tests the validate name
		function
		'''
		self.test_code_1 = frappe.get_doc({
				"doctype": "Reading Code",
				"name1":"t",
			})
		test_name_1 = validate_name(self.test_code.name1)
		test_name_2 = validate_name(self.test_code_1.name1)
		
		self.assertTrue(test_name_1["status"])
		self.assertFalse(test_name_2["status"])

	def test_validate_reading_quality(self):
		'''
		Function that tests the validate reading quality 
		function
		'''
		self.test_code_1 = frappe.get_doc({
				"doctype": "Reading Code",
				"name1":"test_reading_code",
				"good":1,
				"bad":0
			})

		self.test_code_2 = frappe.get_doc({
				"doctype": "Reading Code",
				"name1":"test_reading_code",
				"good":0,
				"bad":1
			})

		self.test_code_3 = frappe.get_doc({
				"doctype": "Reading Code",
				"name1":"test_reading_code",
				"good":1,
				"bad":1

			})

		test_quality_1 = validate_reading_quality(self.test_code_1.good, self.test_code_1.bad)
		test_quality_2 = validate_reading_quality(self.test_code_2.good, self.test_code_2.bad)
		test_quality_3 = validate_reading_quality(self.test_code_3.good, self.test_code_3.bad)
		self.assertTrue(test_quality_1["status"])
		self.assertTrue(test_quality_2["status"])
		self.assertFalse(test_quality_3["status"])


