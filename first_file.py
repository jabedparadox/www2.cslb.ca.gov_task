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
import multiprocessing
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
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
           #':authority': '',
           #':scheme': 'https',
           'X-Requested-With': 'XMLHttpRequest',
           'Upgrade-Insecure-Requests': '1',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,application/json,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           #'Origin': ' ',
           #'Host': ' ',
}

#browser = webdriver.Chrome()
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

# command line arguments.
parser = argparse.ArgumentParser()

licence = []
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
    try:
        os.remove("templicencefile.txt")
    except OSError:
        pass

# searh by name. eg: VIVINT, SUNPOWER etc.
def namesearch(inputtext=None, pagecount=None):
    tblsrch = inputtext.split(' ')[0]
    print ('Collect All Unique License & Business Information For ' + str(inputtext)+ '.')
    url = 'https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/NameSearch.aspx?NextName=' + inputtext
    brwsr = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe') # path where phantomjs.exe located.
    try:
        brwsr.get(url)
    except:
        pass
    try:
        res = str(brwsr.page_source)
        #res = requests.get(url, headers=headers).text
    except:
        res = 'n/a'
    soupnxtpage_a = BeautifulSoup(res, 'html.parser')
    try:
        table_a = soupnxtpage_a.find_all('tr')
    except:
        table_a = 'n/a'
    for tabledata_a in table_a:
        #while len((re.findall(tblsrch, str(tabledata_a), re.DOTALL))) > 0:
        if tblsrch in str(tabledata_a):
            licenceno = list(set(re.findall('LicenseDetail.aspx\?LicNum=(.*?)"', str(tabledata_a), re.DOTALL)))
            licence.append(licenceno)
    #var1 = re.findall('Contractor Name</td><td>(.*?)<', str(res), re.DOTALL)[-1]
    #var2 = re.findall('License</td><td><a href="LicenseDetail.aspx\?LicNum=(.*?)"', str(res), re.DOTALL)[-1]
    #licenceno = list(set(re.findall('LicenseDetail.aspx\?LicNum=(.*?)"', str(res), re.DOTALL)))
    #licence.append(licenceno)
    nxtpage = re.findall('>Next 50 Business (.*?)\&', str(res), re.DOTALL)
    d = 0
    while len((nxtpage)) > 0:
        d+=1
        print (str(d) + '. Next 50 Business Names.')
        try:
            brwsr.find_element_by_id('ctl00_LeftColumnMiddle_NextLicenses').click()
        except:
            pass
        #nxtpageurl = str('https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/NameSearch.aspx?NextName=' + var1 + '%27&NextLicNum=' + var2).replace(' ', '+')
        #nxtpageurlres = requests.get(nxtpageurl, headers=headers).text
        try:
            nxtpageurlres = str(brwsr.page_source)
        except:
            nxtpageurlres = 'n/a'
        
        soupnxtpage = BeautifulSoup(nxtpageurlres, 'html.parser')
        #table = soupnxtpage.find_all('table', {'id' : 'ctl00_LeftColumnMiddle_Table1'})
        try:
            table = soupnxtpage.find_all('tr')
        except:
            table = 'n/a'
        for tabledata in table:
            #while len((re.findall(tblsrch, str(tabledata), re.DOTALL))) > 0:
            if tblsrch in str(tabledata):
            #licenceno =  str(re.findall('LicenseDetail.aspx\?LicNum=(.*?)"', str(tabledata), re.DOTALL)) + '~' + str(re.findall('Status</td><td class="(.*?)<', str(tabledata), re.DOTALL))
                licenceno = list(set(re.findall('LicenseDetail.aspx\?LicNum=(.*?)"', str(tabledata), re.DOTALL)))
                licence.append(licenceno)
        if 'value="Next 50 Business Names' not in nxtpageurlres:
        #while len((re.findall('value="Next 50 Business Names (.*?)>', str(nxtpageurlres), re.DOTALL))) == 0:
            os.system("taskkill /im phantomjs.exe")
            #os.system("taskkill /im chromedriver.exe")
            #os.system("taskkill /im chrome.exe")
            break
        if d == pagecount:
            break
    return licenceno

#namesearch(sys.argv[1:])
namesearch('VIVINT', 2)

licence = str(licence).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',')
licence = list(set([x for x in licence if len(x.strip()) > 0]))
print ('Total ' + str(len(licence)) + ' Unique Business Bames & Licence Found.')

# save licence to templicencefile.txt.
for temporarylicence in licence:
    with open('templicencefile.txt', 'a') as templicencefile:
        templicencefile.write(temporarylicence + "\n")
        templicencefile.close()

# search by licence.
#def licencesearch(licencenumber=None):
def licencesearch(licence_search):
    licence_search = str(licence_search).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',')
    #while len((licence)) != 0:
    datestring = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    outputFile = open('1_New_Contractor_File_' + datestring + '.csv', 'w', newline='', encoding="utf8")
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(["Licence", "Name", "Phone", "Dba", "Address", "City", "State", "Zip", "Issue_Date", "Expire_Date"])
    e = 0
    for i in licence_search:
        e+=1
        print (str(e) + '. Collect New Contractor Inrormation From Licence : ' + '(' + str(i) + ')')
        licenceurl = 'https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=' + i
        try:
            licenceres = requests.get(licenceurl, headers=headers).text
        except:
            licenceres = 'n/a'
        soup = BeautifulSoup(licenceres, 'html.parser')
        try:
            results = str(soup.find_all('td', {'class' : 'centerContent'})[0]).split('<br/>')
        except:
            results = 'n/a'
        try:
            name = str(results[0]).replace('<td class="centerContent" colspan="2" id="ctl00_LeftColumnMiddle_BusInfo">', '')
        except:
            name = 'n/a'
        try:
            if 'Business Phone Number' in str(results):
                phone = str(results[-3]).replace('Business Phone Number:', '')
            else:
                phone = 'n/a'
        except:
            phone = 'n/a'
        try:
            if 'DBA' in results[1].upper():
                dba = results[1]
            else:
                dba = 'n/a'
        except:
            dba = 'n/a'
        try:
            if 'DBA' in str(results).upper():
                address = results[3]
            else:
                address = results[1]
        except:
            address = results[1]
        try:
            if 'DBA' in str(results).upper():
                city = str(results[4]).split(',')[0]
                state = str(results[4]).split(' ')[-2]
                zip = str(results[4]).split(' ')[-1]
            else:
                city = str(results[2]).split(',')[0]
                state = str(results[2]).split(' ')[-2]
                zip = str(results[2]).split(' ')[-1]
        except:
            city = str(results[2]).split(',')[0]
            state = str(results[2]).split(' ')[-2]
            zip = str(results[2]).split(' ')[-1]
        try:
            IssDt = re.findall('IssDt">(.*?)<', str(soup), re.DOTALL)[0]
        except:
            IssDt = 'n/a'
        try:
            ExpDt = re.findall('ExpDt" style="font-weight\:bold\;">(.*?)<', str(soup), re.DOTALL)[0]
        except:
            ExpDt = 'n/a'
        #if 'This license is current and active.' in str(soup):
            #stasus = 'ACTIVE'
        #with open('templicencefile.txt', 'a') as templicencefile:
            #templicencefile.write(i + "\n")
            #templicencefile.write(i + "~" + name + "~" + phone)
            #templicencefile.close()
        outputWriter.writerow([i,name,phone,dba,address,city,state,zip,IssDt,ExpDt])
    outputFile.close()
    return

# for multi pool.
def start():
    with multiprocessing.Pool(processes=5) as p:
        p.map_async(licencesearch, licence)

#if __name__=='__main__':
licencesearch(licence)    
print ('Done. Please Check Most Recent "1_New_Contractor_File_ CSV" File & Don\'t Delete "templicencefile.txt" File Before Completing Full Task. ')
input("Press Enter To Exit.")



'''if __name__=='__main__':
    func = licencesearch
    pool = multiprocessing.Pool(4)
    pool.map_async(func, licence)
    pool.close()
    pool.join()
#licencesearch(licence)    
print ('Done.')'''                  

'''def parsing(url):
    driver = webdriver.Chrome()
    driver.set_page_load_timeout()
    driver.get(url)
    text = driver.page_source
    driver.close()
    return text

list = ['', '']
pool = Pool(processes=)
pool.map(parsing, list)'''

