from dash import Dash, html, dcc, Input, Output
import pandas as pd
import kagglehub
import os

# 1. โหลดข้อมูล
print("Checking for dataset...")
path = kagglehub.dataset_download("mazenramadan/imdb-most-popular-films-and-series")
csv_path = os.path.join(path, "imdb.csv")
df = pd.read_csv(csv_path)

# แสดงชื่อคอลัมน์เพื่อความมั่นใจ
print("Current Columns:", df.columns.tolist())

df = df.rename(columns={
    'Rate': 'Rating',
    'Date': 'Year',
    'Name': 'Title'
})

df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

df = df.dropna(subset=['Rating', 'Year', 'Certificate', 'Genre'])