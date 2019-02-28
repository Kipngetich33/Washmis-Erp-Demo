# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MeterReadingCapture(Document):
	'''
	This is the Reading Sheet Controller  class
	'''
	sales_invoice_items_holder = []

	def validate(self):
		'''
		checks:
		'''
		pass

	
	def on_update(self):
		'''
		Function that runs when the document is saved
		'''
		# collect all required meter reading sheet items 
		sales_invoice_items_list = self.get_meter_reading_sheet_items()
	
		# create sales invoices
		create_new_sales_invoice(sales_invoice_items_list)
		


	def on_trash(self):
		pass

	def get_meter_reading_sheet_items(self):
		'''
		Function that gets all customers and their details
		from the meter reading sheet of the document
		arg:
			self
		output:
			{"status":True "message":[[list of items],...,[..]]}
			or
			{"status":True/False,"message":failure message}
		'''
		# initialize the sales_invoice_items_holder as empty
		sales_invoice_items_holder = []
		# loop through all the items in the meter reading sheet
		for meter_reading in self.meter_reading_sheet:
			# get required details
			sales_invoice_details = {}

			# get area and zone for current root
			area_and_zone = get_zone_and_area_using_route(self.route)
		
			sales_invoice_details["customer"] = meter_reading.customer_name
			sales_invoice_details["billing_period"] = self.billing_period
			sales_invoice_details["route"] = self.route
			sales_invoice_details["area"] = area_and_zone["area"]
			sales_invoice_details["zone"] = area_and_zone["zone"]
			sales_invoice_details["previous_reading"] = meter_reading.previous_manual_reading
			sales_invoice_details["current_reading"] = meter_reading.current_manual_readings
			sales_invoice_details["consumption"] = meter_reading.manual_consumption
			sales_invoice_details["type_of_bill"] = "Actual"

			# get the disconnection profile for current customer
			customer_type =  meter_reading.type_of_customer
			current_disconnection_profile = get_disconnection_profile(customer_type)

			sales_invoice_details["disconnection_profile"] = current_disconnection_profile
			sales_invoice_details["type_of_customer"] = customer_type
			sales_invoice_details["type_of_invoice"] = "Bill"

			# append the dictionary to sales_invoice_items_holder
			sales_invoice_items_holder.append(sales_invoice_details)
		
		return sales_invoice_items_holder

def create_new_sales_invoice(list_of_sales_invoice_details):
	'''
	Function that creates a new sales invoice for meter 
	reading a meter reading sheet
	'''
	# create invoices
	for list_item in list_of_sales_invoice_details:
		doc = frappe.get_doc({"doctype":"Sales Invoice"})
		doc.customer = list_item["customer"]
		doc.billing_period = list_item["billing_period"]
		doc.route = list_item["route"]
		doc.area = list_item["area"]
		doc.zone = list_item["zone"]
		doc.previous_reading = list_item["previous_reading"]
		doc.current_reading = list_item["current_reading"]
		doc.consumption = list_item["consumption"]
		doc.type_of_bill = list_item["type_of_bill"]
		doc.disconnection_profile = list_item["disconnection_profile"]["disconnection_name"]
		doc.type_of_customer = list_item["type_of_customer"]
		doc.type_of_invoice = list_item["type_of_invoice"]

		# get applicable items
		applicable_tarrifs = get_applicable_tariff(list_item["type_of_customer"],"Tariff",list_item["consumption"])
		applicable_rent = get_applicable_rent(list_item["type_of_customer"],"Meter")
		
		# loop throught applicable tarrifs
		items_and_quantities = loop_through_tariffs(applicable_tarrifs,list_item["consumption"])
		# Add applicable tarrif rates
		for item in items_and_quantities:
			doc.append("items", {
				"item_code": item["name"],
				"qty": item["qty"],
				'description': "Monthly Bill",
				'uom':'Nos',
				'conversion_factor': 1.0,
				'income_account': 'Sales - UL',
				'cost_center': 'Main - UL'
			})
		# add applicable meter rent
		name_of_rent_item = applicable_rent[0][0]
		doc.append("items",{
				"item_code": name_of_rent_item,
				"qty": 1,
				'description': "Monthly Bill",
				'uom':'Nos',
				'conversion_factor': 1.0,
				'income_account': 'Sales - UL',
				'cost_center': 'Main - UL'
		})
		# check if the sales invoice already exist
		check_if_sales_invoice_exist(list_item["customer"],list_item["billing_period"])
		# save the invoice
		doc.insert()
		#submit the invoice
		doc.submit()


def get_zone_and_area_using_route(name_of_route):
	'''
	Function that gets the zone and area under which
	a given route lies
	'''
	# get area
	route_doc =frappe.get_doc("Territory", name_of_route)
	route_zone = route_doc.parent_territory
	zone_doc = frappe.get_doc("Territory", route_zone)
	route_area = zone_doc.parent_territory
	return {"zone":route_zone,"area":route_area}

def get_disconnection_profile(customer_type):
	'''
	Function that get the disconnection profile based on the 
	type of customer given
	'''
	disconnection_profile = frappe.get_list("Disconnection Profile",
		fields=["*"],
		filters = {
			"customer_group":customer_type
	})

	if(len(disconnection_profile)!=0):
		return disconnection_profile[0]
	else:
		fail_message = "No Disconnection Profile for Customer Type {}".format(customer_type)
		frappe.throw(fail_message)


def loop_through_tariffs(applicable_tarrifs,consumption):
	list_of_tariffs = []
	# get the first item in the list
	
	if(len(applicable_tarrifs)==1):
		# get first item
		key_value_holder = {}
		first_item  = applicable_tarrifs[:1]
		key_value_holder["name"]=first_item[0][0]
		key_value_holder["qty"]=1
		list_of_tariffs.append(key_value_holder)
		return list_of_tariffs

	elif(len(applicable_tarrifs)==2):
		# get first item
		key_value_holder = {}
		first_item  = applicable_tarrifs[:1]
		key_value_holder["name"]=first_item[0][0]
		key_value_holder["qty"]=1
		list_of_tariffs.append(key_value_holder)

		# get last item
		key_value_holder = {}
		last_item  = applicable_tarrifs[len(applicable_tarrifs)-1:]
		units_within_category = (int(consumption) - last_item[0][2]) +1
		key_value_holder["name"]=last_item[0][0]
		key_value_holder["qty"]=units_within_category
		list_of_tariffs.append(key_value_holder)
		return list_of_tariffs

	elif(len(applicable_tarrifs)>2):
		# get first item
		key_value_holder = {}
		first_item  = applicable_tarrifs[:1]
		key_value_holder["name"]=first_item[0][0]
		key_value_holder["qty"]=1
		list_of_tariffs.append(key_value_holder)

		# get middle items
		middle_items = (applicable_tarrifs[1:len(applicable_tarrifs)-1])
		for item in middle_items:
			key_value_holder = {}
			key_value_holder["name"]=item[0]
			key_value_holder["qty"]=item[1]
			list_of_tariffs.append(key_value_holder)
	
		# get last item
		key_value_holder = {}
		last_item  = applicable_tarrifs[len(applicable_tarrifs)-1:]
		units_within_category = (int(consumption) - last_item[0][2]) +1
		key_value_holder["name"]=last_item[0][0]
		key_value_holder["qty"]=units_within_category
		list_of_tariffs.append(key_value_holder)
		return list_of_tariffs


def get_applicable_tariff(type_of_customer,type_of_item,consumption):
	'''
	Function that get all the applicable items Tariffs
	based on the type of customer
	'''
	# get the applicable tarrifs based on the consumption
	applicable_tariffs = frappe.db.sql("""SELECT name,difference_btw_max_and_min,min_quantity from `tabItem` WHERE type_of_customer = '{}' AND type_of_item = '{}' and min_quantity <= {} ORDER BY min_quantity """.format(type_of_customer,type_of_item,consumption))
	if(len(applicable_tariffs) == 0):
		frappe.throw("No Tarrifs Exist for customer type {}".format(type_of_customer))
	else:
		return applicable_tariffs

def get_applicable_rent(type_of_customer,type_of_item):
	'''
	Function that get all the applicable Meter Rent
	based on the type of customer
	'''
	# get applicable meter rent based on type_of_customer
	applicable_meter_rent = frappe.db.sql("""SELECT name from `tabItem` WHERE type_of_customer = '{}' AND type_of_item = '{}'""".format(type_of_customer,type_of_item))
	if(len(applicable_meter_rent) == 0):
		frappe.throw("No Meter Rent Costs Exist for customer type {}".format(type_of_customer))
	else:
		return applicable_meter_rent
		

def check_if_sales_invoice_exist(customer_name,billing_period):
	'''
	Function that checks if a given billing period has 
	already been created
	'''
	duplicate_sales_invoices = frappe.get_list("Sales Invoice",
		fields=["*"],
		filters = {
			"customer":customer_name,
			"billing_period":billing_period
	})

	if(len(duplicate_sales_invoices)==0):
		pass
	else:
		fail_message = "A Sales invoice for {} for customer {} Already Exist".format(billing_period,customer_name)
		frappe.throw(fail_message)
