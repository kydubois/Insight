import urllib.request, urllib.parse, urllib.error
import requests
import json
import time
import ssl
import sys
import pprint as pp
import csv
import re

tagname = input('input tage name: ' )

insightlyurl = 'https://api.insight.ly/v3.1/Contacts/Search?'

with open('credentials.json', 'rb') as creds:
    credentials = json.load(creds)

    api_key = credentials['key'].encode('utf-8')
    api_secret = credentials['secret'].encode('utf-8')
    api_auth = api_key,api_secret

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Openning a new CSV file so we can write in it
fhand = open(tagname + '_ContactEmailList.csv', 'w', newline='', encoding='utf-8')
csvfhand = csv.writer(fhand, delimiter=',')
# We create headers for our new CSV file
csvfhand.writerow(['Hospital ID','Contact First Name','Contact Last Name','Contact Role','Contact Email'])

count = 0
with open(tagname + "_OrganizationsList_with_Emails.csv") as fh:
    reader = csv.DictReader(fh)
    for line in fh:
        hospID = line["Hospital ID"]
        print(hospID)

        parms = dict()
        parms['field_name'] = 'ORGANISATION_ID'
        parms['field_value'] = hospID
        parms['brief'] = 'false'
        # parms['skip'] = count
        parms['top'] = 500
        parms['count_total'] = 'true'

        url = insightlyurl + urllib.parse.urlencode(parms, safe='()', quote_via=urllib.parse.quote)
        uh = requests.get(url, auth = api_auth)
        
        print('Retrieving', url)

        try:
            status = uh.status_code
            # print("Status Code:", status)
            if status != 200:
                print("==== Successful Response Failed ====")
                print(uh.raise_for_status())
                print('')
                break
        except:
            print("==== Failure to Retrieve Status ====")
            print('')
            continue

        dumps = uh.headers
        dumps_total = int(dumps["X-Total-Count"])
        print('dumps_total, "Total Available Records")
        print('')

        js = uh.json()
              
        pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(js)

        for r in js:
            # pp.pprint(r)
            # print('')
            first = r["FIRST_NAME"]
            last = r["LAST_NAME"]
            orgID = r["ORGANISATION_ID"]
            role = r["TITLE"]
            email = r["EMAIL_ADDRESS"]
            print(first, last)
            print(orgID)
            print(role)
            print(email)
            print('')
            csvfhand.writerow([orgID,first,last,role,email])
            count +=1

        if count % 10 == 0 :
            print('Pausing for a bit...')
            time.sleep(5)

        print('')
        print(count, "Records written to file.")
        print('')

fhand.close()
