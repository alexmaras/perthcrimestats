import json
import urllib.request
from bs4 import BeautifulSoup

url = "https://www.police.wa.gov.au/Crime/Crime-Statistics-Portal/Statistics?"

args = {}
args['start_year'] = "1999"
args['startMonth'] = "1"
args['endYear'] = "2017"
args['endMonth'] = "12"

suburb_file = open("suburbs",'r')
suburb_list = suburb_file.read().splitlines()

suburb_crime_data = []

for suburb in suburb_list:
    print("getting " + suburb)
    args['locality'] = suburb

    tmp_url = url
    first = True
    for key,val in args.items():
        if first:
            first = False
        else:
            tmp_url += "&"
        tmp_url += key + "=" + val.replace(' ', '%20')

    print(tmp_url)
    with urllib.request.urlopen(tmp_url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html5lib")
        table = soup.find("table")
        headings = [th.get_text() for th in table.find("tr").find_all("th")]
        
        datasets = []
        for row in table.find_all("tr")[1:-1]:
            dataset = dict(zip(headings, (td.get_text() for td in row.find_all('td'))))
            dataset["suburb"] = suburb
            datasets.append(dataset)

        suburb_crime_data.append(datasets)

with open('output_suburbs.json', 'w') as f:
    json.dump(suburb_crime_data, f)
