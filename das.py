from dash import Dash, html, dcc, Input, Output, dash_table
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
    # ส่วนหัวที่ชิดขอบบนสุด
    html.H1("🎬 IMDB Movie Dashboard", 
            style={'textAlign': 'center', 'color': "#ffffff", 'padding': '40px 20px 10px 20px', 'margin': '0'}),
    
    html.Div(id='summary-stats', 
             style={'textAlign': 'center', 'color': '#f3ce13', 'fontSize': '20px', 'paddingBottom': '20px'}),

    # Dropdown Filter
    html.Div([
        html.Label("เลือกกลุ่มผู้ชม (Certificate):", style={'color': 'white', 'display': 'block', 'marginBottom': '10px'}),
        dcc.Dropdown(
            id='cert-dropdown',
            options=[{'label': i, 'value': i} for i in sorted(df['Certificate'].unique())],
            value='PG-13',
            style={'color': 'black'}
        ),
    ], style={'width': '40%', 'margin': 'auto', 'padding': '10px'}),

    # พื้นที่แสดงกราฟ
    html.Div([
        html.Div([
            dcc.Graph(id='graph-1', style={'display': 'inline-block', 'width': '50%'}),
            dcc.Graph(id='graph-2', style={'display': 'inline-block', 'width': '50%'}),
        ]),
        dcc.Graph(id='graph-3', style={'width': '100%'}),
    ], style={'padding': '20px'}),

    # --- ส่วนที่เพิ่มใหม่: ตารางข้อมูลภาพยนตร์ ---
    html.Div([
        html.H3("📋 รายละเอียดข้อมูลภาพยนตร์", style={'color': '#f3ce13', 'paddingLeft': '20px'}),
        dash_table.DataTable(
            id='data-table',
            columns=[
                {"name": "Title", "id": "Title"},
                {"name": "Year", "id": "Year"},
                {"name": "Rating", "id": "Rating"},
                {"name": "Genre", "id": "Genre"},
                {"name": "Certificate", "id": "Certificate"}
            ],
            page_size=10,
            style_table={'overflowX': 'auto', 'padding': '20px'},
            style_header={'backgroundColor': '#333', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid #444'},
            style_cell={'backgroundColor': '#1a1a1a', 'color': 'white', 'textAlign': 'left', 'padding': '10px', 'border': '1px solid #444'},
        )
    ])
], style={
    'backgroundColor': "#000000", 
    'minHeight': '100vh',
    'margin': '-8px',      
    'padding': '0',
    'overflowX': 'hidden'
})

# 4. Callback (ต้องคืนค่า 5 อย่าง: กราฟ 3 ตัว, ข้อความสรุป, และ ข้อมูลตาราง)
@app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-2', 'figure'),
     Output('graph-3', 'figure'),
     Output('summary-stats', 'children'),
     Output('data-table', 'data')],
    [Input('cert-dropdown', 'value')]
)
def update_charts(selected_cert):
    filtered_df = df[df['Certificate'] == selected_cert]
    
    # Fig 1: Histogram
    fig1 = px.histogram(filtered_df, x="Rating", title="การกระจายของคะแนนรีวิว",
                        template="plotly_dark", color_discrete_sequence=['#f3ce13'])
    fig1.update_layout(xaxis_title="Rating", yaxis_title="Movie Count")

    # Fig 2: Scatter
    fig2 = px.scatter(filtered_df, x="Year", y="Rating", hover_name="Title",
                      title="คะแนนรีวิวในแต่ละปี", template="plotly_dark")
    fig2.update_traces(marker=dict(size=10, opacity=0.6, line=dict(width=1, color='White')))
    
    # Fig 3: Bar
    genre_avg = filtered_df.groupby('Genre')['Rating'].mean().nlargest(10).reset_index()
    fig3 = px.bar(genre_avg, x='Genre', y='Rating', title="Top 10 ประเภทหนังคะแนนสูงสุด", 
                  template="plotly_dark",
                  color='Rating',
                  color_continuous_scale='Viridis')
    fig3.update_xaxes(tickangle=0)
    fig3.update_layout(xaxis_tickfont_size=10)
    
    # คำนวณค่าสรุป
    avg_rating = filtered_df['Rating'].mean()
    total_movies = len(filtered_df)
    summary_text = f"จำนวนภาพยนตร์ทั้งหมด: {total_movies} เรื่อง | คะแนนเฉลี่ย: {avg_rating:.2f}"
    
    # เตรียมข้อมูลตาราง
    table_data = filtered_df.to_dict('records')
    
    return fig1, fig2, fig3, summary_text, table_data

if __name__ == '__main__':
    app.run(debug=True)