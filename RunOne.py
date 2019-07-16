import json
import urllib.request, urllib.parse, urllib.error
import requests
import ssl
import sqlite3
import time
import sys
import codecs
import csv
import pprint as pp
import re

tagname = input('input tag name: ')

insightlyurl = 'https://api.insight.ly/v3.1/Organisations/SearchByTag?'

with open('credentials.json', 'rb') as creds:
    credentials = json.load(creds)

    api_key = credentials['key'].encode('utf-8')
    api_secret = credentials['secret'].encode('utf-8')
    api_auth = api_key,api_secret

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# # create a new CSV file
fhand = open(tagname + '_OrganizationsList_with_Emails.csv', 'wb+', newline='')
csvfhand = csv.writer(fhand)
csvfhand.writerow(['Hospital','Hospital ID','State','Zip','Hospital Email'])

count = 0
while True:


    parms = dict()
    parms['tagName'] = tagname
    parms['skip'] = count
    parms['top'] = 500
    parms['count_total'] = 'true'

    url = insightlyurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)

    uh = requests.get(url, auth = api_auth)

    try:
        status = uh.status_code
        print("Status Code:", status)
        if status != 200:
            print("==== Successful Response Failed ====")
            break
    except:
        print("==== Failure to Retrieve Status ====")
        continue

    dumps = uh.headers
    dumps_total = int(dumps["X-Total-Count"])

    data = uh.json()  # this is a list

    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    for item in data:
        # pp.pprint(item)
        # print('')
        # hospname = str(item['ORGANISATION_NAME'].encode('utf-8'))
        # hospname = hospname[2:-1]
        hospname = item['ORGANISATION_NAME']
        hospID = item['ORGANISATION_ID']
        state = item["ADDRESS_SHIP_STATE"]
        zipCode = item["ADDRESS_SHIP_POSTCODE"]

        # print('length of CUSTOMFIELDS ',len(item['CUSTOMFIELDS']))
        emaillist = list()
        for r in item["CUSTOMFIELDS"]:
            if EMAIL_REGEX.match(r["FIELD_VALUE"]):  # search for email, skip phone numbers
                # email = str(r["FIELD_VALUE"].encode('utf-8'))
                # email = email[2:-1]
                email = r["FIELD_VALUE"]
                emaillist.append(email)
                print(hospname)
                print(hospID)
                print(email)
                try:
                    csvfhand.writerow([hospname,hospID,state,zipCode,email])
                except:
                    continue
                continue
            else:
                email = ''
                continue

        #write hospital name and email to csv
        count +=1

    if count % 2 == 0:
        print('Compiling Data...')
        time.sleep(5)


    if count == dumps_total:
        print("Total of",count, "records written to database.")
        break

fhand.close()

