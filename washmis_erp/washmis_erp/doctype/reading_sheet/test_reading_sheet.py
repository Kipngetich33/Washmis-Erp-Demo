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
		#test billing period
		self.test_billing_period = frappe.get_doc({
			"doctype":"Billing Period",
			"billing_period":"Test Billing Period 1",
            "start_date_of_billing_period":"1970-01-01",
			"end_date_of_billing_period":"1970-01-31",
			"period_rank":1
		})
		
		#test territory country
		self.test_territory = frappe.get_doc({
			"doctype":"Territory",
			"territory_name":"Test Country 1",
			"type_of_territory":"Country",
			"parent_territory":"All Territories",
			"is_group":1
		})

		# test territory area
		self.test_territory_area = frappe.get_doc({
			"doctype":"Territory",
			"territory_name":"Test Area 1",
			"type_of_territory":"Area",
			"parent_territory":"Test Country 1",
			"is_group":1
		})

		# test territory zone
		self.test_territory_zone = frappe.get_doc({
			"doctype":"Territory",
			"territory_name":"Test Zone 1.0",
			"type_of_territory":"Zone",
			"parent_territory":"Test Area 1",
			"is_group":1
		})

		# test territory route
		self.test_territory_route = frappe.get_doc({
			"doctype":"Territory",
			"territory_name":"Test Route 1.1",
			"type_of_territory":"Route",
			"parent_territory":"Test Zone 1.0",
			"is_group":0
		})

		#test customer group
		self.test_customer_group = frappe.get_doc({
			"doctype":"Customer Group",
			"parent_customer_group":"All Customer Groups",
            "customer_group_name":"Test Customer Group"
		})

		#test account
		self.test_customer_account = frappe.get_doc({
			"doctype":"Account",
			"account_name":"Test Account 1",
			"account_number":0,
			"company":"Upande Ltd",
			"Report Type":"Balance Sheet",
			"currency":"KES",
			"parent_account":"Accounts Receivable - UL",
			"account_type":"Receivable"
		})

		# test customer
		self.test_customer_1 = frappe.get_doc({
			"doctype":"Customer",
			"customer_name":"Test Customer",
			"customer_group":"Test Customer Group",
			"territory":"Test Country 1",
			"area":"Test Area 1",
			"zone":"Test Zone 1.0",
			"route":"Test Route 1.1"
		})

		# save the test data
		self.test_billing_period.insert()
		self.test_territory.insert()
		self.test_territory_area.insert()
		self.test_territory_zone.insert()
		self.test_territory_route.insert()
		self.test_customer_group.insert()
		self.test_customer_account.insert()
		self.test_customer_1.insert()

		# test reading sheets
		self.test_reading_sheet = frappe.get_doc({
			"doctype":"Reading Sheet",
			"billing_period":"Test Billing Period 1",
			"route":"Test Route 1.1",
			"route_and_billing_period":"Test Route 1.1 Test Billing Period 1"
		})
		
		# add test meter reading sheet row (child table)
		self.test_meter_reading_sheet = frappe.get_doc({
			"doctype":"Meter Reading Sheet",
			"customer_name":"Test Customer",
			"account_no":"0 - Test Account 1 - UL",
			"previous_manual_reading":20,
			"current_manual_readings":25,
			"manual_consumption":5
		})
		self.test_reading_sheet.append("meter_reading_sheet",self.test_meter_reading_sheet)


		# second part of test data
		#test billing period
		self.test_billing_period_2 = frappe.get_doc({
			"doctype":"Billing Period",
			"billing_period":"Test Billing Period 2",
            "start_date_of_billing_period":"1970-02-01",
			"end_date_of_billing_period":"1970-02-28",
			"period_rank":2
		})
		
		#test territory country
		self.test_territory_2 = frappe.get_doc({
			"doctype":"Territory",
			"territory_name":"Test Country 2",
			"type_of_territory":"Country",
			"parent_territory":"All Territories",
			"is_group":1
		})

		# test territory area
		self.test_territory_area_2 = frappe.get_doc({
			"doctype":"Territory",
			"territory_name":"Test Area 2",
			"type_of_territory":"Area",
			"parent_territory":"Test Country 2",
			"is_group":1
		})

		# test territory zone
		self.test_territory_zone_2 = frappe.get_doc({
			"doctype":"Territory",
			"territory_name":"Test Zone 2.0",
			"type_of_territory":"Zone",
			"parent_territory":"Test Area 2",
			"is_group":1
		})

		# test territory route
		self.test_territory_route_2 = frappe.get_doc({
			"doctype":"Territory",
			"territory_name":"Test Route 2.1",
			"type_of_territory":"Route",
			"parent_territory":"Test Zone 2.0",
			"is_group":0
		})

		#test customer group
		self.test_customer_group_2 = frappe.get_doc({
			"doctype":"Customer Group",
			"parent_customer_group":"All Customer Groups",
            "customer_group_name":"Test Customer Group 2"
		})

		#test account
		self.test_customer_account_2 = frappe.get_doc({
			"doctype":"Account",
			"account_name":"Test Account 2",
			"account_number":0,
			"company":"Upande Ltd",
			"Report Type":"Balance Sheet",
			"currency":"KES",
			"parent_account":"Accounts Receivable - UL",
			"account_type":"Receivable"
		})

		# test customer
		self.test_customer_2 = frappe.get_doc({
			"doctype":"Customer",
			"customer_name":"Test Customer 2",
			"customer_group":"Test Customer Group 2",
			"territory":"Test Country 2",
			"area":"Test Area 2",
			"zone":"Test Zone 2.0",
			"route":"Test Route 2.1"
		})

		# save the test data
		self.test_billing_period_2.insert()
		self.test_territory_2.insert()
		self.test_territory_area_2.insert()
		self.test_territory_zone_2.insert()
		self.test_territory_route_2.insert()
		self.test_customer_group_2.insert()
		self.test_customer_account_2.insert()
		self.test_customer_2.insert()

		# test reading sheets
		self.test_reading_sheet_2 = frappe.get_doc({
			"doctype":"Reading Sheet",
			"billing_period":"Test Billing Period 2",
			"route":"Test Route 2.1",
			"route_and_billing_period":"Test Route 2.1 Test Billing Period 2"
		})
		
		# add test meter reading sheet row (child table)
		self.test_meter_reading_sheet_2 = frappe.get_doc({
			"doctype":"Meter Reading Sheet",
			"customer_name":"Test Customer",
			"account_no":"0 - Test Account 2 - UL",
			"previous_manual_reading":20,
			"current_manual_readings":25,
			"manual_consumption":5
		})
		self.test_reading_sheet.append("meter_reading_sheet",self.test_meter_reading_sheet_2)
		

	def tearDown(self):
		'''
		Function that runs at the end of each test file to delete items
		'''
		self.test_billing_period.delete()
		self.test_customer_1.delete()
		self.test_territory_route.delete()
		self.test_territory_zone.delete()
		self.test_territory_area.delete()
		self.test_territory.delete()
		self.test_customer_group.delete()
		self.test_customer_account.delete()

		# delete second data set
		self.test_billing_period_2.delete()
		self.test_customer_2.delete()
		self.test_territory_route_2.delete()
		self.test_territory_zone_2.delete()
		self.test_territory_area_2.delete()
		self.test_territory_2.delete()
		self.test_customer_group_2.delete()
		self.test_customer_account_2.delete()

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

	def test_create_new_system_values(self):
		'''
		Tests the customer_details_exists function
		'''
		saved_sytem_values = frappe.get_all('System Values', 
			filters={
					"target_record":"Test Route 1.1",
					"target_document": "Reading Sheet"
				}, 
			fields=['name']
			)
		self.assertEqual(len(saved_sytem_values),0)

		# create new values
		self.test_reading_sheet.create_new_system_values()
		saved_sytem_values = frappe.get_all('System Values', 
			filters={"target_record":"Test Route 1.1",
					"target_document": "Reading Sheet"
					},
			fields=['name']
			)
		self.assertEqual(len(saved_sytem_values),1)

		# delete the saved system values
		saved_sytem_values = frappe.get_all('System Values', 
			filters={
					"target_record":"Test Route 1.1",
					"target_document": "Reading Sheet"
				}, 
			fields=['name']
			)
		name_of_saved_value = saved_sytem_values[0].name
		doc = frappe.get_doc("System Values", name_of_saved_value)
		doc.delete()

	def test_get_period(self):
		'''
		Tests the customer_details_exists function
		'''
		found_period = self.test_reading_sheet.get_period("Test Billing Period 1")
		self.assertEqual(found_period.name,"Test Billing Period 1")

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
			"target_record":"Test Route 1.1",
			"description":"Test Billing Period 1",
		})
		self.test_system_value.insert()
		found_values = self.test_reading_sheet.get_last_system_values_of_route2()
		self.assertTrue(found_values["status"])

		# delete the saved test system values
		saved_sytem_values = frappe.get_all('System Values', 
			filters={
					"target_record":"Test Route 1.1",
					"target_document": "Reading Sheet",
				}, 
			fields=['name']
			)
		name_of_saved_value = saved_sytem_values[0].name
		doc = frappe.get_doc("System Values", name_of_saved_value)
		doc.delete()

	def test_validate_system_values_for_route(self):
		'''
		Tests the customer_details_exists function
		'''
		system_values_exist = self.test_reading_sheet.validate_system_values_for_route()
		self.assertFalse(system_values_exist)
		
		#add system values
		self.test_system_value = frappe.get_doc({
			"doctype":"System Values",
			"target_document":"Reading Sheet",
			"int_value":1,
			"target_record":"Test Route 1.1",
			"description":"Test Billing Period 1",
		})
		self.test_system_value.insert()
		system_values_exist = self.test_reading_sheet.validate_system_values_for_route()
		self.assertTrue(system_values_exist)

		# delete the saved system values
		saved_sytem_values = frappe.get_all('System Values', 
			filters={
					"target_record":"Test Route 1.1",
					"target_document": "Reading Sheet",
				},  
			fields=['name']
			)
		name_of_saved_value = saved_sytem_values[0].name
		doc = frappe.get_doc("System Values", name_of_saved_value)
		doc.delete()

		system_values_exist = self.test_reading_sheet.validate_system_values_for_route()
		self.assertFalse(system_values_exist)











		


