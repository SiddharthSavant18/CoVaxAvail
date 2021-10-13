import requests
from datetime import date
import math
import json
from twilio.rest import Client
import time

while True:
    today = date.today()
    d1 = today.strftime("%d-%m-%y")

    print("Distrct ID")
    dist_id = int(input())
    print("Distrct ID:" ,dist_id)

    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={0}&date={1}'.format(dist_id,d1)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    x = requests.get(url, headers=headers)
    data = x.json()

    cnt = 1
    AllCentresFor18=[]

    for d in data["centers"]:
        for s in d["sessions"]:
            centre_detail = "Centre {0}:".format(cnt) + "\nCentre Address:" +d['name']+"," + d["address"] + "\nVaccine: " + s['vaccine'] + "\nAvailable Capacity dose 1: " + str(s["available_capacity_dose1"]) + "\nAvailable Capacity dose 2: " + str(s["available_capacity_dose2"]) + '\n' + "\nFor Age Limit: " + str(s["min_age_limit"]) + '\n'
            if(s["min_age_limit"] == 18  and s["available_capacity_dose1"] > 0): #and s["available_capacity_dose2"] > 0 ):
                AllCentresFor18.append(centre_detail)
            else:
                continue
        centre_detail=''
        cnt=cnt+1

    if(len(AllCentresFor18)==0):
        print("Vaccine for 18+ is not available currently for next 7days!")
    else:
        print("Vaccine for 18+ is available....Get it Now!")

    messageFor18 = ""

    if len(AllCentresFor18) >0:
        messageFor18 = messageFor18 + "Available  vaccination centres for 18+:\n\n"
        for mess in  AllCentresFor18:
            messageFor18 = messageFor18 + mess
            messageFor18 = messageFor18 + "\n"
            print(messageFor18)

    else:
        messageFor18 = messageFor18 + "No Vaccine slot available for 18 and above age currently for next 7days"
        print(messageFor18)

    if(len(AllCentresFor18) > 0):
       account_sid = 'add Acc Key'
       auth_token = 'add token'

       client = Client(account_sid, auth_token)

       message = client.messages \
                   .create(
       to= 'add Receiver mobile number',
       from_= 'add Sender twilio contact number',
       body= messageFor18,
    )

    time.sleep(60)