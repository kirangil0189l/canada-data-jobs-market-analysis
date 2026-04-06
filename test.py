# import requests
# import pandas as pd

# url = "https://jsearch.p.rapidapi.com/search"

# headers = {
#     "x-rapidapi-key": "5559f8f3e9msh2c372832fae5ccbp156c1ejsne13b6e410d60",
#     "x-rapidapi-host": "jsearch.p.rapidapi.com"
# }

# params = {
#     "query": "data analyst Canada",
#     "page": "1",
#     "num_pages": "5",
#     "country": "ca"
# }

# response = requests.get(url, headers=headers, params=params)
# data = response.json()

# # Print full response to see structure
# print("Status code:", response.status_code)
# print("Response keys:", data.keys())
# print("Full response:", data)

# import pandas as pd

# df = pd.read_csv("canada_jobs_cleaned.csv")

# # Just check location column quickly
# print("Total jobs:", len(df))
# print("\nAll unique locations:")
# print(df['location'].unique())

# import requests
# from bs4 import BeautifulSoup

# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# }

# url = "https://weworkremotely.com/categories/remote-data-science-jobs"
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')

# # Print raw HTML to see real structure
# print(response.text[:5000])


# import pandas as pd

# df = pd.read_csv("canada_jobs_final.csv")
# print(df.columns.tolist())
# print("\nProvince column sample:")
# print(df['province'].head(20))
# print("\nAll unique province values:")
# print(df['province'].unique())

# import pandas as pd

# # Load and check raw CSV
# df = pd.read_csv("canada_jobs_final.csv")

# print("Shape:", df.shape)
# print("\nColumns:", df.columns.tolist())
# print("\nProvince column position:", df.columns.tolist().index('province'))

# # Check if description text is leaking into province
# print("\nAny description text in province?")
# long_provinces = df[df['province'].str.len() > 20]
# print(long_provinces[['title', 'province']].head(10))

# # Re-save cleanly
# df_clean = df[['title', 'company', 'location', 'province',
#                'job_type', 'work_type', 'salary_min',
#                'salary_max', 'salary_avg', 'source']].copy()

# # Drop description completely — Tableau doesn't need it
# df_clean.to_csv("canada_jobs_tableau.csv", index=False)
# print("\nSaved clean file: canada_jobs_tableau.csv")
# print("Columns:", df_clean.columns.tolist())
# print("\nProvince values:")
# print(df_clean['province'].value_counts())


import pandas as pd

df = pd.read_csv("canada_jobs_tableau.csv")

# Standardize job type values
df['job_type'] = df['job_type'].str.strip()
df['job_type'] = df['job_type'].replace({
    'FULLTIME': 'Full-time',
    'PARTTIME': 'Part-time',
    'CONTRACTOR': 'Contractor',
    'INTERN': 'Internship',
    'Full time': 'Full-time',
    'Part time': 'Part-time'
})

print("Fixed job types:")
print(df['job_type'].value_counts())

df.to_csv("canada_jobs_tableau.csv", index=False)
print("✅ Saved!")