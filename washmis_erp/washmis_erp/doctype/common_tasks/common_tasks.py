# -*- coding: utf-8 -*-
# Copyright (c) 2019, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CommonTasks(Document):
	'''
	This is the Common Tasks Controller  class
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
		# check if required details exist
		check_details(self)

		# calculate the total time
		calculate_total_turnaround(self)
		
		# frappe.throw("pause")

	def on_trash(self):
		pass

def check_details(self):
	'''
	Function that checks to ensure that crucial details
	are given
	'''
	# if any of the task require another check if the later is given
	if(self.does_this_task_require_to_be_handled_after_another_task == "Yes"):
		if(len(self.if_yes_which_task_does_this_task_come_after) == 0):
			frappe.throw("Please Select a Task That the Current Task Comes After")
		else:
			pass

	# check if the avarage turn around value is given
	if(self.average_turn_around_time == "Hours"):
		if(self.hours == 0):
			frappe.throw("Please Add the Duration in Hours")
		else:
			pass
	elif(self.average_turn_around_time == "Days"):
		if(self.days == 0):
			frappe.throw("Please Add the Duration in Days")
		else:
			pass


def calculate_total_turnaround(self):
	'''
	Function that calculates the total turnaround time
	of the common tasks based on whether or not it depends
	on the results of another task
	E.g. if a common task takes 1 days and it depends
	on the results on another tasks that takes 2 days then
	the total turnaround time for the task is 3 days
	'''
	total_turnaround = 0 

	print "*"*80
	# get the total turnaround of the preceding tasks
	if(len(self.if_yes_which_task_does_this_task_come_after) != 0):
		# get the total turnaround of the preceding tasks
		preceding_task_name = self.if_yes_which_task_does_this_task_come_after
		# preceding_task = frappe.get_doc("Common Tasks",preceding_task_name)

		preceding_task_list = frappe.get_list("Common Tasks",
			fields=["total_time_to_finish_task"],
			filters = {
				"name":preceding_task_name
		})

		# check if the total cost was collected correctly
		if(len(preceding_task_list) == 0):
			frappe.throw("Something Went Wrong Try Again")

		preceding_task =preceding_task_list[0]
		if(preceding_task.total_time_to_finish_task):
			total_turnaround += float(preceding_task.total_time_to_finish_task)
		else:
			pass
	else:
		pass

	# get turnaround of current tasks
	if(self.hours):
		convert_to_days = float(self.hours) / 24
		total_turnaround += convert_to_days

	if(self.days):
		total_turnaround += float(self.days)

	# use the total as the Total turnaround
	self.total_time_to_finish_task = total_turnaround

	

