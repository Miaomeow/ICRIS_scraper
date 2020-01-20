#!/usr/bin/env python3

import os
import glob
import re
import json
import pymongo

from pymongo import MongoClient
from bs4 import BeautifulSoup as bs

PATH = os.getcwd() + '/results'
COLLECTION_NAME = "companies"

client = MongoClient("localhost", 27017)
db = client["icris"]
db.drop_collection(COLLECTION_NAME)
db.create_collection(COLLECTION_NAME)
collection = db[COLLECTION_NAME]
collection.create_index([("basic_info.cr_no", pymongo.ASCENDING)], unique=True)

def clean_empty_fields(data):
    for key, value in data.items():
        if value == '-':
            data[key] = ""

def import_data(data):
    try:
        collection.insert_one(data)
    except pymongo.errors.DuplicateKeyError:
        pass

# Main
for i, filename in enumerate(glob.glob(os.path.join(PATH, '*.html'))):

    print('\n',filename)

    soup = bs(open(filename), 'html.parser')
    content_blocks = soup.find_all('div', 'jqm-block-content2')
    company_info = {}

    
    #Basic Company Information
    
    basic_info = content_blocks[0].find_all('p', {'class':'content'})
    data = {}
    data["cr_no"] = basic_info[0].text.strip()
    data["company_name_eng"] = basic_info[1].text.strip().split('\n')[0]
    try:
        data["company_name_chi"] = basic_info[1].text.strip().split('\n')[1]
    except:
        data["company_name_chi"] = ""
    data["company_type"] = basic_info[2].text.strip()
    data["date_of_incorporation"] = basic_info[3].text.strip()
    data["status"] = basic_info[4].text.strip()
    data["remarks"] = basic_info[5].text.strip()
    data["winding_up_mode"] = basic_info[6].text.strip()
    data["date_of_dissolution"] = basic_info[7].text.strip()
    data["register_of_charges"] = basic_info[8].text.strip()
    data["note"] = basic_info[9].text.strip()

    clean_empty_fields(data)
    company_info['basic_info'] = data

    # Name History

    name_history = content_blocks[1].find_all('p', {'class': 'content'})
    data = {}
    data["effective_date"] = name_history[0].text.strip()
    pattern = re.compile('(?P<eng>[A-Z\.,&\s]+)(?P<chi>.+)')
    old_name = re.search(pattern, name_history[1].text.strip())
    data = {**data, **old_name.groupdict()}

    clean_empty_fields(data) 
    company_info['name_history'] = data

    
    # Registered Office
    
    registered_office = " ".join(content_blocks[2].find('p', 'content').text.strip().split())
    company_info["registered_office"] = registered_office

    
    # Share Capital
    
    share_capital = content_blocks[3].find_all('p', {'class': 'content'})
    data = {}
    data["issued"] = " ".join(share_capital[0].text.strip().split())
    data["paid_up"] = " ".join(share_capital[1].text.strip().split())

    clean_empty_fields(data)
    company_info["share_capital"] = data

    
    #Directors
    
    block_no = 4
    company_info["directors"] = []
    while block_no < len(content_blocks):
        director_num = content_blocks[block_no].find('p', 'content').text.strip()

        if re.match("\d+", director_num) is None:
            break
        
        director = content_blocks[block_no].find_all('p', {'class': 'content'})
        data = {}
        data["name_eng"] = " ".join(director[1].text.strip().split())
        data["name_chi"] = director[2].text.strip()
        data["HKID"] = director[3].text.strip()
        data["overseas_passport_no"] = director[4].text.strip()
        data["passport_country"] = director[5].text.strip()
        data["director_type"] = director[6].text.strip()

        clean_empty_fields(data)
        company_info["directors"].append(data)

        block_no +=1
    
    
    # Company Secretary
    
    # Two cases: body corporate/ natural person
    
    company_info["com_sec"] = []
    counter = 1
    while block_no < len(content_blocks):
        com_sec_no = content_blocks[block_no].find('p').text.strip()
        if re.search("#\d+", com_sec_no) is None:
            break

        com_sec = content_blocks[block_no].find_all('p', {'class': 'content'})
        data = {}

        if com_sec_no.find("Body Corporate") is not -1:
            data["name_eng"] = com_sec[0].text.strip()
            data["name_chi"] = com_sec[1].text.strip()
            data["cr_no"] = com_sec[2].text.strip()
            data["address"] = " ".join(com_sec[3].text.strip().split())
            data["date_of_appointment"] = com_sec[4].text.strip()
            data["note"] = com_sec[5].text.strip()
            data["type"] = "Body Corporate"
        elif com_sec_no.find("Natural Person") is not -1:
            data["surname_eng"] = com_sec[0].text.strip()
            data["name_eng"] = com_sec[1].text.strip()
            data["name_chi"] = com_sec[2].text.strip()
            data["name_prev"] = com_sec[3].text.strip()
            data["alias"] = com_sec[4].text.strip()
            data["address"] = " ".join(com_sec[5].text.strip().split())
            data["HKID"] = com_sec[6].text.strip()
            data["overseas_passport_no"] = com_sec[7].text.strip()
            data["passport_country"] = com_sec[8].text.strip()
            data["date_of_appointment"] = com_sec[9].text.strip()
            data["note"] = com_sec[10].text.strip()
            data["type"] = "Natural Person"
        else:
            print("No matching com sec type")

        clean_empty_fields(data)
        company_info["com_sec"].append(data)
        block_no += 1
        counter += 1
    
    print(json.dumps(company_info, indent=4, sort_keys=True))
    
    # MongoDB
    try:
        collection.insert_one(company_info)
    except pymongo.errors.DuplicateKeyError:
        print("company %s has been inserted" % company_info["basic_info"]["company_name_eng"])





