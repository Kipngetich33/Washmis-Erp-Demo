# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

# python std lib imports
from __future__ import unicode_literals
import datetime
from calendar import monthrange

# frappe imports
import frappe
from frappe.model.document import Document


class ReadingSheet(Document):
	'''
	This is the Reading Sheet Controller  class
	'''
	# def run_functions(self,if_value):
	# 	'''
	# 	function that runs all other validation function 
	# 	of the class reading sheet
	# 	args:
	# 		validate function and its arguments
	# 	}
	# 	'''
	# 	if(if_value):
	# 		pass
	# 	else:
	# 		frappe.throw(if_value["message"])

	def run_functions2(self,function_to_run):
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
		checks:
			(i)validate thatcustomers exists in the selected route
			(ii) validate that all required details for customers are given
			(ii) Validate that a system value for route exist else create one
			(iii) Ensure that Reading sheets are saved in the right order
				i.e a January Reading Sheet Should come before february
		'''
		# validate that customers exists in the selected route
		self.run_functions2(self.validate_customers_exists)
		# validate that all required details for customers are given
		self.run_functions2(self.validate_customer_details_exists)
		#validate readings
		self.run_functions2(self.validate_readings)

		# validate system values for route or create one if none exists

		# sytem_values_exist = self.validate_system_values_for_route()
		sytem_values_exist = self.get_last_system_values_of_route2()
		if(sytem_values_exist["status"]):
			pass
		else:
			# create new system values
			self.create_new_system_values()

		#validate order of billing periods
		if(sytem_values_exist["status"]):
			# a value exists hence a  comparison is required 
			current_billing_period = self.get_period(self.billing_period)
			last_saved_period = self.get_period(sytem_values_exist["message"].description)
			self.run_functions2(self.compare_period_ranks(current_billing_period,last_saved_period))
		else:
			# go ahead and save it since no for root exists yet
			pass
			
		# 	system_values_exists = self.get_last_system_values_of_route2()
		# name_of_found_period = None # initialize to none

		# if(system_values_exists["status"]):
		# 	name_of_found_period = self.get_period(system_values_exists["message"].description)
		# else:
		# 	# create new or check the most appropriate way to handle it
		# 	pass
		# # in_right_order = self.validate_reading_sheets_order()



		'''
		# (iv) If Reading Sheet's billing period in order check if its already saved
		reading_already_saved = False
		if(in_right_order):
			reading_already_saved = if_reading_sheet_exist(self.name)
		
		if(reading_already_saved):
			# save customer previous readings but do change system values
			save_current_readings(self.meter_reading_sheet)
		else:
			# save and change system values, customer readings
			save_current_readings(self.meter_reading_sheet)
		
		# Update system values for route
		# You can only update this because all the other test about the
		# order have already passed
		update_system_values_for_route(self)
		'''
		# frappe.throw("pause")
		
	def on_update(self):
		pass
	
	def on_trash(self):
		'''
		Contoller function called before a Reading Sheet
		is deleted
		(i) Deny Deletion to avoid data loss
		'''
		# (i) Deny deletion to avoid loss of data
		# frappe.throw("You Can Only Modify a Reading Sheet Once its Created")
		pass

	# the section below contains functions used by the validate function
	def validate_customers_exists(self):
		'''
		Function that checks if all the required fields 
		have been filled
		'''
		try:
			if(len(self.meter_reading_sheet)== 0):
				return {"status":False,"message":"There Are No Active Customers Marching Route,Billing Period"}
			else:
				return {"status":True}
		except:
			return {"status":False,"message":"There Are No Active Customers Marching Route,Billing Period"}

	def validate_customer_details_exists(self):
		'''
		Function that check that customer_details_exists
		function
		'''
		for i in range(len(self.meter_reading_sheet)):
	 		row_to_check = self.meter_reading_sheet[i]

				#check if account_no exist
			if not (row_to_check.account_no):
				message = "Account No for Customer {} Does Not Exist".\
				format(row_to_check.customer_name)
				return {"status":False,"message":message}

				# check if previous_reading exist
			elif not(row_to_check.previous_manual_reading):
				message = "Previous Readings for Customer {} Does Not Exist".\
				format(row_to_check.customer_name)
				return {"status":False,"message":message}

				# check for current readings 
			elif not(row_to_check.current_manual_readings):
				message = "Current Readings for Customer {} Does Not Exist".\
				format(row_to_check.customer_name)
				return {"status":False,"message":message}

				# check for manual consumption
			elif not(row_to_check.manual_consumption):
				message = "Manual consumption for Customer {} Does Not Exist".\
				format(row_to_check.customer_name)
				return {"status":False,"message":message}
			else:
				return {"status":True}

	def validate_readings(self):
		'''
		Function that checks to ensure that readings 
		dont contain obvious error eg. negatives
		'''
		for i in range(len(self.meter_reading_sheet)):
	 		row_to_check = self.meter_reading_sheet[i]

			if(int(row_to_check.previous_manual_reading)<0):
				message = "Previous Manual Readings for Customer {} is Negative".\
				format(row_to_check.customer_name)
				return {"status":False,"message":message}
			elif(int(row_to_check.current_manual_readings)<0):
				message = "Current Manual Readings for Customer {} is Negative".\
				format(row_to_check.customer_name)
				return {"status":False,"message":message}
			elif(int(row_to_check.manual_consumption)<0):
				message = "Manual Consumption for Customer {} is Negative".\
				format(row_to_check.customer_name)
				return {"status":False,"message":message}
			else:
				return {"status":True}

	def validate_system_values_for_route(self):
		'''
		Checks if system values for the route already 
		exists
		args:
			self
		output:
			True/False
		'''		
		# get the last reading's System Values
		last_reading_system_values = frappe.get_list("System Values",
				fields=["name","target_document", "int_value","target_record"],
				filters = {
					"target_document": "Reading Sheet",
					"target_record":self.route,
			})

		if(len(last_reading_system_values)>0):
			return True
		else:
			return False

	def create_new_system_values(self):
		'''
		function that creates new system values for 
		route if none exist
		'''
		new_system_value = frappe.get_doc({"doctype":"System Values"})
		new_system_value.target_document = "Reading Sheet"
		new_system_value.int_value = self.tracker_number
		new_system_value.target_record = self.route
		new_system_value.description = self.billing_period
		new_system_value.insert()

	def validate_reading_sheets_order(self):
		'''
		Function that checks if the current reading 
		sheet obeys the ranks of billing periods in 
		terms of dates
		args:
			self
		output:
			greater or less than (supposed period)
		'''
		last_saved_period = self.get_last_system_values_of_route().description
		last_period = self.get_period(last_saved_period)
		current_period = self.get_period(self.billing_period)
		
		# compare_period_ranks(current_period,last_period)
		if(self.compare_period_ranks):
			return True
		else:
			return False

	def get_last_system_values_of_route(self):
		'''
		Function that gets the system values of the last reading sheet
		for a specific route
		'''
		last_system_value = frappe.get_list("System Values",
				fields=["int_value","name","description"],
				filters = {
					"target_document": "Reading Sheet",
					"target_record":self.route,
				})
		if(len(last_system_value)==0):
			# no values for system exist yet hence pass
			pass
		else:
			return last_system_value[0]

	def get_last_system_values_of_route2(self):
		'''
		Function that gets the system values of the last reading sheet
		for a specific route
		'''
		last_system_value = frappe.get_list("System Values",
				fields=["int_value","name","description"],
				filters = {
					"target_document": "Reading Sheet",
					"target_record":self.route,
				})
		if(len(last_system_value)!=0):
			return {"status":True,"message":last_system_value[0]}
		else:
			return {"status":False, "message":"No system value exists for route"}

	def get_period(self,name_of_billing_period):
		'''
		function that returns the billing period values when the
		name of the period's name is provided
		'''
		requested_period_values = frappe.get_list("Billing Period",
				fields=["name","period_rank","end_date_of_billing_period","start_date_of_billing_period"],
				filters = {
					"name": name_of_billing_period,
				})

		if(len(requested_period_values)>0):
			return requested_period_values[0]
		else:
			frappe.throw("Billing Period named {} Does not Exist".format(name_of_billing_period))

	def compare_period_ranks(self,current_period,last_period):
		'''
		function that checks if the current billing period 
		start date is exactly the same as the end date of last
		reading sheet or begging of billing period
		'''
		c_start = current_period.start_date_of_billing_period
		c_end = current_period.end_date_of_billing_period
		l_end = last_period.end_date_of_billing_period

		print "*"*100
		print c_start
		print c_end
		print l_end

		correct_start_of_next_period = l_end + datetime.timedelta(days = 1)
		correct_next_end_day = monthrange(correct_start_of_next_period.year,correct_start_of_next_period.month)[1]
		correct_next_end_date = datetime.datetime(correct_start_of_next_period.year,correct_start_of_next_period.month,correct_next_end_day)

		if(c_start < correct_start_of_next_period or c_end < correct_next_end_date):
			message = "The Last Saved Reading Sheet was For Billing Period {} \
					You Cannot Create Reading Sheets For Earlier Periods".format(last_period.name)
			return {"status":False, "message":message}
		elif(c_start > correct_start_of_next_period or c_end > correct_next_end_date):
			message = "Please Create a reading sheet for the previous period first"
			return {"status":False, "message":message}
		elif(c_start == correct_start_of_next_period and c_end == correct_next_end_date):
			return{"status":True}
		else:
			return {"staus":False,"message":"Something went wrong please check and try again"}

	def get_correct_end_dates(self,start_date):
		'''
		Function that takes the 1st day of every month and
		returns the last day of that month
		'''

		start_date=  self.start_date_of_billing_period
		# get the correct end date based on the given month and year
		correct_end_date = monthrange(int(start_date[0:4]),int(start_date[5:7]))[1]


# ================================================================================
# the section below is the general functions section

def save_current_readings(current_meter_reading_sheet):
	'''
	Functions that loops throught all the customer in meter
	reading sheet and call the save_each_customer reading
	function to save them to each customer's previous readings
	'''
	# check if there are any customers in the sheet
	if(len(current_meter_reading_sheet)== 0):
		frappe.throw("There Are No Active Customers Marching Route,Billing Period")
	else:
		# there are customers loop through each one
		for i in range(len(current_meter_reading_sheet)):
			current_row = current_meter_reading_sheet[i]
			save_each_customer_readings(current_row)


def save_each_customer_readings(current_row):
	'''
	Function that saves the each customer's current readings to 
	as their previous readings in the customer doctype
	'''
	customer_system_no = current_row.system_no
	# get the customer
	current_loop_customer = frappe.get_list("Customer",
			filters = {
				"system_no": customer_system_no
			})
	if(len(current_loop_customer)>0):
		current_customer_name = current_loop_customer[0].name
		# get doc of that specific customer
		current_customer_doc = frappe.get_doc("Customer", current_customer_name)
		current_customer_doc.previous_reading = current_row.current_manual_readings
		current_customer_doc.save()
	else:
		frappe.throw("Customer of System No {} Does Not Exist".format(customer_system_no))


def if_january_next_year(current_period,last_period):
	'''
	check the current period is december and the next
	period is Jan of the following year
	'''
	if(last_period.start_date_of_billing_period <current_period.start_date_of_billing_period):
		# check if month and dates 
		if(last_period.start_date_of_billing_period.month == 12 and current_period.start_date_of_billing_period.month ==1 ):
			return True
		else:
			return False
	elif(last_period.start_date_of_billing_period >current_period.start_date_of_billing_period):
		return False
	else:
		return False
	
	
def if_reading_sheet_exist(name_of_current_reading_sheet):
	'''
	Function that checks if the current reading sheet 
	already been saved
	arg:
		name of curren reading sheet
	output:
		True / False
	'''
	requested_reading_sheets = frappe.get_list("Reading Sheet",
			fields=["name"],
			filters = {
				"name": name_of_current_reading_sheet,
			})
	if(len(requested_reading_sheets)>0):
		# a reading sheet with the name already exists
		return True
	else:
		return False


def update_system_values_for_route(self):
	'''
	Function that updates the system values
	for a route by changing the description field to
	value current billling period
	'''

	# get the name of system values for this current route
	system_value_for_route = frappe.get_list("System Values",
			fields=["int_value","name","description"],
			filters = {
				"target_document": "Reading Sheet",
				"target_record":self.route,
			}
		)

	if(len(system_value_for_route)>0):
		new_system_value = frappe.get_doc("System Values", system_value_for_route[0].name)
		new_system_value.int_value = self.tracker_number
		new_system_value.description = self.billing_period
		new_system_value.save()
	else:
		frappe.throw("Cannot Update System Values for Current, No record Exist")



def get_period_with_start_date(correct_start_of_next_period):
	'''
	Function that gets a billing period basing on the given
	start date of billing period
	'''
	requested_period_values = frappe.get_list("Billing Period",
			fields=["name","period_rank","end_date_of_billing_period","start_date_of_billing_period"],
			filters = {
				"start_date_of_billing_period": correct_start_of_next_period,
			})

	if(len(requested_period_values)>0):
		return requested_period_values[0]
	else:
		frappe.throw("Billing Period With Start Date {} Does not Exist, Create It First".format(correct_start_of_next_period))


def get_system_values_for_route(self):
	'''
	Get system values for current route
	args:
		self
	output:
		[..["name","target_document", "int_value","target_record"]]
	'''		
	# get the last reading's System Values
	last_reading_system_values = frappe.get_list("System Values",
	fields=["name","target_document", "int_value","target_record"],
	filters = {
		"target_document": "Reading Sheet",
		"target_record":self.route,
	})
	if(len(last_reading_system_values)==0):
		# no values for system exist yet hence pass
		pass
	else:
		return last_reading_system_values[0]