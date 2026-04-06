import pandas as pd
import matplotlib.pyplot as plt

# ── LOAD DATA ───────────────────────────────────────────
df = pd.read_csv("canada_jobs.csv")
print(f"Total jobs loaded: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst look:")
print(df.head())

# ── BASIC INFO ──────────────────────────────────────────
print("\n── Missing Values ──")
print(df.isnull().sum())

print("\n── Job Types ──")
print(df['job_type'].value_counts())

print("\n── Remote vs On-site ──")
print(df['remote'].value_counts())

# ── CLEAN LOCATION ──────────────────────────────────────
# Extract province from location column
def extract_province(location):
    if pd.isna(location):
        return 'Unknown'
    
    location = str(location)
    
    provinces = [
        'Ontario',
        'British Columbia',
        'Alberta',
        'Quebec',
        'Manitoba',
        'Saskatchewan',
        'Nova Scotia',
        'New Brunswick',
        'Newfoundland',
        'Prince Edward Island',
        'Yukon',
        'Northwest Territories',
        'Nunavut'
    ]
    
    for province in provinces:
        if province.lower() in location.lower():
            return province
    
    # Handle French version
    if 'québec' in location.lower():
        return 'Quebec'
        
    return 'Unknown'

df['province'] = df['location'].apply(extract_province)

print("\n── Jobs by Province (corrected) ──")
print(df['province'].value_counts())

# ── SKILL ANALYSIS ──────────────────────────────────────
import re

skills = {
    'SQL': r'\bSQL\b',
    'Python': r'\bPython\b',
    'R (language)': r'\bR\b(?!\s*&)',  
    'Excel': r'\bExcel\b',
    'Tableau': r'\bTableau\b',
    'Power BI': r'\bPower\s*BI\b',
    'Machine Learning': r'\bMachine\s*Learning\b',
    'Azure': r'\bAzure\b',
    'Spark': r'\bSpark\b',
    'MongoDB': r'\bMongoDB\b',
    'PostgreSQL': r'\bPostgreSQL\b',
    'Pandas': r'\bPandas\b',
    'NumPy': r'\bNumPy\b',
    'Statistics': r'\bStatistics\b',
    'ETL': r'\bETL\b',
    'Looker': r'\bLooker\b',
    'Snowflake': r'\bSnowflake\b',
    'AWS': r'\bAWS\b',
    'Databricks': r'\bDatabricks\b',
    'dbt': r'\bdbt\b',
    'TensorFlow': r'\bTensorFlow\b',
    'PyTorch': r'\bPyTorch\b',
    'Scikit-learn': r'\bScikit-learn\b',
    'NoSQL': r'\bNoSQL\b'
}

skill_counts = {}
for skill, pattern in skills.items():
    count = df['description'].str.contains(pattern, case=False, na=False, regex=True).sum()
    skill_counts[skill] = count

skill_df = pd.DataFrame(list(skill_counts.items()),
                        columns=['skill', 'job_count'])
skill_df.sort_values('job_count', ascending=False, inplace=True)
skill_df['percentage'] = (skill_df['job_count'] / len(df) * 100).round(1)

print("\n── Top Skills in Demand (corrected) ──")
print(skill_df.to_string(index=False))

# ── SALARY ANALYSIS ─────────────────────────────────────
salary_df = df.dropna(subset=['salary_min', 'salary_max'])
print(f"\n── Salary Data ({len(salary_df)} jobs with salary info) ──")
if len(salary_df) > 0:
    print(f"Average min salary: ${salary_df['salary_min'].mean():,.0f}")
    print(f"Average max salary: ${salary_df['salary_max'].mean():,.0f}")
    print(f"Highest max salary: ${salary_df['salary_max'].max():,.0f}")
    print(f"Lowest min salary:  ${salary_df['salary_min'].min():,.0f}")

# ── QUICK CHARTS ────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Canadian Data Analyst Job Market Analysis', fontsize=16)

# Chart 1 — Top 10 Skills
top_skills = skill_df.head(10)
axes[0,0].barh(top_skills['skill'], top_skills['job_count'], color='steelblue')
axes[0,0].set_title('Top 10 In-Demand Skills')
axes[0,0].set_xlabel('Number of Jobs')
axes[0,0].invert_yaxis()

# Chart 2 — Jobs by Province
province_counts = df['province'].value_counts().head(8)
axes[0,1].bar(province_counts.index, province_counts.values, color='coral')
axes[0,1].set_title('Jobs by Province')
axes[0,1].set_xlabel('Province')
axes[0,1].set_ylabel('Number of Jobs')
axes[0,1].tick_params(axis='x', rotation=45)


# Chart 3 — Remote vs On-site
# Detect remote from keywords if API field unreliable
df['remote_detected'] = df['description'].str.lower().str.contains(
    'remote|work from home|wfh|hybrid|télétravail', 
    case=False, na=False
) | df['title'].str.lower().str.contains(
    'remote|hybrid', 
    case=False, na=False
)

print("\n── Remote/Hybrid Detection (from keywords) ──")
print(df['remote_detected'].value_counts())

# Categorize more specifically
def classify_work_type(row):
    text = str(row.get('description', '')).lower() + ' ' + str(row.get('title', '')).lower()
    if 'hybrid' in text:
        return 'Hybrid'
    elif 'remote' in text or 'work from home' in text or 'wfh' in text:
        return 'Remote'
    else:
        return 'On-site'

df['work_type'] = df.apply(classify_work_type, axis=1)

print("\n── Work Type Breakdown ──")
print(df['work_type'].value_counts())

# Fix the pie chart to use work_type
work_counts = df['work_type'].value_counts()
colors_map = {'On-site': 'steelblue', 'Remote': 'coral', 'Hybrid': 'mediumseagreen'}
colors = [colors_map.get(label, 'grey') for label in work_counts.index]

axes[1,0].pie(work_counts.values, labels=work_counts.index,
              autopct='%1.1f%%', colors=colors)
axes[1,0].set_title('Work Type (Remote / Hybrid / On-site)')

# Chart 4 — Job Type
job_type_counts = df['job_type'].value_counts().head(5)
axes[1,1].bar(job_type_counts.index, job_type_counts.values, color='mediumseagreen')
axes[1,1].set_title('Job Types')
axes[1,1].set_xlabel('Type')
axes[1,1].set_ylabel('Count')
axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('job_market_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n Chart saved as job_market_analysis.png")

# ── SAVE CLEANED DATA FOR TABLEAU ───────────────────────
df['salary_avg'] = (df['salary_min'].fillna(0) + df['salary_max'].fillna(0)) / 2
df.to_csv("canada_jobs_cleaned.csv", index=False)
skill_df.to_csv("skill_analysis.csv", index=False)

print("\n Saved: canada_jobs_cleaned.csv  → for Tableau")
print(" Saved: skill_analysis.csv        → for Tableau")
print("\nNext step: Build Tableau dashboard!")


#Debugging
print("\n── Remote column debug ──")
print("Data type:", df['remote'].dtype)
print("Unique values:", df['remote'].unique())
print("Value counts:", df['remote'].value_counts())
# # Debug province detection
# print("\n── Province Debug ──")
# print("Sample location values:")
# print(df['location'].value_counts().head(30))

# print("\n── Rows classified as Unknown ──")
# unknown = df[df['province'] == 'Unknown']
# print(f"Total Unknown: {len(unknown)}")
# print(unknown['location'].value_counts().head(20))

# print("\n── Rows classified as Other ──")
# other = df[df['province'] == 'Other']
# print(f"Total Other: {len(other)}")
# print(other['location'].value_counts().head(20))