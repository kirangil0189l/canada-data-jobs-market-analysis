# Canadian Data Analyst Job Market Analysis

## Why I Built This

I'm actively looking for data analyst roles in Canada and wanted to 
understand what skills employers actually care about — not just what 
people say online. So instead of guessing, I built a scraper to collect 
real job postings and analyze them.

---

## What I Did

Collected 149 job postings from Indeed, Glassdoor and RemoteOK using 
Python and public APIs. Cleaned the data, extracted skill mentions from 
job descriptions, and built a Tableau dashboard to explore the results.

---

## What I Found

- **SQL shows up in 65% of postings** — it's non-negotiable for analyst roles
- **Python is in 36% of jobs** — clearly expected beyond just Excel
- **Power BI is more common than Tableau** in Canadian postings — 
  good to know if you're choosing which to learn
- **Ontario has almost half the jobs** — Toronto/GTA is the clear hub
- **Only 12% of jobs are fully remote** — hybrid is more realistic at 32%

---

## Dashboard
 [View on Tableau Public](https://public.tableau.com/shared/D8T9MJR3Y?:display_count=n&:origin=viz_share_link)

---

## Files

| File | What it does |
|------|-------------|
| `combined_scraper.py` | Pulls jobs from JSearch API |
| `remote_scraper.py` | Pulls remote jobs from RemoteOK |
| `analysis.py` | Cleans data, detects skills, work type |
| `combined_data.py` | Merges both sources into one dataset |
| `canada_jobs_tableau.csv` | Final cleaned data used in Tableau |
| `skill_analysis_final.csv` | Skill counts and percentages |

---

## Tools Used
Python · Pandas · BeautifulSoup · Matplotlib · Tableau · JSearch API · RemoteOK API

---

## Honest Limitations

- LinkedIn blocks scrapers so LinkedIn jobs are missing — 
  remote numbers are probably understated because of this
- No salary data — the API didn't return it reliably for Canadian postings
- This is a snapshot from April 2026, not a live dataset
- 149 jobs is a decent sample but not exhaustive

---

## How to Run It Yourself
```bash
pip install requests beautifulsoup4 pandas matplotlib
1. Get a free API key from [RapidAPI JSearch](https://rapidapi.com)
2. Replace `YOUR_API_KEY_HERE` in `combined_scraper.py` with your key
3. Run the scripts

python3 combined_scraper.py   # collect jobs
python3 remote_scraper.py     # collect remote jobs  
python3 analysis.py           # clean and analyze
python3 combine_data.py       # merge everything
```
Then open Tableau and connect to `canada_jobs_tableau.csv`

---
## Updated Version of above project using n8n
## n8n Automation Workflow

I extended this project by creating an n8n workflow to automate job market data collection and monitoring. The workflow collects job postings from multiple APIs, combines the data into one dataset, removes duplicate job postings, and saves the cleaned records into Google Sheets. I also added a weekly alert that checks for newly posted jobs and notifies me about new opportunities.

Workflow steps:
1. Schedule Trigger runs the workflow automatically.
2. HTTP Request nodes collect job posting data from multiple APIs.
3. JavaScript code nodes clean and standardize the fields.
4. Merge node combines data from different sources.
5. Duplicate records are removed to keep the dataset clean.
6. Google Sheets node stores the final cleaned data.
7. Weekly alert identifies newly posted jobs.

**Sukhkirandeep Kaur Sidhu,Ph.D.**  
[Portfolio](https://www.sukhkirandeep.com) · 
[LinkedIn](https://www.linkedin.com/in/sukhkirandeep-kaur-sidhu-ph-d-18420a82) · 
sukhkirandeep.kaur@gmail.com
