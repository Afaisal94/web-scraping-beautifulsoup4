from bs4 import BeautifulSoup
import requests
import math
import csv
import json

data_csv = []
data_json = []

def get_total_pages():
    url = 'https://www.indeed.com/jobs?'
    params = {
        'q': 'web',# Keyword
        'l': 'new york state',# Location
        'vjk': '7867bce2090b7abf'
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    }
    res = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    contents = soup.find(attrs={'id': 'searchCountPages'}).text.replace(' ', '').replace('Page1of', '').replace('jobs', '').replace(',', '')
    count = int(contents)
    pages = math.ceil(count/15) # total data / data per page (15)
    return pages

def get_data_index():
    url = 'https://www.indeed.com/jobs?'
    params = {
        'q': 'web',# Keyword
        'l': 'new york state',# Location
        'vjk': '7867bce2090b7abf'
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    }
    res = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    contents = soup.find_all(attrs={'class': 'job_seen_beacon'})

    for item in contents:
        title = item.find(attrs={'class': 'jobTitle'}).text
        company = item.find(attrs={'class': 'companyName'}).text
        location = item.find(attrs={'class': 'companyLocation'}).text
        date = item.find(attrs={'class': 'date'}).text.replace("Posted", "")
        # CSV
        content_csv = [title, company, location, date]
        data_csv.append(content_csv)
        # JSON
        content_json = {
            "title": title,
            "company": company,
            "location": location,
            "post_date": date
        }
        data_json.append(content_json)

total_pages = get_total_pages()

def get_data_paging():
    for x in range(total_pages):
        start = x * 10
        url = 'https://www.indeed.com/jobs?'
        params = {
            'q': 'web',# Keyword
            'l': 'new york state',# Location
            'start': start,# Paging
            'vjk': '7867bce2090b7abf',
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        }
        res = requests.get(url, params=params, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        contents = soup.find_all(attrs={'class': 'job_seen_beacon'})

        for item in contents:
            title = item.find(attrs={'class': 'jobTitle'}).text
            company = item.find(attrs={'class': 'companyName'}).text
            location = item.find(attrs={'class': 'companyLocation'}).text
            date = item.find(attrs={'class': 'date'}).text.replace("Posted", "")
            # CSV
            content_csv = [title, company, location, date]
            data_csv.append(content_csv)
            # JSON
            content_json = {
                "title": title,
                "company": company,
                "location": location,
                "post_date": date
            }
            data_json.append(content_json)

def storing_csv():
    with open('data.csv', mode='w', newline='') as csv_file:
        # Create object
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write
        writer.writerow(["JOB TITLE", "COMPANY NAME", "LOCATION", "DATE POSTED"])

        for d in data_csv:
            writer.writerow(d)

    print("Writing to CSV has been successful !")

def storing_json():
    # Serializing json
    json_object = json.dumps(data_json, indent=4)

    # Writing to sample.json
    with open("data.json", "w") as outfile:
        outfile.write(json_object)

    print("Writing to JSON has been successful !")

get_data_index()
get_data_paging()
storing_csv()
storing_json()