# -*- coding: utf-8 -*-
# Copyright (c) 2018, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import utils
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

		# add checks to ensure that the fileds are filled correctly
		
	def on_trash(self):
		pass


def create_survey_data_item(self):
	'''
	Function that creates a child data item i.e the 
	Survey data item from the current document
	'''
	date_to_apply = frappe.utils.now()
	self.append("survey_data_items", {
		"survey_date":date_to_apply,
		"customer_name":self.customer_name,
		"type_of_sanitation":self.type_of_sanitation,
		"pour_flush_to_sewer":self.pour_flush_to_sewer,
		"flush_to_sewer":self.flush_to_sewer,
		"premises_to_be_charged_sewer_services":self.premises_to_be_charged_sewer_services,
		"ventilated_improved_pit_latrine":self.ventilated_improved_pit_latrine,
		"other_traditional_pit_latrine":self.other_traditional_pit_latrine,
		"other_specify":self.other_specify,
		"gps_coordinate_of_the_meter_x":self.gps_coordinate_of_the_meter_x,
		"gps_coordinate_of_the_t_junction_y":self.gps_coordinate_of_the_t_junction_y,
		"x":self.x,
		"y":self.y,
		"all_customer_information_captured_in_gis":self.all_customer_information_captured_in_gis,
		"comments":self.comments,
		"geolocation":self.geolocation,
		"issue_meter":self.issue_meter,
		"meter_serial_no":self.meter_serial_no,
		"meter_size_or_type":self.meter_size_or_type,
		"initial_reading":self.initial_reading,
		"issue_date":self.issue_date,
		"received_date":self.received_date,
		"connection_with_company":self.connection_with_company,
		"make_new_connection":self.make_new_connection,
		"deposit":self.deposit,
		"new_connection_fee":self.new_connection_fee,
		"the_status_of_the_connection_is_correct":self.the_status_of_the_connection_is_correct,
		"no_other_connection_before":self.no_other_connection_before,
		"there_is_an_appropriate_line_nearby":self.there_is_an_appropriate_line_nearby,
		"the_meter_position_will_be_as_per_the_company_policy":self.the_meter_position_will_be_as_per_the_company_policy,
		"meter_state":self.meter_state
	})

	# print self.survey_data_items
	for item in self.survey_data_items:
		# save the current survey data item
		if(item.survey_date == date_to_apply):
			item.insert()
