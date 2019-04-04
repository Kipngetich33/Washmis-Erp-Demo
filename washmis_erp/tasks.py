import requests
import frappe
import datetime
import pandas
import json
import numpy
import calendar
import datetime

import sys

if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

def create_billing_period():
	#first day of the month 
	first_day_of_the_month = datetime.datetime.today().date().replace(day=1)

	get_month = datetime.datetime.today().month
	get_year = datetime.datetime.today().year

	#get the last day of the month
	last_day = calendar.monthrange(get_year, get_month)[1]

	#get last date of the month
	last_day_of_the_month = datetime.datetime.today().date().replace(day=last_day)

	#create billing period
	get_curr_month_in_text = first_day_of_the_month.strftime("%B")

	#convert first and last date of the month to string
	first_day_of_the_month = first_day_of_the_month.strftime('%Y-%m-%d')
	last_day_of_the_month = last_day_of_the_month.strftime('%Y-%m-%d')

	#billing period text
	billing_period_name = "%s %s"%(get_curr_month_in_text, str(get_year))

	bp_doc_list = frappe.get_list("Billing Period", {"billing_period": billing_period_name})
	if not bp_doc_list:
		data = {
			"doctype": "Billing Period",
			"billing_period": billing_period_name,
			"start_date_of_billing_period": first_day_of_the_month,
			"end_date_of_billing_period":last_day_of_the_month
		}
		bp_doc = frappe.get_doc(data)

		try:
			bp_doc.insert()
			frappe.db.commit()
		except Exception as err:
			print(err)
	#print(first_day_of_the_month, last_day_of_the_month)

def automatic_meter_reading_demo():
	"""
		Using Pure fresh Naivasha Ellitrack device. I am going to simulate weekly billing

	"""

	#Get sensor data from ellitrack
	serial = 17112915

	#get period dates
	first_day_of_the_month = datetime.datetime.today().replace(day=1)
	yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
	#seven_days_earlier = yesterday - datetime.timedelta(days=7)

	period_from = yesterday.strftime("%d-%m-%Y")
	period_from = period_from + ' +00:00:00'
	period_to = yesterday.strftime("%d-%m-%Y")
	period_to = period_to + " +23:59:59"

	#print(period_from, period_to)

	#initialize request session
	login_url = "http://www.ellitrack.nl/auth/login/"

	#authenticate session
	ellitrack_session = requests.Session()
	ellitrack_session.post(login_url, data={'username': "markdeblois", 'password': "upandegani"})

	#get data for pure fresh ellitrack
	data_url = "http://www.ellitrack.nl/measurement/downloadexport/serialnumber/%s/type/period/n/0" \
          "/periodtype/date/periodfrom/%s/periodto/%s/format/json" % (serial, period_from, period_to)
	resp = ellitrack_session.get(data_url)

	if resp.status_code == 200:
		output = StringIO(resp.text)
		ell_df = pandas.read_csv(output, sep="\t")

		#unnecessary columns removed
		ell_df_stripped = ell_df[ell_df.columns[0:2]]

		#get prev and curr readings
		prev_reading = ell_df_stripped['1 Energie'].min()
		curr_reading = ell_df_stripped['1 Energie'].max()

		#Insert data into Meter Reading Sheet Doctype
		data = {
			"doctype": "Meter Reading Capture",
			"reading_date": first_day_of_the_month,
		}
		
		#billing month
		get_curr_month = first_day_of_the_month.strftime("%B")

		automatic_readings_data = {
				"doctype": "Meter Reading Sheet",
				"automatic_meter_id": "%s" %serial,
				"previous_automatic_readings": "%s" %prev_reading,
				"current_automatic_readings": "%s" %curr_reading,
				"parent": "All Territories %s 2018" %get_curr_month,
				"parenttype": "Meter Reading Capture",
				"parentfield": "meter_reading_sheet"
			}

		#check if doc exists
		name = "All Territories "+get_curr_month+" 2018"
		doc_list = frappe.get_list("Meter Reading Capture", filters={'name':name})
		if doc_list:
			mdoc = frappe.get_doc("Meter Reading Capture", name)

			try:
				mrs_doc = frappe.get_doc(automatic_readings_data)
				mrs_doc.insert()
				frappe.db.commit()
			except Exception as err:
				return err
		else:
			#create new doc
			doc = frappe.new_doc("Meter Reading Capture")
			doc.reading_date = first_day_of_the_month
			doc.billing_period = get_curr_month+" 2018"
			doc.route = "All Territories"
			doc.route_and_billing_period = name

			try:
				doc.insert()
				frappe.db.commit()
			except Exception as err:
				return err

			try:
				#update doc with the meter readings
				mrs_doc = frappe.get_doc(automatic_readings_data)
				mrs_doc.insert()
				frappe.db.commit()
			except Exception as err:
				return err


def send_bill():
	'''
	Function that retrives new invoices and 
	sends an sms to the respective customers
	'''
	# get all unsent messages
	list_of_unsent = applicable_meter_rent = frappe.db.sql("""SELECT name,customer, \
		type_of_invoice,bill_amount,total_outstanding_amount from `tabSales Invoice` \
		WHERE sms_sent = 'No' and status ='Unpaid' or status = 'Overdue' """)
	
	# loop through the list of customers
	recipients_and_messages = []
	for unsent in list_of_unsent:
		sales_invoice = unsent[0]
		customer_name = unsent[1]
		type_of_invoice = unsent[2]
		bill_amount = unsent[3]
		total_outstanding_amount = unsent[4]
		
		'''
		# construct message
		print "inside the ofr"
		message_to_send = "You have a new Invoice ({}) of {} ,your new outstanding balance is therefore {}"\
			.format(type_of_invoice,bill_amount,total_outstanding_amount)
		
		# get customer number
		# customer_number = frappe.db.sql("""SELECT name,tel_no \
		# 	from `tabCustomer` WHERE name = '{}'""".format(customer_name))
		
		# set the status of the sales invoice to sent
		sale_invoice_doc = frappe.get_doc('Sales Invoice',sales_invoice)
		sale_invoice_doc.cancel()
		# sale_invoice_doc.sms_sent = "Yes"
		sale_invoice_doc.save()

		# customer = frappe.get_doc('Customer', self.name)
		# doc = frappe.get_doc("Customer System Number","*")
		# 	doc.customer_number = doc.customer_number + 1
		# 	doc.save()

		# return frappe.db.sql("""SELECT * from `tabCustomer`""")
		'''

		# set system values for time smses were sent
		# check if system value exists
		list_of_values = frappe.get_list("System Values",
			fields=["*"],
			filters = {
				"target_document":"Sales Invoice",
				"target_record":"Bill"
		})

		if len(list_of_values) == 0:
			print "None Exist"
			new_system_value = frappe.get_doc({"doctype":"System Values"})
			new_system_value.target_document = "Sales Invoice"
			new_system_value.target_record = "Bill"
			new_system_value.description = "03/04/2019"
			new_system_value.insert()

			sales_value = frappe.get_doc({
				"doctype":"System Values",
				"target_document":"Sales Invoice",
				"target_record":"Bill"
			})
			sales_value.insert()

		elif len(list_of_values) == 1:
			frappe.throw("Exist")
		else:
			frappe.throw("An Error Occured Creating System Values for Sales Invoices")


		
		