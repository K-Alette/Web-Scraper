#Kodi Lein
#CYBR-260-45
#8/20/2021
#This program is a web scraper that pulls job data from
#indeed.com and parses it. It then writes the information
#into a CSV file so the user can view it.
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

#function: getURL
#purpose: get the URL to pull data from
#input: positiona and location for job search
#return: URL
def getURL(position, location):
    #generate url from position and location
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    print(url)
    return url

#function: get_record
#purpose: pulls data from URL using HTML tags
#input: none
#return: job data as "record"
def get_record(card):
    # get position
    try:
        job_title = card.h2.text.strip().lstrip('new')
    except AttributeError:
        job_title = ''
    # get company
    try:
        company = card.find('span', class_='companyName').text.strip()
    except AttributeError:
        company = ''
    # get url
    try:
        atag = card.find('a')
        job_url = 'https://www.indeed.com' + atag.get('href')
    except AttributeError:
        job_url = ''
    # get job location
    try:
        job_loc = card.find('div', class_='companyLocation').text.strip()
    except AttributeError:
        job_loc = ''
    # get summary
    try:
        jd = card.find('div', class_='job-snippet').text.strip('\n')
    except AttributeError:
        jd = ''
    # get salary
    try:
        salary = card.find('span', class_='salary-snippet').text
    except AttributeError:
        salary = ''
    # get post date
    try:
        post_date = card.find('span', class_='date').text.strip()
    except AttributeError:
        post_date = ''
    today = datetime.today().strftime('%Y-%m-%d')

    record = (job_title, company, job_loc, jd, post_date, today, salary, job_url)

    return record

#function: main
#purpose: main driver - parse HTML and write to CSV file
#input: position and location of job
#return: records (parsed job data from HTML code)
def main(position, location):
    records = []
    url = getURL(position, location)

    #while valid URL, gather data
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_ = 'slider_container')

        #get records for each listing
        for card in cards:
            record = get_record(card)
            records.append(record)

        #go to next page if there is one, break if no next page is available
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label':'Next'}).get('href')
        except AttributeError:
            break

        #write data to csv file
        with open('results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['JobTitle', 'Company', 'Location', 'Summary', 'PostDate', 'ExtractDate', 'Salary', 'URL'])
            writer.writerows(records)

#run program, specify job title and location
main('programming%20internship', 'seattle')