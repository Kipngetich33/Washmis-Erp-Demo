# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
import frappe.defaults
from billing_period import BillingPeriod 

class TestBillingPeriod(unittest.TestCase):
	'''
	Class that tests the billing period class objects
	'''

	def setUp(self):
		'''
		function that runs at the beggining of each test to 
		set up test data
		'''
		self.test_billing_period =  frappe.get_doc(
			{	
				"doctype":"Billing Period",
				"billing_period":"Test_billing_period",
				"start_date_of_billing_period":"2019-01-01",
				"end_date_of_billing_period":"2019-01-31",
				"period_rank":1
			}
		)

	def tearDown(self):
		'''
		functions that runs at the end of each test to destroy
		current test data 
		'''
		pass

	def test_run_functions(self):
		'''
		Function that tests the functionality of
		run functions
		'''
		result = self.test_billing_period.run_functions(self.test_billing_period.check_field_are_filled)
		self.assertTrue(result)   

	def test_check_field_are_filled(self):
		'''
		Checks to ensure that all mandatory fields and filled
		correctly
		'''
		result = self.test_billing_period.check_field_are_filled()
		self.assertTrue(result["status"])

		self.test_billing_period.billing_period = None
		result = self.test_billing_period.check_field_are_filled()
		self.assertFalse(result["status"])

		self.test_billing_period.billing_period = "Test_billing_period"
		self.test_billing_period.start_date_of_billing_period = None
		result = self.test_billing_period.check_field_are_filled()
		self.assertFalse(result["status"])

		self.test_billing_period.start_date_of_billing_period = "2019-01-01"
		self.test_billing_period.end_date_of_billing_period = None
		result = self.test_billing_period.check_field_are_filled()
		self.assertFalse(result["status"])

		self.test_billing_period.end_date_of_billing_period = "2019-01-31"
		self.test_billing_period.period_rank = None
		result = self.test_billing_period.check_field_are_filled()
		self.assertFalse(result["status"])

	def test_validate_start_and_end_dates(self):
		'''
		Tests the validate_start_and_end_dates function
		'''
		dates_status = self.test_billing_period.validate_start_and_end_dates()
		self.assertTrue(dates_status["status"])

		self.test_billing_period.start_date_of_billing_period = "2019-01-02"
		dates_status = self.test_billing_period.validate_start_and_end_dates()
		self.assertFalse(dates_status["status"])

		self.test_billing_period.end_date_of_billing_period = "2019-01-02"
		dates_status = self.test_billing_period.validate_start_and_end_dates()
		self.assertFalse(dates_status["status"])

		
		

		
