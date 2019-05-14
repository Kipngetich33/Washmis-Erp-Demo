# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "washmis_erp"
app_title = "WaSHMIS ERP"
app_publisher = "Paul Karugu"
app_description = "Billing Software for Water Utilities"
app_icon = "fa fa-money"
app_color = "#61a4cc"
app_email = "paul.k.karugu@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/washmis_erp/css/washmis_erp.css"
# app_include_js = "/assets/washmis_erp/js/washmis_erp.js"

# include js, css files in header of web template
# web_include_css = "/assets/washmis_erp/css/washmis_erp.css"
# web_include_js = "/assets/washmis_erp/js/washmis_erp.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "washmis_erp.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "washmis_erp.install.before_install"
# after_install = "washmis_erp.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "washmis_erp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"cron": {
# 		"* * * * *": [ #every day at midnight
# 			'''comment the task below for now until I test it fully to
# 			avoid breaking code
# 			"washmis_erp.tasks.automatic_meter_reading_demo"
# 			'''
# 			# "washmis_erp.tasks.send_valve_closing_command"
# 			# "washmis_erp.tasks.send_valve_opening_command"

# 			],
# 		"0 0 1 * *": [ #every first day of the month at midnight
# 		],
		

# 	}
# }



scheduler_events = {
	"all": [
			# "washmis_erp.tasks.all"
			# "washmis_erp.tasks.send_valve_closing_command"
			# "washmis_erp.tasks.send_valve_opening_command"
	],
	"daily": [
# 		"washmis_erp.tasks.daily"
	],
	"cron": {
        "* * * * *": [
            "washmis_erp.tasks.send_valve_closing_command",
			"washmis_erp.tasks.send_valve_opening_command"
        ],
    },
	"hourly": [
# 		"washmis_erp.tasks.hourly"
	],
	"weekly": [
# 		"washmis_erp.tasks.weekly"
	]
# 	"monthly": [
# # 		"washmis_erp.tasks.monthly"
# 	]
}



# Testing
# -------

# before_tests = "washmis_erp.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "washmis_erp.event.get_events"
# }

