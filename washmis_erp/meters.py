# -*- coding: utf-8 -*-
# Copyright (c) 2019, Paul Karugu and contributors
# For license information, please see license.txt

'''
The module below is a meant to demostrate location of assets by bulling data 
from kewaco geonode and adding locations to the master meters , doing this there 
are some important records that the assets depends on this include:

Item Code = "Kewasco Master Meter"
Item Name = "Kewasco Master Meter"
Asset Category = "Master Meters"
Asset Owner = "Company"
Asset Owner Company = "Viwasco" # because the current test company is viwasco
Gross Purchase Amount = 25000 
Is Existing Asset = True i.e 1

Location is dynamically generated in the function
Location aspects:

Name = Meter Serial Number
Location Name = Meter Serial Number
Latitude = Latitude
Longitude = Longitude
Location = GeoLocation string generated from latitude and longitude

'''

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

import requests
import pymysql.cursors
import json
	

def get_gis():
    serial = "27D14BE027630Y"
    url = 'http://gis.washmis.com/geoserver/ows?service=wfs&version=1.1.0&typename=geonode:kewasco_master_meters&request=getfeature&cql_filter=serial_no=%{}%27&outputFormat=json'.format(serial)
    response = requests.get(
        url,
        auth=('admin_kewasco', 'pw4kewasco')
    )
    return response

def get_serial_numbers():
    url = "http://gis.washmis.com/geoserver/ows?service=wfs&version=1.1.0&typename=geonode:kewasco_master_meters&request=getfeature&SRSName=EPSG:4326&outputFormat=json"
    response = requests.get(
        url,
        auth=('admin_kewasco', 'pw4kewasco')
    )

    return response


def process_data():
    gis_data= get_serial_numbers().json()
    
    # get the features
    all_features = gis_data["features"]

    # loop through all features
    for feature in all_features:
        # serial number
        current_serial_no = feature["properties"]["serial_no"]
        print current_serial_no

        # save location
        if current_serial_no == None:
            pass
        else:
            # save asset location
            save_location(feature)
            # save asset
            save_asset(feature)

def save_location(serial_location):
    '''
    Function that saves each serial number and its
    location
    '''
    # serial number
    serial_no = serial_location["properties"]["serial_no"]
    # cordinates
    latitude = serial_location["geometry"]["coordinates"][0][1]
    longitude = serial_location["geometry"]["coordinates"][0][0]

    #location and comments and meter size
    meter_size = serial_location["properties"]["meter_size"]
    location =  meter_size = serial_location["properties"]["location"]
    comments =  meter_size = serial_location["properties"]["comments"]

    geol_str = {}
    geol_str["type"] = "FeatureCollection"
    geol_str["features"] = [{
        "type":"Feature",
        "properties":{},
        "geometry":{
            "type":"Point",
            "coordinates":[longitude,latitude]
            }
    }]

    geol_str = json.dumps(geol_str)

    # create connection
    connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Empharse333',
            db='2f9071bd4f19be4c',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor: 
            # construct the sql syntax
            sql = "INSERT INTO `tabLocation` (`name`,`location_name`,`parent_location`,`latitude`,`longitude`,`location`) VALUES ('{}','{}','{}',{},{},'{}')".format(serial_no,serial_no,'Kewasco Master Meters',latitude,longitude,geol_str)
            # commit the changes
            cursor.execute(sql)

        # save changes to database
        connection.commit()
    finally:
        connection.close()


def save_asset(serial_location):
    '''
    Function that saves and update assets details
    '''

    # serial number
    serial_no = serial_location["properties"]["serial_no"]

     # create connection
    connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Empharse333',
            db='2f9071bd4f19be4c',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor: 
            # construct the sql syntax
            sql = "INSERT INTO `tabAsset` (`name`,`asset_name`,`item_code`,`item_name`,`asset_category`,`asset_owner`,`company`,`location`,`purchase_date`,`gross_purchase_amount`,`available_for_use_date`,`is_existing_asset`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',{})".format(serial_no,serial_no,'Kewasco Master Meter','Kewasco Master Meter','Master Meters','Company','Viwasco',serial_no,'2019-04-15',25000,'2019-04-15',1)
            # commit the changes
            cursor.execute(sql)
        
        # save changes to database  
        connection.commit()
    finally:
        connection.close()