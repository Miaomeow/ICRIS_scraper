#!/usr/bin/env python3

import csv
import subprocess
import os
import json

from datetime import datetime
from pprint import pprint

import pymongo
import pathlib


PATH = os.getcwd()
client = pymongo.MongoClient('localhost', 27017)
companies = client['icris']['companies']

# Create Export and date folder
pathlib.Path(PATH+"/export").mkdir(parents=True, exist_ok=True)
fname = datetime.now().strftime("%Y-%m-%d.%H:%M:%S")
pathlib.Path(PATH+"/export/"+fname).mkdir(parents=True, exist_ok=True)

# Export basic information, name history, registered office, share captial
subprocess.Popen([PATH + '/export.sh', fname])
fname = "export/" + fname + "/"

# Export directors
with open(fname+"directors.csv", 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow([
        "basic_info.cr_no",
        "basic_info.company_name_eng",
        "directors.name_eng",
        "directors.name_chi",
        "directors.HKID",
        "directors.director_type",
        "directors.overseas_passport_no",
        "directors.passport_country"
    ])

    for c in companies.find():

        for item in c["directors"]:
            data = [
                c["basic_info"]["cr_no"],
                c["basic_info"]["company_name_eng"],
                item["name_eng"],
                item["name_chi"],
                item["HKID"],
                item["director_type"],
                item["overseas_passport_no"],
                item["passport_country"]
            ]

            writer.writerow(data)
            

# Export company secretary
with open(fname+"com_sec.csv", 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow([
        "basic_info.cr_no",
        "basic_info.company_name_eng",
        "com_sec.type",
        "com_sec.name_eng",
        "com_sec.name_chi",
        "com_sec.date_of_appointment",
        "com_sec.address",
        "com_sec.note",
        "com_sec.cr_no",
        "com_sec.name_prev",
        "com_sec.surname_eng",
        "com_sec.alias",
        "com_sec.HKID",
        "com_sec.passport_country",
        "com_sec.overseas_passport_no"
    ])

    for c in companies.find():

        for item in c["com_sec"]:
            data = [
                c["basic_info"]["cr_no"],
                c["basic_info"]["company_name_eng"],
                item["type"],
                item["name_eng"],
                item["name_chi"],
                item["date_of_appointment"],
                item["address"],
                item["note"]
            ]
            if item["type"] == "Body Corporate":
                data.append(item['cr_no'])

            else:
                data.extend([
                    "",
                    item["name_prev"],
                    item["surname_eng"],
                    item["alias"],
                    item["HKID"],
                    item["passport_country"],
                    item["overseas_passport_no"]
                ])

            writer.writerow(data)
