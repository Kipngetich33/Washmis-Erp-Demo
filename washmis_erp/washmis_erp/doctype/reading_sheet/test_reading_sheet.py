# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import frappe.defaults
import unittest

class TestReadingSheet(unittest.TestCase):
	'''
    Class that tests the Reading Code Doctype 
    functionality
    '''
	@classmethod
	def setUpTestData(cls):
		'''
		Function that sets up required test data only 
		once
		'''
		pass

	def setUp(self):
		frappe.set_user("Administrator")

		# test customer
		self.test_customer_1 = frappe.get_doc({
			"doctype":"Customer",
			"customer_name":"Test Customer",
			"customer_group":"Domestic",
			"territory":"Kenya",
			"area":"Area A",
			"zone":"Zone 1.0",
			"route":"Route 1.1"
		})

		# test reading sheets
		self.test_reading_sheet = frappe.get_doc({
			"doctype":"Reading Sheet",
			"billing_period":"January 2018",
			"route":"Route 1.1",
			"route_and_billing_period":"Route 1.1 January 2018"
		})

	
		# add test meter reading sheet row (child table)
		self.test_reading_sheet.append("meter_reading_sheet", {
			"customer_name":"Test Customer",
			"account_no":"1002 - Test Account - WP",
			"previous_manual_reading":20,
			"current_manual_readings":25,
			"manual_consumption":5
		})

		# saving the test data
		self.test_customer_1.insert()
		

	def tearDown(self):
		'''
		Function that runs at the end of each test file to delete items
		'''
		self.test_customer_1.delete()

	def test_validate_customers_exists(self):
		'''
		Function that tests the check if customer exists function
		'''
		customer_exists = self.test_reading_sheet.validate_customers_exists()
		self.assertTrue(customer_exists["status"])

		# missing meter reading sheet
		self.test_reading_sheet.meter_reading_sheet = None
		customer_exists_1 = self.test_reading_sheet.validate_customers_exists()
		self.assertFalse(customer_exists_1["status"])

	def test_validate_customer_details_exists(self):
		'''
		Tests the customer_details_exists function
		'''
		customer_details = self.test_reading_sheet.validate_customer_details_exists()
		self.assertTrue(customer_details["status"])

		#missing account number
		self.test_reading_sheet.meter_reading_sheet[0].account_no = None
		customer_details = self.test_reading_sheet.validate_customer_details_exists()
		self.assertFalse(customer_details["status"])

		#missing previous manual readings
		self.test_reading_sheet.meter_reading_sheet[0].previous_manual_reading = None
		customer_details = self.test_reading_sheet.validate_customer_details_exists()
		self.assertFalse(customer_details["status"])

		#missing current manual readings
		self.test_reading_sheet.meter_reading_sheet[0].current_manual_reading = None
		customer_details = self.test_reading_sheet.validate_customer_details_exists()
		self.assertFalse(customer_details["status"])

		#missing current manual consumption
		self.test_reading_sheet.meter_reading_sheet[0].manual_consumption = None
		customer_details = self.test_reading_sheet.validate_customer_details_exists()
		self.assertFalse(customer_details["status"])

	def test_validate_readings(self):
		'''
		Tests the customer_details_exists function
		'''
		customer_details = self.test_reading_sheet.validate_readings()
		self.assertTrue(customer_details["status"])

		#test with negative previous manual readings
		self.test_reading_sheet.meter_reading_sheet[0].previous_manual_reading = -5
		customer_details = self.test_reading_sheet.validate_readings()
		self.assertFalse(customer_details["status"])

		#test with negative current manual readings
		self.test_reading_sheet.meter_reading_sheet[0].current_manual_reading = -5
		customer_details = self.test_reading_sheet.validate_readings()
		self.assertFalse(customer_details["status"])

		#test with negative manual consumption readings
		self.test_reading_sheet.meter_reading_sheet[0].manual_consumption = -5
		customer_details = self.test_reading_sheet.validate_readings()
		self.assertFalse(customer_details["status"])

	# def test_validate_system_values_for_route(self):
	# 	'''
	# 	Tests the customer_details_exists function
	# 	'''
	# 	# test system value for toot
	# 	self.test_system_value = frappe.get_doc({
	# 		"doctype":"System Values",
	# 		"name":"testvalues",
	# 		"target_document":"Reading Sheet",
	# 		"int_value":1,
	# 		"target_record":"Route 1.1",
	# 		"description":"January 2018",
	# 	})
		
	# 	# save the system values object
	# 	self.test_system_value.insert()
	# 	customer_details = self.test_reading_sheet.validate_system_values_for_route()
	# 	self.assertTrue(customer_details["status"])

	# 	# delete the saved system values
	# 	saved_sytem_values = frappe.get_all('System Values', 
	# 		filters={}, 
	# 		fields=['name']
	# 		)
	# 	name_of_saved_value = saved_sytem_values[0].name
	# 	doc = frappe.get_doc("System Values", name_of_saved_value)
	# 	doc.delete()

	# 	customer_details = self.test_reading_sheet.validate_system_values_for_route()
	# 	self.assertFalse(customer_details["status"])

	def test_create_new_system_values(self):
		'''
		Tests the customer_details_exists function
		'''
		saved_sytem_values = frappe.get_all('System Values', 
			filters={}, 
			fields=['name']
			)
		self.assertEqual(len(saved_sytem_values),0)

		# create new values
		self.test_reading_sheet.create_new_system_values()
		saved_sytem_values = frappe.get_all('System Values', 
			filters={}, 
			fields=['name']
			)
		self.assertEqual(len(saved_sytem_values),1)

		# delete the saved system values
		saved_sytem_values = frappe.get_all('System Values', 
			filters={}, 
			fields=['name']
			)
		name_of_saved_value = saved_sytem_values[0].name
		doc = frappe.get_doc("System Values", name_of_saved_value)
		doc.delete()

	def test_get_period(self):
		'''
		Tests the customer_details_exists function
		'''
		self.test_billing_period = frappe.get_doc({
			"doctype":"Billing Period",
			"billing_period":"test period",
			"start_date_of_billing_period":"1970-01-01",
			"end_date_of_billing_period":"1970-01-31",
			"period_rank":1
		})
		self.test_billing_period.insert()

		found_period = self.test_reading_sheet.get_period("test period")
		self.assertEqual(found_period.name,"test period")

		# delete test data
		doc = frappe.get_doc("Billing Period", "test period")
		doc.delete()

	def test_get_last_system_values_of_route2(self):
		'''
		Tests get_last_system_values_of_route2
		'''
		found_values = self.test_reading_sheet.get_last_system_values_of_route2()
		self.assertFalse(found_values["status"])

		# test system value
		self.test_system_value = frappe.get_doc({
			"doctype":"System Values",
			"target_document":"Reading Sheet",
			"int_value":1,
			"target_record":"Route 1.1",
			"description":"January 2018",
		})

		self.test_system_value.insert()
		found_values = self.test_reading_sheet.get_last_system_values_of_route2()
		self.assertTrue(found_values["status"])

		# delete the saved test system values
		saved_sytem_values = frappe.get_all('System Values', 
			filters={}, 
			fields=['name']
			)
		name_of_saved_value = saved_sytem_values[0].name
		doc = frappe.get_doc("System Values", name_of_saved_value)
		doc.delete()

	def test_compare_period_ranks(self):
		'''
		Tests get_last_system_values_of_route2
		'''
		self.test_billing_period_1 =  frappe.get_doc(
			{	
				"doctype":"Billing Period",
				"billing_period":"Test_billing_period",
				"start_date_of_billing_period":"2019-01-01",
				"end_date_of_billing_period":"2019-01-31",
				"period_rank":1
			}
		)

		self.test_billing_period_2 =  frappe.get_doc(
			{	
				"doctype":"Billing Period",
				"billing_period":"Test_billing_period2",
				"start_date_of_billing_period":"2019-02-01",
				"end_date_of_billing_period":"2019-02-28",
				"period_rank":1
			}
		)

		self.test_reading_sheet = frappe.get_doc({
			"doctype":"Reading Sheet",
			"billing_period":"January 2018",
			"route":"Route 1.1",
			"route_and_billing_period":"Route 1.1 January 2018"
		})

		print " this is the test print"
		# compare_period_ranks = self.test_reading_sheet.compare_period_ranks
		self.test_reading_sheet.compare_period_ranks(self.test_billing_period_2,self.test_billing_period_1)
		# results = compare_period_ranks(self.test_billing_period_2,self.test_billing_period_1)
		# self.assertTrue(results)

		# self.test_billing_period_1.start_date_of_billing_period = "2019-02-01"
		# self.test_billing_period_1.end_date_of_billing_period = "2019-02-28"
		# self.assertFalse(self.test_billing_period_2,self.test_billing_period_1)




		






		


