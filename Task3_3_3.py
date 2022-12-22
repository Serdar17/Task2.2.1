import requests
import pandas as pd
from pandas import json_normalize
pd.set_option("expand_frame_repr", False)

pages = []
for i in range(0, 20):
    pages.append(f"https://api.hh.ru/vacancies?specialization=1&per_page=100&page={i}&date_from=2022-12-16T21:00:00&date_to=2022-12-17T00:00:00")

vacancies = []
for page in pages:
    result = requests.get(page).json()
    vacancies.extend(result["items"])

df_current = pd.read_csv("vacancies_for_2022-12-16.csv")
df = json_normalize(vacancies)
df1 = df[["name", "salary.from", "salary.to", "salary.currency", "area.name", "published_at"]]
df1.columns = df1.columns.str.replace(".", "_")
df_current = df_current.append(df1, ignore_index=True)
df_current.to_csv("vacancies_for_2022-12-16.csv", index=False)