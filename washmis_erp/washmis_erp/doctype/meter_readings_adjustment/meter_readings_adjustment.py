# -*- coding: utf-8 -*-
# Copyright (c) 2019, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MeterReadingsAdjustment(Document):
	'''
	This is the controller class for meter reading 
	Sheets
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
		# check all required fields are available
		# check_required_fields()

		# ensure that the adjustment is being done on the latest month
		system_values_list = frappe.get_list("System Values",
			fields=["*"],
			filters = {
				"target_document":"Reading Sheet",
				"target_record":self.route,
				"description":self.billing_period
		})
		if(len(system_values_list)==0):
			frappe.throw("You Can Only Adjust the Reading of The Last Billing Period")
		else:
			pass


		# Adjust customer's previous reading
		adjust_customer_previous_reading(self.customer,self.new_readings)
		# update adjusted readings on meter reading adjustment
		self.new_previous_customer_readings = self.new_readings
		
		# Adjust previous reading sheet's values
		adjust_reading_sheet_values(self.customer,self.billing_period,self.new_readings)
		# update adjusted previous reading sheet values
		self.adjusted_reading_sheet_value = self.new_readings
		self.new_reading_sheet_value  = self.new_readings

		# update adjusted consumption values on meter reading adjustment
		self.adjusted_consumption = int(self.new_readings) - int(self.previous_readings)

		# Adjust sales invoice values
		if(self.sales_invoice_to_amend):
			adjust_sales_invoice_values(self,self.customer,self.billing_period,self.new_readings)

		else:
			# no sales invoice matching exist yet 
			pass

	def on_trash(self):
		pass


def check_required_fields():
	'''
	Function that runs checks to ensure that
	all the required fields are given
	'''
	pass


def adjust_customer_previous_reading(customer_name,new_readings):
	'''
	Function that sets the customer's previous 
	reading
	'''
	customer_doc =frappe.get_doc("Customer", customer_name)
	customer_doc.previous_reading = new_readings
	customer_doc.save()


def adjust_reading_sheet_values(customer_name,billing_period,new_readings):
	'''
	Function that set the value of previous reading sheets
	'''
	found_reading_sheets = frappe.get_list("Meter Reading Sheet",
		fields=["*"],
		filters = {
			"parenttype":"Reading Sheet",
			"customer_name":customer_name,
			"billing_period":billing_period
	})

	# check if reading sheet available
	if(len(found_reading_sheets)!=0):
		pass
	else:
		fail_message = "No Reading Sheet Record available for Customer '{}' for Billing Period '{}'".format(customer_name,billing_period)
		frappe.throw(fail_message)

	#get the name of reading sheet
	previous_reading_sheet_name = found_reading_sheets[0].name
	 
	# set new values to meter reading sheet
	meter_reading_sheet_doc =frappe.get_doc("Meter Reading Sheet",previous_reading_sheet_name )
	if(new_readings < int(meter_reading_sheet_doc.current_manual_readings)):
		pass
	elif(new_readings == int(meter_reading_sheet_doc.current_manual_readings)):
		frappe.throw("New Readings is Equal to the previous reading")
	elif(new_readings > int(meter_reading_sheet_doc.current_manual_readings)):
		frappe.throw("You Are trying to Increase billing for Previous Period You Should Instead Just Create a Sales Invoice with the Difference")
	meter_reading_sheet_doc.current_manual_readings = new_readings
	
	#calculate consumption
	new_consumption = new_readings - int(meter_reading_sheet_doc.previous_manual_reading)

	# ensure the consumption is not negative
	if(new_consumption >= 0):
		pass
	else:
		frappe.throw("The Consumption Value Cannot be Less then 0")
	
	# set new consumption
	meter_reading_sheet_doc.manual_consumption = new_consumption
	meter_reading_sheet_doc.save()


def adjust_sales_invoice_values(self,customer,billing_period,new_readings):
	'''
	Function that adjusts the values of the existing sales invoice
	'''
	# get applicable sales invoice
	fetched_sales_invoice = get_sales_invoice(customer,billing_period)
	
	# get items from sales invoice
	invoice_items = get_sales_invoice_items(fetched_sales_invoice.name)
	
	# get items details from item doctype
	fetched_item_docs = fetch_items_by_code(invoice_items)

	# the assumption is that all adjustements will be made to reduce the bill
	# adjustment to increase the bill will require a different approach
	new_consumption = new_readings - fetched_sales_invoice.previous_reading

	# get items on which reduction will be implemented
	reduction_items = get_reduction_items(fetched_item_docs,new_consumption)
	previous_consumption = fetched_sales_invoice.consumption
	invoice_name = fetched_sales_invoice.name
	
	# calculate quantity and items to reduce
	calulate_reduction(self,reduction_items,new_consumption,customer,fetched_sales_invoice,new_readings)
	

def get_sales_invoice(customer,billing_period):
	'''
	Function that gets the sales invoice linked
	to current customer and period
	'''
	sales_invoices = frappe.get_list("Sales Invoice",
		fields=["name","consumption","previous_reading"],
		filters = {
			"customer":customer,
			"billing_period":billing_period,
			"is_return":0
	})
	if(len(sales_invoices) == 1):
		return sales_invoices[0]
	elif(len(sales_invoices)<1):
		message = "Sales Invoice Matching Customer {} and Billing Period {} Does Not Exist".format(customer,billing_period)
		frappe.throw(message)
	elif(len(sales_invoices)>1):
		message = "There Exist More than One Sales Invoice Matching Customer {} and Billing Period {}".format(customer,billing_period)
		frappe.throw(message)


def get_sales_invoice_items(sales_invoice_name):
	'''
	function that fetches and arranges all the items
	from a given sales invoice
	'''
	list_of_items = frappe.get_list("Sales Invoice Item",
		fields=["name","item_code","qty"],
		filters = {
			"parent":sales_invoice_name
	})
	return list_of_items


def fetch_items_by_code(invoice_items):
	'''
	Function that fetches an items based on
	their item codes
	'''
	items_list_holder = []
	for invoice_item in invoice_items:
		list_of_items = frappe.get_list("Item",
			fields=["name","type_of_item","min_quantity","max_quantity"],
			filters = {
				"item_code":invoice_item.item_code,
				"type_of_item":"Tariff"
		})
		if(len(list_of_items)==0):
			# item is not a tarrif
			pass
		else:
			items_list_holder.append(list_of_items[0])
	return items_list_holder

def get_reduction_items(fetched_item_docs,new_consumption):
	'''
	Function that gets items on which the reduction will
	be done
	'''
	reduction_items = []
	for item_doc in fetched_item_docs:
		if(item_doc.max_quantity >= new_consumption ):
			reduction_items.append(item_doc)
		else:
			pass
	return reduction_items


def calulate_reduction(self,reduction_items,new_consumption,customer,fetched_sales_invoice,new_readings):
	'''
	Function that determine the quantities of items 
	to be reduced in the credit note
	'''
	# create invoices
	doc = frappe.get_doc({"doctype":"Sales Invoice"})
	doc.customer = customer
	doc.type_of_invoice = "Bill"
	doc.is_return = 1
	doc.return_against = fetched_sales_invoice.name

	# variable holders
	reduction_items = reduction_items
	items_counter = 0 
	item_n_quantity = []

	# loop through the reduction items
	for item in reduction_items:
		diff = 0
		if(item.min_quantity == 0):
			diff = 0
		elif(item.max_quantity >= fetched_sales_invoice.consumption):
			# count number of items
			items_counter +=1

			if(item.min_quantity <= new_consumption and item.max_quantity >= new_consumption):
				# use the difference between previous consumption and current consumption
				diff = fetched_sales_invoice.consumption - new_consumption
			else:
				# use the difference between the previous consumption min_quantity
				diff = (fetched_sales_invoice.consumption - item.min_quantity)+1
		else:
			# count number of items
			items_counter +=1

			if(item.min_quantity <= new_consumption and item.max_quantity >= new_consumption):
				# use the difference between max_quantity and new_consumption
				diff = item.max_quantity - new_consumption
			else:
				# use the diffrence between then min and max value
				diff = (item.max_quantity - item.min_quantity)+1

		# now add items below using the diff
		diff *= -1
		if(diff == 0):
			pass
		else:
			doc.append("items", {
				"item_code":item.name,
				"qty": diff,
				'description': "Return",
				'uom':'Nos',
				'conversion_factor': 1.0,
				'income_account': 'Sales - UL',
				'cost_center': 'Main - UL'
			})

			# add items reduced
			item_n_quantity.append({"name":item.name,"qty":diff})

	
	# save the invoice
	if(items_counter == 0):
		# update the adjsuted sale invoice amount
		doc = frappe.get_doc("Sales Invoice",fetched_sales_invoice.name)
		self.new_sales_invoice_value = doc.total

	else:
		# calculate the adjusted sales invoice value
		calculate_adjusted_sales_invoice_value(self,fetched_sales_invoice.name,item_n_quantity)

		# save the credit note
		doc.insert()
		#submit the invoice
		doc.submit()


def calculate_adjusted_sales_invoice_value(self,invoice_name,item_n_quantity):
		found_credit_notes = frappe.get_list("Sales Invoice",
			fields=["name"],
			filters = {
				"return_against":invoice_name
		})
		# calculate the amount the customer will not pay
		total_reduction = 0
		for credit_note in found_credit_notes:
			doc = frappe.get_doc("Sales Invoice",credit_note.name)
			doc.cancel()
			doc.delete()

		# calculate reduction from current items
		for item in item_n_quantity:
			# get the item
			item_price_list = frappe.db.sql(""" SELECT price_list_rate FROM `tabItem Price` WHERE item_code = '{}' """.format(item["name"]))
			item_price = item_price_list[0][0]
			total_reduction += item_price * item["qty"]

		self.new_sales_invoice_value = self.previous_invoice_amount + total_reduction

		

		