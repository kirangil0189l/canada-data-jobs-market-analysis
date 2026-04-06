import requests
import pandas as pd
import time

API_KEY = "YOUR_API_KEY_HERE"

url = "https://jsearch.p.rapidapi.com/search"
headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}

# Search multiple queries to get more data
queries = [
    "data analyst Canada",
    "data scientist Canada",
    "business analyst Canada",
    "database analyst Canada",
    "SQL analyst Canada"
]

all_jobs = []

for query in queries:
    print(f"Fetching: {query}...")
    params = {
        "query": query,
        "page": "1",
        "num_pages": "3",
        "country": "ca"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        for job in data.get('data', []):
            all_jobs.append({
                "title":       job.get('job_title') or 'N/A',
                "company":     job.get('employer_name') or 'N/A',
                "location":    (job.get('job_city') or '') + ", " + (job.get('job_state') or ''),
                "salary_min":  job.get('job_min_salary') or None,
                "salary_max":  job.get('job_max_salary') or None,
                "job_type":    job.get('job_employment_type') or 'N/A',
                "remote": job.get('job_is_remote') or False,
                "remote_keywords": any(word in (job.get('job_description', '') + ' ' + job.get('job_title', '')).lower() 
                       for word in ['remote', 'work from home', 'wfh', 'hybrid', 'télétravail']),
                "description": job.get('job_description') or '',
                "source":      "JSearch"
            })
        print(f"  → Got {len(data.get('data', []))} jobs")
        time.sleep(1)  # be polite to the API

    except Exception as e:
        print(f"  → Error: {e}")

# Build dataframe
df = pd.DataFrame(all_jobs)
df['location'] = df['location'].str.strip(', ')

# Remove duplicates
df.drop_duplicates(subset=['title', 'company'], inplace=True)
print(f"\nTotal unique jobs collected: {len(df)}")

# ── SKILL ANALYSIS ──────────────────────────────────────
skills = [
    'SQL', 'Python', 'Tableau', 'Power BI', 'Excel',
    'R', 'Machine Learning', 'Azure', 'Spark', 'MongoDB',
    'PostgreSQL', 'Pandas', 'NumPy', 'Statistics', 'ETL',
    'Looker', 'Snowflake', 'AWS', 'Databricks', 'dbt'
]

print("\n── Top Skills in Demand ──")
skill_counts = {}
for skill in skills:
    count = df['description'].str.contains(skill, case=False, na=False).sum()
    skill_counts[skill] = count
    print(f"  {skill:20} {count} jobs")

skill_df = pd.DataFrame(list(skill_counts.items()),
                        columns=['skill', 'job_count'])
skill_df.sort_values('job_count', ascending=False, inplace=True)

# ── LOCATION ANALYSIS ───────────────────────────────────
print("\n── Top Locations ──")
print(df['location'].value_counts().head(10))

# ── REMOTE ANALYSIS ─────────────────────────────────────
print("\n── Remote vs On-site ──")
print(df['remote'].value_counts())

# ── SALARY ANALYSIS ─────────────────────────────────────
salary_df = df.dropna(subset=['salary_min', 'salary_max'])
if len(salary_df) > 0:
    print(f"\n── Salary Insights ──")
    print(f"  Average min salary: ${salary_df['salary_min'].mean():,.0f}")
    print(f"  Average max salary: ${salary_df['salary_max'].mean():,.0f}")

# ── SAVE FILES ──────────────────────────────────────────
df.to_csv("canada_jobs.csv", index=False)
skill_df.to_csv("skill_analysis.csv", index=False)
print("\nSaved: canada_jobs.csv")
print("Saved: skill_analysis.csv")