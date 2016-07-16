import urllib2
import re
import csv

from bs4 import BeautifulSoup

def unescape(s):
	s = s.replace("&amp;","&")
	return s

url = 'http://www.ashp.org/rss/shortages/#current'
req = urllib2.Request(url)
resp = urllib2.urlopen(req)
resp_data = resp.read()

# Use regular expressions to only find drug shortage links
# using ASHP's RSS feed
links = re.findall(r'</title><link>(http://www.ashp.org/menu/DrugShortages/CurrentShortages/Bulletin.*?)</link>',str(resp_data))

for page in links:
    url_page=unescape(page)
    req = urllib2.Request(url_page)
    resp = urllib2.urlopen(req)
    resp_page = resp.read()

    # Import html into BeautifulSoup
    # 'html.parser' is used so Beautiful does not try to add ending tags. Otherwise soup.findAll is affected
    soup = BeautifulSoup(resp_page, 'html.parser')

    # Find all of the affected NDCs using regular expressions
    # #####-####-## (format of a national drug code / NDC) in a 
    # converted string using the HTML tag <span id="whatever">
    affected_ndcs = re.findall(r'NDC (\d\d\d\d\d-\d\d\d\d-\d\d)', \
    str(soup.findAll(id="ctl00_ContentPlaceHolder1_lblProducts")))

    # Find all of the available NDCs using regular expressions
    # #####-####-## (format of a national drug code / NDC) in a 
    # converted string using the HTML tag <span id="whatever">
    available_ndcs = re.findall(r'NDC (\d\d\d\d\d-\d\d\d\d-\d\d)', \
    str(soup.findAll(id="ctl00_ContentPlaceHolder1_lblAvailable")))

    # Find discontinued NDCs using the 'Affected NDCs' portion
    # and regular expressions. Generally on the ASHP website,
    # discontinued NDCs are like '10 mg, 90 count (NDC 63304-0827-90) - discontinued'
    dced_ndcs = re.findall(r'NDC (\d\d\d\d\d-\d\d\d\d-\d\d).*discontinued', \
    str(soup.findAll(id="ctl00_ContentPlaceHolder1_lblProducts")))

    drug_name = re.findall(r'<span id="ctl00_ContentPlaceHolder1_lblDrug">(.*?)</span>', \
    str(soup.findAll(id="ctl00_ContentPlaceHolder1_lblDrug")))
    drug_name[0] = drug_name[0].decode('ascii','ignore').encode('ascii')

    file_name = 'output.csv'
    with open(file_name,'a') as f:
        writer = csv.writer(f,delimiter=',')
        for item in affected_ndcs:
            writer.writerow([drug_name[0],item,'Affected NDC'])
        for item_2 in available_ndcs:
            writer.writerow([drug_name[0],item_2,'Available NDC'])
        for item_3 in dced_ndcs:
            writer.writerow([drug_name[0],item_3,'Discontinued NDC'])
        f.close()

