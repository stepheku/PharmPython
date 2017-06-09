import requests
import re
import csv
from bs4 import BeautifulSoup

ndc_regex_pattern = r'\d{4,5}-\d{3,4}-\d{1,2}'
output_file_name = 'output.csv'

url = 'https://www.ashp.org/rss/shortages/#current'
resp = requests.get(url)
resp_data = resp.content

# Use regular expressions to only find drug shortage links
# using ASHP's RSS feed
links = re.findall(r'<link>https://www.ashp.org.*?Id=(\d{1,})</link>', str(resp_data))

def create_output_file_headers(file_name):
    with open(output_file_name,'w') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerow(['Drug name', 'NDC', 'Category'])
        f.close()

def main():
    for ids in links:
        url_page = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortage-Detail.aspx?id=' + str(ids)
        # Webpage uses redirects now
        resp = requests.get(url_page, allow_redirects=True)
        resp_page = resp.content
    
        # Import html into BeautifulSoup
        soup = BeautifulSoup(resp_page, 'html.parser')
        drug_name = re.findall(r'>(.*?)</span>', str(soup.findAll(id="1_lblDrug")))
        affected_ndcs = re.findall(ndc_regex_pattern, str(soup.findAll(id="1_lblProducts")))
        available_ndcs = re.findall(ndc_regex_pattern, str(soup.findAll(id="1_lblAvailable")))
    
        output_file_name = 'output.csv'
        with open(output_file_name,'a') as f:
            writer = csv.writer(f,delimiter=',')
            for item in affected_ndcs:
                writer.writerow([drug_name[0], item, 'Affected NDC'])
            for item_2 in available_ndcs:
                writer.writerow([drug_name[0], item_2, 'Available NDC'])
            f.close()

if __name__ == '__main__':
    create_output_file_headers(output_file_name)
    main()
