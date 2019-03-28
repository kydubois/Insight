import urllib.request, urllib.parse, urllib.error
import requests
import json
import time
import ssl
import sys
import pprint as pp
import csv
import re
from secrets import INuser_pass

tagname = input('input tage name: ' )

insightlyurl = 'https://api.insight.ly/v2.2/Contacts/Search?'


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Openning a new CSV file so we can write in it
fhand = open(tagname + '_ContactEmailListURLS.csv', 'w', newline='',encoding='utf-8')
csvfhand = csv.writer(fhand, delimiter=',')
# We create headers for our new CSV file
csvfhand.writerow(['Hospital','Hospital ID','Contact First Name','Contact Last Name','Contact Role','Contact Email'])

count = 0
with open(tagname + "_OrganizationsListURLs.csv") as fh:
    next(fh)
    for line in fh:
        hosp = line.replace('"','').rstrip("\n")
        print(hosp)

        parms = dict()
        parms['organisation'] = hosp
        parms['brief'] = 'false'
        # parms['skip'] = count
        parms['top'] = 500
        parms['count_total'] = 'true'

        url = insightlyurl + urllib.parse.urlencode(parms, safe='()', quote_via=urllib.parse.quote)
        uh = requests.get(url, auth = INuser_pass)
        # uh = requests.get(url, auth = ('95453022-fd45-4aee-83af-daf8c138a8e9',''))
        print('Retrieving', url)

        try:
            status = uh.status_code
            print("Status Code:", status)
            if status != 200:
                print("==== Successful Response Failed ====")
                print('')
                break
        except:
            print("==== Failure to Retrieve Status ====")
            print('')
            continue

        dumps = uh.headers
        dumps_total = int(dumps["X-Total-Count"])
        print(dumps_total, "Total Available Records")
        print('')

        js = uh.json()

        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

        for r in js:
            # pp.pprint(r)
            # print('')
            first = r["FIRST_NAME"]
            last = r["LAST_NAME"]
            hospID = r["LINKS"][0]["ORGANISATION_ID"]
            role = r["LINKS"][0]["ROLE"]
            try:
                emaillist = list()
                for ro in r["CONTACTINFOS"]:
                    if EMAIL_REGEX.match(ro["DETAIL"]):  # search for email, skip phone numbers
                        email = ro["DETAIL"]
                        emaillist.append(email)
                        print(hosp)
                        print(hospID)
                        print(first)
                        print(last)
                        print(role)
                        print(email)
                        print('')
                        csvfhand.writerow([hosp,hospID,first,last,role,email])
                        continue
                    else:
                        email = ''
                        continue
            except:
                continue

        count +=1

    if (count % 10 == 0):
        print('Pausing for a bit...')
        time.sleep(5)

    print('')
    print(count, "Records written to file.")
    print('')

# cur.close()
fhand.close()
