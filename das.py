from dash import Dash, html, dcc, Input, Output
import pandas as pd
import kagglehub
import os

# 1. โหลดข้อมูล
print("Checking for dataset...")
path = kagglehub.dataset_download("mazenramadan/imdb-most-popular-films-and-series")
csv_path = os.path.join(path, "imdb.csv")
df = pd.read_csv(csv_path)
