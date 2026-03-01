from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import kagglehub
import os

# 1. โหลดข้อมูล
path = kagglehub.dataset_download("mazenramadan/imdb-most-popular-films-and-series")
csv_path = os.path.join(path, "imdb.csv")
df = pd.read_csv(csv_path)

# 2. จัดการข้อมูล
df = df.rename(columns={'Rate': 'Rating', 'Date': 'Year', 'Name': 'Title'})
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Rating', 'Year', 'Certificate', 'Genre'])

app = Dash(__name__)

# 3. ออกแบบหน้าตาเว็บ
app.layout = html.Div([
    html.H1("🎬 IMDB Movie Dashboard", style={'textAlign': 'center', 'color': "#ffffff", 'padding': '20px'}),
    
    # ส่วนตัวเลขสรุป (Summary Stats)
    html.Div(id='summary-stats', style={'textAlign': 'center', 'color': '#f3ce13', 'fontSize': '20px', 'marginBottom': '20px'}),

    html.Div([
        html.Label("เลือกกลุ่มผู้ชม (Certificate):", style={'color': 'white'}),
        dcc.Dropdown(
            id='cert-dropdown',
            options=[{'label': i, 'value': i} for i in sorted(df['Certificate'].unique())],
            value='PG-13',
            style={'color': 'black'}
        ),
    ], style={'width': '40%', 'margin': 'auto', 'padding': '20px'}),

    html.Div([
        html.Div([
            dcc.Graph(id='graph-1', style={'display': 'inline-block', 'width': '50%'}),
            dcc.Graph(id='graph-2', style={'display': 'inline-block', 'width': '50%'}),
        ]),
        dcc.Graph(id='graph-3', style={'width': '100%'}),
    ], style={'padding': '20px'})
], style={
    'backgroundColor': "#000000", 
    'minHeight': '100vh',  # คลุมทั้งหน้าจอ
    'margin': '-8px',      # ลบขอบขาวของ Browser
    'padding': '0',        # มั่นใจว่าไม่มี padding ด้านนอกสุด
    'overflowX': 'hidden'  # ป้องกันแถบเลื่อนแนวนอนโผล่
})

# 4. ส่วน Callback (หัวใจการทำงาน)
@app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-2', 'figure'),
     Output('graph-3', 'figure'),
     Output('summary-stats', 'children')],
    [Input('cert-dropdown', 'value')]
)
def update_charts(selected_cert):
    # กรองข้อมูล
    filtered_df = df[df['Certificate'] == selected_cert]
    
    # กราฟที่ 1: Histogram
    fig1 = px.histogram(filtered_df, x="Rating", title="การกระจายของคะแนนรีวิว",
                        template="plotly_dark", color_discrete_sequence=['#f3ce13'])
    fig1.update_layout(xaxis_title="Rating", yaxis_title="movie count")

    # กราฟที่ 2: Scatter
    fig2 = px.scatter(filtered_df, x="Year", y="Rating", hover_name="Title",
                      title="คะแนนรีวิวในแต่ละปี", template="plotly_dark")
    fig2.update_traces(marker=dict(size=10, opacity=0.6, line=dict(width=1, color='White')))
    
    # กราฟที่ 3: Bar (คำนวณก่อนสร้างกราฟ)
    genre_avg = filtered_df.groupby('Genre')['Rating'].mean().nlargest(10)
    fig3 = px.bar(genre_avg, title="Top 10 ประเภทหนังคะแนนสูงสุด", 
                  template="plotly_dark",
                  color=genre_avg.values,
                  color_continuous_scale='Viridis')
    fig3.update_xaxes(tickangle=0)
    fig3.update_layout(xaxis_tickfont_size=8)
    
    # คำนวณค่าสรุป
    avg_rating = filtered_df['Rating'].mean()
    total_movies = len(filtered_df)
    summary_text = f"จำนวนภาพยนตร์ทั้งหมด: {total_movies} เรื่อง | คะแนนเฉลี่ย: {avg_rating:.2f}"
    
    return fig1, fig2, fig3, summary_text

if __name__ == '__main__':
    app.run(debug=True)