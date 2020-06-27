"""
Total of 2037 recommended pitches with 9 pitches per page.
Total pages = 2037/9 = 227

ALGORITHM:

for each page in the 227 pages from the calculation above:
	for each individual information block in the page:
		populate data dictionary
"""

from bs4 import BeautifulSoup
import requests
import json
import pdb

content_urls = list()
data = dict()
counter = 0

def runner():
    page_num = 0
    url = "https://football-technology.fifa.com/en/resource-hub/certified-product-database/playing-surfaces/football-turf/recommended-pitches/"
    
    for num in range(1, 228):
        print("Processing page number ", page_num)
        form_data = { "Page": num }

        req = requests.post(url, form_data)
        soup = BeautifulSoup(req.content, "html.parser")

        divs = soup.find_all("div", {"class": "row row--results"})

        for div in divs:
            a_tags = div.find_all("a", {"class": "button button--arrow button--border" })

            for a_tag in a_tags:
                populate_data(a_tag['href'])

        page_num+= 1

def populate_data(target_url):
    global counter

    data[target_url] = dict()

    
    req = requests.post(target_url)
    soup = BeautifulSoup(req.content, "html.parser")

    h1s = soup.find_all("h1")
    title = h1s[0].contents[0]
    data_rows = soup.find_all("tr")
    data[target_url]['pitch'] = title


    for row in data_rows:
        key = row.th.contents[0]

        if len(row.td.contents) == 0:
            value = "NO_DATA"
        else:
            value = row.td.contents[0].strip()

        if not value:
            value = "NO_DATA"

        data[target_url][key] = value

    print("Processed url number ", counter)
    counter+= 1

def dump_json_to_file():
    with open('result.json', 'w') as fp:
        json.dump(data, fp)

runner()
dump_json_to_file()
