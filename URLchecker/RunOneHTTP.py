import json
import urllib.request, urllib.parse, urllib.error
import requests
import ssl
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

# create a new CSV file
fhand = open(tagname + '_OrganizationsList_with_Emails_and_URLs.csv', 'w', newline='', encoding='utf-8')
csvfhand = csv.writer(fhand)
csvfhand.writerow(['Hospital','Hospital ID','Hospital Email','Hospital URL'])


count = 0
while True:


    parms = dict()
    parms['tag'] = tagname
    parms['skip'] = count
    parms['top'] = 500
    parms['count_total'] = 'true'

    url = insightlyurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)

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
    URL_REGEX = re.compile(r"(http:\/\/www\.|http:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")

    for item in data:
        # pp.pprint(item)
        # print('')
        # hospname = str(item['ORGANISATION_NAME'].encode('utf-8'))
        # hospname = hospname[2:-1]
        hospname = item["ORGANISATION_NAME"]
        hospID = item['ORGANISATION_ID']

        # print('length of tags ',len(item['TAGS'])


        for u in item["CONTACTINFOS"]:
            if URL_REGEX.match(u["DETAIL"]):
                url = u["DETAIL"]
            else:
                url = ''
                continue

        # print('length of CUSTOMFIELDS ',len(item['CUSTOMFIELDS']))
        # emaillist = list()
        for r in item["CUSTOMFIELDS"]:
            if EMAIL_REGEX.match(r["FIELD_VALUE"]):  # search for email, skip phone numbers
                # email = str(r["FIELD_VALUE"].encode('utf-8'))
                # email = email[2:-1]
                email = r["FIELD_VALUE"]
                # emaillist.append(email)
                try:
                    print(hospname)
                    print(hospID)
                    print(email)
                    print(url)
                    csvfhand.writerow([hospname,hospID,email,url])
                except:
                    continue
                continue
            else:
                email = ''
                continue

        #write hospital name and email to csv
        # csvhosphand.writerow([hospname])
        # csvIDhand.writerow([hospname,hospID])
        count += 1

    if count % 2 == 0:
        print('Compiling Data...')
        print(count)
        time.sleep(5)


    if count == dumps_total:
        print("Total of",count, "records written to file.")
        break

# cur.close()
fhand.close()
# hosphand.close()
# IDhand.close()
