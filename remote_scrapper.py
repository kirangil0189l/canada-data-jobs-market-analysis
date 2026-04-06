import requests
import pandas as pd

print("Fetching from RemoteOK API...")

url = "https://remoteok.com/api"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

response = requests.get(url, headers=headers)
data = response.json()

# First item is a notice, skip it
jobs = data[1:]

all_jobs = []
data_keywords = ['data', 'analyst', 'sql', 'python', 'analytics',
                 'database', 'machine learning', 'scientist', 'bi', 'tableau']

for job in jobs:
    title = job.get('position', '')
    
    # Only keep data-related jobs
    if any(kw in title.lower() for kw in data_keywords):
        all_jobs.append({
            "title": title,
            "company": job.get('company', 'N/A'),
            "location": job.get('location', 'Worldwide'),
            "salary_min": job.get('salary_min', None),
            "salary_max": job.get('salary_max', None),
            "job_type": "FULLTIME",
            "work_type": "Remote",
            "description": job.get('description', ''),
            "province": "Remote/Worldwide",
            "source": "RemoteOK"
        })

print(f"Found {len(all_jobs)} remote data jobs")

if len(all_jobs) > 0:
    remote_df = pd.DataFrame(all_jobs)
    print(remote_df[['title', 'company', 'location']].head(20))
    remote_df.to_csv("remote_jobs.csv", index=False)
    print("\n✅ Saved: remote_jobs.csv")
else:
    print("No jobs found")