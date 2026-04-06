import pandas as pd

# ── LOAD BOTH SOURCES ───────────────────────────────────
api_df = pd.read_csv("canada_jobs_cleaned.csv")
remote_df = pd.read_csv("remote_jobs.csv")

print(f"API jobs (Indeed/Glassdoor): {len(api_df)}")
print(f"Remote jobs (RemoteOK):      {len(remote_df)}")

# ── MAKE SURE COLUMNS MATCH ─────────────────────────────
# Add missing columns to remote_df
remote_df['remote'] = True
remote_df['job_type'] = remote_df.get('job_type', 'FULLTIME')

# Add missing columns to api_df if needed
if 'source' not in api_df.columns:
    api_df['source'] = 'JSearch'

# ── COMBINE ─────────────────────────────────────────────
combined_df = pd.concat([api_df, remote_df], ignore_index=True)

# Remove duplicates
combined_df.drop_duplicates(subset=['title', 'company'], inplace=True)

print(f"\nCombined total:              {len(combined_df)} jobs")

# ── FIX WORK TYPE ───────────────────────────────────────
# RemoteOK jobs are all remote — make sure they're tagged correctly
combined_df.loc[combined_df['source'] == 'RemoteOK', 'work_type'] = 'Remote'

print(f"\n── Work Type Breakdown ──")
print(combined_df['work_type'].value_counts())

print(f"\n── Source Breakdown ──")
print(combined_df['source'].value_counts())

print(f"\n── Province Breakdown ──")
print(combined_df['province'].value_counts())

# ── SKILL ANALYSIS ON COMBINED DATA ─────────────────────
import re

skills = {
    'SQL':               r'\bSQL\b',
    'Python':            r'\bPython\b',
    'Excel':             r'\bExcel\b',
    'Power BI':          r'\bPower\s*BI\b',
    'Tableau':           r'\bTableau\b',
    'R (language)':      r'\bR\b',
    'Statistics':        r'\bStatistics\b',
    'Machine Learning':  r'\bMachine\s*Learning\b',
    'Azure':             r'\bAzure\b',
    'ETL':               r'\bETL\b',
    'Spark':             r'\bSpark\b',
    'MongoDB':           r'\bMongoDB\b',
    'PostgreSQL':        r'\bPostgreSQL\b',
    'Snowflake':         r'\bSnowflake\b',
    'AWS':               r'\bAWS\b',
    'Databricks':        r'\bDatabricks\b',
    'dbt':               r'\bdbt\b',
    'Looker':            r'\bLooker\b',
    'NumPy':             r'\bNumPy\b',
    'Pandas':            r'\bPandas\b',
}

skill_counts = {}
for skill, pattern in skills.items():
    count = combined_df['description'].str.contains(
        pattern, case=False, na=False, regex=True).sum()
    skill_counts[skill] = count

skill_df = pd.DataFrame(list(skill_counts.items()),
                        columns=['skill', 'job_count'])
skill_df.sort_values('job_count', ascending=False, inplace=True)
skill_df['percentage'] = (skill_df['job_count'] / len(combined_df) * 100).round(1)

print(f"\n── Top Skills (combined data) ──")
print(skill_df.to_string(index=False))

# ── SAVE FINAL FILES ────────────────────────────────────
combined_df.to_csv("canada_jobs_final.csv", index=False)
skill_df.to_csv("skill_analysis_final.csv", index=False)

print(f"\nSaved: canada_jobs_final.csv     → main Tableau data")
print(f" Saved: skill_analysis_final.csv  → skills Tableau data")
print(f"\nTotal jobs ready for Tableau: {len(combined_df)}")