import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Search for data analyst jobs in Canada
url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=data+analyst&locationstring=Canada"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Fetching jobs from Canada Job Bank...")
response = requests.get(url, headers=headers)
print(f"Status code: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')

# Find all job listings
jobs = []
listings = soup.find_all('article', class_='resultJobItem')

print(f"Found {len(listings)} job listings")

for job in listings:
    try:
        title = job.find('span', class_='noctitle').text.strip()
    except:
        title = "N/A"
    try:
        company = job.find('li', class_='business').text.strip()
    except:
        company = "N/A"
    try:
        location = job.find('li', class_='location').text.strip()
    except:
        location = "N/A"
    try:
        salary = job.find('li', class_='salary').text.strip()
    except:
        salary = "N/A"

    jobs.append({
        "title": title,
        "company": company,
        "location": location,
        "salary": salary
    })

# Save to CSV
df = pd.DataFrame(jobs)
print(df.head())
df.to_csv("canada_jobs.csv", index=False)
print("Saved to canada_jobs.csv!")