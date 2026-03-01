from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import kagglehub
import os

# 1. โหลดข้อมูลจาก Kaggle
path = kagglehub.dataset_download("mazenramadan/imdb-most-popular-films-and-series")
csv_path = os.path.join(path, "imdb.csv")
df = pd.read_csv(csv_path)

df = df.rename(columns={
    'Rate': 'Rating',
    'Date': 'Year',
    'Name': 'Title'
})

df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

df = df.dropna(subset=['Rating', 'Year', 'Certificate', 'Genre'])

app = Dash(__name__)

# ออกแบบโครงสร้างหน้าเว็บ (Layout)
app.layout = html.Div([
    # ส่วนหัว (Header)
    html.H1("🎬 IMDB Movie Dashboard", 
            style={'textAlign': 'center', 'color': '#f3ce13', 'padding': '20px'}),
    
    # ส่วนตัวเลือก (Dropdown Filter)
    html.Div([
        html.Label("เลือกเรตหนัง (Certificate):", style={'color': 'white'}),
        dcc.Dropdown(
            id='cert-dropdown',
            options=[{'label': i, 'value': i} for i in sorted(df['Certificate'].unique())],
            value='PG-13', # ค่าเริ่มต้น
            style={'color': 'black'}
        ),
    ], style={'width': '40%', 'margin': 'auto', 'padding': '20px'}),

    # ส่วนพื้นที่วางกราฟ (Graph Container)
    html.Div([
        dcc.Graph(id='rating-hist'),  # กราฟความถี่คะแนน
        dcc.Graph(id='year-scatter'), # กราฟเทรนด์ตามปี
        dcc.Graph(id='genre-bar'),    # กราฟแท่งประเภทหนัง
    ], style={'padding': '20px'})

], style={'backgroundColor': '#1a1a1a', 'minHeight': '100vh'}) # พื้นหลังสีดำเข้ม

@app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-2', 'figure'),
     Output('graph-3', 'figure')],
    [Input('cert-dropdown', 'value')]
)

def update_charts(selected_cert):
    # 1. กรองข้อมูลตามที่ผู้ใช้เลือก
    filtered_df = df[df['Certificate'] == selected_cert]
    
    # 2. สร้างกราฟที่ 1: Histogram (ดูการกระจายของคะแนน)
    fig1 = px.histogram(filtered_df, x="Rating", title="การกระจายของคะแนนรีวิว",
                        template="plotly_dark", color_discrete_sequence=['#f3ce13'])
    # 3. สร้างกราฟที่ 2: Scatter (ดูคะแนนตามปีที่ฉาย)
    fig2 = px.scatter(filtered_df, x="Year", y="Rating", hover_name="Title",
                      title="คะแนนรีวิวในแต่ละปี", template="plotly_dark")
    # 4. สร้างกราฟที่ 3: Bar (10 อันดับประเภทหนังที่คะแนนเฉลี่ยสูงสุด)
    genre_avg = filtered_df.groupby('Genre')['Rating'].mean().nlargest(10)
    fig3 = px.bar(genre_avg, title="Top 10 ประเภทหนังคะแนนสูงสุด", template="plotly_dark")
    
    return fig1,fig2,fig3

if __name__ == '__main__':
    app.run(debug=True)