#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from datetime import datetime, timedelta
import time
from smtplib import SMTP
age = 52
#str12345=input("Enter Pincode : ")
pincodes = ["414106"]
num_days = 2
print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

pin=[]
date=[]
price=[]
c_name=[]
cb=[]
capacity=[]
v_type=[]

while True:
    counter = 0   
    for pincode in pincodes:   
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
            
            result = requests.get(URL, headers=header)

            if result.ok:
                response_json = result.json()
                if response_json["centers"]:
                    if(print_flag.lower() =='y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                    print('Pincode: ' + pincode)
                                    print("Available on: {}".format(given_date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ", session["available_capacity"])
                                    pin.append(pincode)
                                    date.append(given_date)
                                    p=str(center["fee_type"])
                                    price.append(p)
                                    c_name.append(center["name"])
                                    cb.append(center["block_name"])
                                    capacity.append(session["available_capacity"])
                                    
                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                        v_type.append(session["vaccine"])
                                    print("\n")
                                    counter = counter + 1
            
                                        
            else:
                print("No Response!")
                
    if counter==0:
        print("No Vaccination slot available..!")
    else:
        print("Search Completed..!")
        #smtp server ddress of mail provider
        HOST='smtp.gmail.com'
                                        
        #This is TLS
        PORT=587
        SENDER='kirankumarntelkar@gmail.com'
        PASSWORD='Kiran@789'
                                        
        #creating smtp server obj
        server=SMTP(host=HOST,port=PORT)
                                        
        #Connect
        server.connect(host=HOST,port=PORT)
                                        
        #extended hello; like sying hello
        server.ehlo()
        server.starttls()
        server.ehlo()
                                        
        #loggin in
        server.login(user=SENDER, password=PASSWORD)
        str2="\n\nVaccine details :"
        RECIPIENT="shaikhmatin3230@gmail.com"
        pin_len=len(pin)
        for i in range(0,pin_len):
            str2=str2+"\n\nPincode : "+pin[i]+"\nAvailable on : "+date[i]+"\nCenter : "+c_name[i]+", "+cb[i]+"\nPrice : "+price[i]+"\nAvailability : "+str(capacity[i])+"\nVaccine type : "+v_type[i]
 
        MESSAGE="Hurry up..!\nSlot is available for booking on your pincode..!"+str2
        server.sendmail(SENDER,RECIPIENT,MESSAGE)      
        
        print("Email is sent successfully on your registered E-mail..!")


# In[ ]:





# In[ ]:




