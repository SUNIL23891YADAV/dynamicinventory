#!/usr/bin/env python

'''
Example custom dynamic inventory script for Ansible, in Python.
'''

import os
import sys
import argparse
import csv

try:
    import json
except ImportError:
    import simplejson as json

csvfilepath = "input.csv"
jsonFilePath = "output.json"    

class ExampleInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.example_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory);

    # Example inventory for testing.
    def example_inventory(self):
            

            rows = {}
            new_data_dict = {}

            with open(csvfilepath, 'r') as data_file:
                data = csv.DictReader(data_file, delimiter=",")

                for row in data:
                    item = dict()
                    temp_list = []
                    temp_list = row["hosts"].split(",")
                    item["hosts"] = temp_list
                    #item["chidren"] = row["children"]
                    item["vars"] = dict()
                    item["vars"]["ansible_ssh_user"] = row["ansible_ssh_user"]
                    #item["vars"]["ansible_ssh_key"] =  row["ansible_ssh_user"]

                    new_data_dict[row["Groups"]] = item 
                    
                    item = {}
                    item['hostvars'] = {}
                    new_data_dict[row["_meta"]] = item



            # converting it to into Json

            with open(jsonFilePath, "w") as jsonFile:
                jsonFile.write(json.dumps(new_data_dict, indent=4))
                #print (json.dumps(new_data_dict))
                #data = json.load(read_file)
            #return (json.load(new_data_dict))

            with open(jsonFilePath, "r") as read_file:
                 data = json.load(read_file)

            return data
   

            
    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

# Get the inventory.
ExampleInventory()
