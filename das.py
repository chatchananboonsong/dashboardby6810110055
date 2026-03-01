from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
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

import plotly.express as px # เพิ่ม import ตัวนี้ที่ด้านบนสุดของไฟล์ด้วยครับ

# สร้างตัวแอป Dash
app = Dash(__name__)

# ออกแบบหน้าตาเว็บ
app.layout = html.Div([
    html.H1("🎬 IMDB Movie Dashboard", style={'textAlign': 'center', 'color': '#f3ce13'}),
    
    # ส่วนตัวเลือก (Dropdown)
    html.Div([
        html.Label("เลือกกลุ่มผู้ชม (Certificate):", style={'color': 'white'}),
        dcc.Dropdown(
            id='cert-dropdown',
            options=[{'label': i, 'value': i} for i in sorted(df['Certificate'].unique())],
            value='PG-13', # ค่าเริ่มต้นที่ให้แสดง
            style={'color': 'black'}
        ),
    ], style={'width': '40%', 'margin': 'auto', 'padding': '20px'}),
])