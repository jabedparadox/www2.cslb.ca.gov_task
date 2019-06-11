#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/env python
#!/usr/bin/env python3
# -*- coding: utf8 -*-

# https://www2.cslb.ca.gov/
# date                 :- 11/06/2019
# author               :- Md Jabed Ali(jabed)

import warnings
warnings.simplefilter("ignore", UserWarning)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import random
from json import loads
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import argparse
import re
#import aiohttp
#import async_timeout
#from aiohttp import web
import csv
from json import loads
import json
import argparse
import os
import sys
import time
from datetime import datetime
#from google.cloud import translate

# different headers.
def random_useragent():
    #http://useragentstring.com/pages/useragentstring.php
    url = "https://fake-useragent.herokuapp.com/browsers/0.1.8"
    r = requests.get(url)
    randomuseragent = loads(r.text)['browsers']
    #print(random.choice(randomuseragent[random.choice(list(randomuseragent))]))
    return random.choice(randomuseragent[random.choice(list(randomuseragent))])

#u_a = random_useragent()

# user agent.
headers = {#'User-Agent': u_a,
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
           #':authority': '',
           #':scheme': 'https',
           'X-Requested-With': 'XMLHttpRequest',
           'Upgrade-Insecure-Requests': '1',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,application/json,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           #'Origin': ' ',
           #'Host': ' ',
}

#options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')
#selenium_chrome_driver_path = ""
#driver = webdriver.Chrome(chrome_options = options, executable_path = selenium_chrome_driver_path)

#brwsr = webdriver.Chrome()
#brwsr = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
#brwsr.set_window_size(1024, 768) # Resizing the window.(default)
#brwsr.get("")
#brwsr.save_screenshot('')

licenceno = []
HISLicNum = []
var = []

# for next page.
def nextpage(a):
    #var.clear()
    #del var[:]
    var1 = re.findall('Contractor Name</td><td>(.*?)<', str(a), re.DOTALL)[-1]
    var2 = re.findall('License</td><td><a href="LicenseDetail.aspx\?LicNum=(.*?)"', str(a), re.DOTALL)[-1]
    #while True:

# remove log file.
if os.path.exists("ghostdriver.log"):
    try:
        os.remove("ghostdriver.log")
    except OSError:
        pass

# remove templicencefile.txt if exist.
if os.path.exists("templicencefile.txt"):
    with open("templicencefile.txt") as f:
        for row in f:
            licenceno.append(row.split()[0])
else:
  print("The File Does Not Exists. Make Sure \"templicencefile.txt\" Is On This/Working Directory/Folder.")

# searh by licenceno for salesperson list/HISLicNum.
def contractorhissearch(HISLicNum_func):
    print ('Total ' + str(len(licenceno)) + " License Found In \"templicencefile.txt\" ."  + '\n')
    e = 0
    for HISLic  in HISLicNum_func:
        e+=1
        print (str(e) + ". Collect Contractor's License Detail (Salesperson List) For This License " + HISLic + '.')
        hisurl = 'https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ContractorHISList.aspx?LicNum=' + HISLic
        #brwsr = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        #brwsr.get(url)
        #hisres = str(brwsr.page_source)
        try:
            hisres = requests.get(hisurl, headers=headers).text
        except:
            hisres = 'n/a'
        hislicenceno = list((re.findall('href="HisDetail.aspx\?HISLicNum=(.*?)"', str(hisres), re.DOTALL)))
        HISLicNum.append(hislicenceno)
        try:
            nxtpage = re.findall('class="onlineServicesButton"', str(hisres), re.DOTALL)
        except:
            nxtpage = 'n/a'
        #time.sleep()
        #while len((hislicenceno)) == 0:
        if 'href="HisDetail.aspx?HISLicNum=' not in str(hisres):
            print ('   No Contractor\'s License Detail (Salesperson List) Found For This License ' + HISLic + '.' + '\n')
            #break
        pagecount = 0
        f = 0
        while len((nxtpage)) > 0:
            pagecount+=50
            f+=1
            print ('   ' + str(f) + '. Next ' + str(pagecount) + ' Records ▶.')
            hisurl_nxt = 'https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ContractorHISList.aspx?LicNum=' + str(HISLic) + '&LicName=&BlockStartsAt=' + str(pagecount)
            try:
                hisres_nxt = requests.get(hisurl_nxt, headers=headers).text
            except:
                hisres_nxt = 'n/a'
            hislicenceno = list((re.findall('href="HisDetail.aspx\?HIS(.*?)"', str(hisres_nxt), re.DOTALL)))
            HISLicNum.append(hislicenceno)
            if 'class="onlineServicesButtonInvisible"' in str(hisres_nxt):
              break  
    return hislicenceno

contractorhissearch(licenceno)

HISLicNum = str(HISLicNum).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',')
HISLicNum = list(set(re.findall('LicNum=(.*?)\'', str(HISLicNum), re.DOTALL)))
print ('Total ' + str(len(HISLicNum)) + ' Unique HIS Registration Found.')

# searh by his licence number.
#def licencesearch(licencenumber=None):
def salesperson_information(his_search):
    #his_search = str(his_search).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',')
    #while len((licence)) != 0:
    datestring = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    outputFile1 = open('2_New_Salesperson_File_' + datestring + '.csv', 'w', newline='', encoding="utf8")
    outputFile2 = open('3_New_Salesperson_To_Contractor_' + datestring + '.csv', 'w', newline='', encoding="utf8")
    outputWriter1 = csv.writer(outputFile1)
    outputWriter2 = csv.writer(outputFile2)
    outputWriter1.writerow(["Name", "Address", "City", "State", "Zip", "Phone", "His_Number", "Issue_Date", "Expire_Date", "Status"])
    outputWriter2.writerow(["His_Regumber", "Contractor_Licence", "Effective_Start_Date", "Effective_End_Date"])
    e = 0
    for i in his_search:
        e+=1
        print ('Collect Registration Detail From His Licence Number : ' + str(e) + '. ' + '(' + str(i).replace('&amp;HISLmfPre=', ' ') + ')')
        HisDetailurl = 'https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/HisDetail.aspx?HISLicNum=' + str(i).replace('amp;', '') #&HISLmfPre=SP
        try:
            HisDetailres = requests.get(HisDetailurl, headers=headers).text
        except:
            HisDetailres = 'n/a'
        try:
            soup = BeautifulSoup(HisDetailres, 'html.parser')
        except:
            soup = 'n/a'
        #results = str(soup.find_all('td', {'class' : 'centerContent'})[0]).split('<br/>')
        #name = str(results[0]).replace('<td class="centerContent" colspan="2" id="ctl00_LeftColumnMiddle_BusInfo">', '')
        try:
            name = soup.find_all('td', {'id' : 'ctl00_LeftColumnMiddle_HISName'})[0].text
        except:
            name = 'n/a'
        try:
            address = soup.find_all('td', {'id' : 'ctl00_LeftColumnMiddle_Address1'})[0].text
        except:
            address = 'n/a'
        try:
            city = str(soup.find_all('td', {'id' : 'ctl00_LeftColumnMiddle_CityStateZip'})[0].text).split(',')[0]
        except:
            city = 'n/a'
        try:
            state = str(soup.find_all('td', {'id' : 'ctl00_LeftColumnMiddle_CityStateZip'})[0].text).split(' ')[-2]
        except:
            state = 'n/a'
        try:
            zip = str(soup.find_all('td', {'id' : 'ctl00_LeftColumnMiddle_CityStateZip'})[0].text).split(' ')[-1]
        except:
            zip = 'n/a'
        try:
            phone = soup.find_all('td', {'id' : 'ctl00_LeftColumnMiddle_PhoneNumber'})[0].text
        except:
            phone = 'n/a'
        try:
            his_num = re.findall('ctl00_LeftColumnMiddle_HIS_No">(.*?)<', str(soup), re.DOTALL)[0]
        except:
            his_num = 'n/a'
        try:
            IssDt = re.findall('ctl00_LeftColumnMiddle_issueDate">(.*?)<', str(soup), re.DOTALL)[0]
        except:
            IssDt = 'n/a'
        try:
            ExpDt = re.findall('ctl00_LeftColumnMiddle_expirationDate">(.*?)<', str(soup), re.DOTALL)[0]
        except:
            ExpDt = 'n/a'
        try:
            RegStatus = soup.find_all('td', {'id' : 'ctl00_LeftColumnMiddle_RegStatus'})[0].text
        except:
            RegStatus = 'n/a'
        #print (name,address,city,state,zip,phone,his_num,IssDt,ExpDt,RegStatus)
        try:
            detail = soup.find_all('blockquote')[1:]
        except:
            detail = 'n/a'
        for details in detail:
            try:
                His_Regumber_2nd = re.findall('ctl00_LeftColumnMiddle_HIS_No">(.*?)<', str(soup), re.DOTALL)[0] # his_num
            except:
                His_Regumber_2nd = 'n/a'
            try:
                Contractor_Licence_2nd = re.findall('LicenseDetail.aspx\?LicNum=(.*?)"', str(details), re.DOTALL)[0]
            except:
                Contractor_Licence_2nd = 'n/a'
            
            #Status2nd =
            try:
                Effective_Start_Date_2nd = re.findall('Effective Date:</strong>(.*?)<', str(details).replace('Effective Dates:</strong>', 'Effective Date:</strong>'), re.DOTALL)[0]
            except:
                Effective_Start_Date_2nd = 'n/a'
            try:
                Effective_End_Date_2nd = Effective_Start_Date_2nd.split('-')[1]
            except:
                Effective_End_Date_2nd = 'n/a'

            outputWriter2.writerow([His_Regumber_2nd,Contractor_Licence_2nd,Effective_Start_Date_2nd,Effective_End_Date_2nd])
        #outputFile2.close()
        outputWriter1.writerow([name,address,city,state,zip,phone,his_num,IssDt,ExpDt,RegStatus])
    outputFile1.close()
    outputFile2.close()
    return

            
    '''if 'Business Phone Number' in str(results):
            phone = str(results[-3])
        else:
            phone = 'n/a'
        if 'DBA' in results[1].upper():
            dba = results[1]
        else:
            dba = 'n/a'
        if 'DBA' in str(results).upper():
            address = results[3]
        else:
            address = results[1]
        if 'DBA' in str(results).upper():
            city = str(results[4]).split(',')[0]
            state = str(results[4]).split(' ')[-2]
            zip = str(results[4]).split(' ')[-1]
        else:
            city = str(results[2]).split(',')[0]
            state = str(results[2]).split(' ')[-2]
            zip = str(results[2]).split(' ')[-1]
        his_num = re.findall('ctl00_LeftColumnMiddle_HIS_No">(.*?)<', str(soup), re.DOTALL)[0]
        IssDt = re.findall('ctl00_LeftColumnMiddle_issueDate">(.*?)<', str(soup), re.DOTALL)[0]
        ExpDt = re.findall('ctl00_LeftColumnMiddle_expirationDate">(.*?)<', str(soup), re.DOTALL)[0]
        
        print (i,name,phone,dba,address,city,state,zip,his_num,IssDt,ExpDt)
        
        time.sleep(100000)
        #outputWriter.writerow([i,name,phone,dba,address,city,state,zip,IssDt,ExpDt])
    #outputFile.close()
    '''   
    
salesperson_information(HISLicNum)    
print ('Done.')
input("Press Enter To Exit.")

