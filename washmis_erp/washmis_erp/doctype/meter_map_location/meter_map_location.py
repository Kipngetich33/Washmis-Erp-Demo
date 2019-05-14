# -*- coding: utf-8 -*-
# Copyright (c) 2019, Paul Karugu and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests


class MeterMapLocation(Document):

    def validate(self):
        pass
    
    def on_update(self):
        print "*"*80
        print self