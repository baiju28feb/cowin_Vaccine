import requests
import json

from datetime import datetime
import pytz

import time
from datetime import datetime, timedelta

print('Starting search for covid vacciantion slots')

age = 52
pincodes = ["679329"]
print_flag = 'Y'
num_days = 2
IST = pytz.timezone('Asia/Kolkata')
actual = datetime.today()
#print(actual)

list_format = [actual + timedelta(days= i) for i in range(num_days)]
#print(list_format)

actual_dates = [i.strftime("%d%m%y") for i in list_format]
#print(actual_dates)

while True:
    counter = 0

    for pincode in pincodes:
        for given_date in actual_dates:
            print(given_date)
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 

            result = requests.get(URL, headers=header)

            #print(result.text)

            if result.ok:
                response_json = result.json()

                flag = False

                if response_json['centers']:
                    if(print_flag.lower() == 'y'):

                        for center in response_json['centers']:
                            #print(center)

                            for session in center['sessions']:
                                if (session['min_age_limit'] <= age and session['available_capacity']>0):
                                    print('pincode:' + pincode)
                                    print("Available on: {}".format(given_date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availability : ", session["available_capacity"])

                                    if(session["vaccine"] != ''):
                                        print("\t vaccine type:", session["vaccine"])
                                        print("\n")

                                        counter += 1
                                else:
                                    pass
                    else:
                        pass
                else:
                    print('No response received!')
    if counter == 0:
        print('No vaccination slot is available', datetime.now(IST))

    else:
        print('Finished Search!')

    dt = datetime.now() + timedelta(minutes = 2)

    while datetime.now() < dt:
        time.sleep(1)

