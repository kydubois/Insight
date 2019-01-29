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
from secrets import INuser_pass

tagname = input('input tag name: ')

insightlyurl = 'https://api.insight.ly/v2.2/Organisations/Search?'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

db = sqlite3.connect(tagname + '_Orgs.sqlite')  # Make sure to update to new SQL database
cur = db.cursor()

# Create a new database
cur.execute('''
DROP TABLE IF EXISTS Orgs;''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Orgs (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    hospital_ID TEXT,
    hospital TEXT
);
''')
#
# # create a new CSV file
fhand = open(tagname + '_OrgsList_with_Emails.csv', 'wb+', newline='')
csvfhand = csv.writer(fhand)
csvfhand.writerow(['Hospital','Hospital Email','Hospital ID'])

hosphand = open(tagname + '_OrgsList.csv', 'wb+', newline='')
csvhosphand = csv.writer(hosphand)
csvhosphand.writerow(['Hospital'])

IDhand = open(tagname + '_OrgnizationsList_with_IDs.csv', 'w', newline='', encoding='utf-8')
csvIDhand = csv.writer(IDhand)
csvIDhand.writerow(['Hospital', 'Hospital ID'])

count = 0
while True:


    parms = dict()
    parms['tag'] = tagname
    parms['skip'] = count
    parms['top'] = 500
    parms['count_total'] = 'true'

    url = insightlyurl + urllib.parse.urlencode(parms)

    print(url)

    uh = requests.get(url, auth = INuser_pass)

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

        # print('length of tags ',len(item['TAGS']))
        taglist = list()
        for i in item['TAGS']:
            tag = i['TAG_NAME']
            # print(tag)
            taglist.append(tag)

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
                    csvfhand.writerow([hospname,hospID,email])
                except:
                    continue
            else:
                email = ''
                continue


        cur.execute('''INSERT INTO Orgs (hospital_D, hospital)
            VALUES ( ?, ?, ? );''', (str(hospID), str(hospname) ) )
        db.commit()

        #write hospital name and email to csv
        csvhosphand.writerow([hospname])
        csvIDhand.writerow([hospname,hospID])
        count +=1

    if count % 10 == 0:
        print('Compiling Data...')
        time.sleep(5)


    if count == dumps_total:
        print("Total of",count, "records written to database.")
        break

cur.close()
fhand.close()
hosphand.close()
IDhand.close()
