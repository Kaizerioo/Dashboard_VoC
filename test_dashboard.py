import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# ======================================================================================
# 1. KONFIGURASI HALAMAN DAN GAYA (CSS)
# ======================================================================================

st.set_page_config(
    page_title="Voice of Customer Dashboard",
    page_icon="📊",
    layout="wide"
)

# Ekstrak dan adaptasi CSS kunci dari file HTML
# Ini menargetkan kelas yang dihasilkan Streamlit dan kelas kustom yang kita tambahkan.
st.markdown("""
<style>
    /* Mengimpor Font Apple */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Variabel Warna Utama dari CSS asli */
    :root {
        --font-family-apple: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        --card-background: #ffffff;
        --text-primary: #1d1d1f;
        --text-secondary: #4a4a4f;
        --accent-color: #007aff;
        --accent-color-darker: #005ecb;
        --border-color: #d2d2d7;
        --light-border-color: #e5e5ea;
        --shadow-color-light: rgba(0, 0, 0, 0.03);
        --shadow-color-medium: rgba(0, 0, 0, 0.06);
        --border-radius-l: 14px;
        --padding-l: 1.2rem;
    }

    /* Font dan Latar Belakang Tubuh Utama */
    body {
        font-family: var(--font-family-apple);
        background-color: #f2f4f6; /* Disederhanakan dari gradien untuk kinerja */
    }

    /* Menata Kontainer Widget Streamlit */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--card-background);
        border-radius: var(--border-radius-l);
        padding: calc(var(--padding-l) - 0.5rem) var(--padding-l) var(--padding-l) var(--padding-l);
        box-shadow: 0 2px 5px var(--shadow-color-light), 0 5px 10px var(--shadow-color-medium);
        border: 1px solid var(--border-color);
    }
    
    /* Header di dalam widget */
    h3 {
        font-size: 1.05rem;
        font-weight: 500;
        color: var(--text-primary);
        letter-spacing: -0.01em;
        margin-bottom: 0.5rem;
    }
    
    /* Teks sekunder untuk metrik */
    .metric-subtitle {
        font-size: 0.8rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }

    /* Gaya untuk metrik khusus */
    .health-trend {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        font-weight: 400;
        font-size: 0.85rem;
    }
    .trend-positive { color: #34c759; }
    .trend-negative { color: #ff3b30; }

    /* Gaya untuk Alert */
    .alert-item {
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid;
    }
    .alert-critical { border-left-color: #ff3b30; background: color-mix(in srgb, #ff3b30 8%, transparent); }
    .alert-high { border-left-color: #ff9500; background: color-mix(in srgb, #ff9500 8%, transparent); }
    
    /* Menghilangkan padding dari kolom Streamlit untuk kontrol yang lebih baik di dalam widget */
    [data-testid="stHorizontalBlock"] {
        gap: 1.2rem;
    }

</style>
""", unsafe_allow_html=True)


# ======================================================================================
# 2. DATA MOCK & FUNGSI BANTU
# Ini mereplikasi data yang ditemukan di skrip JS
# ======================================================================================

# Data untuk Health Score Widget
health_score_data = {
    "This Month": {"score": 82, "trend": 1.5, "trend_label": "vs. last month", "labels": ["Week 1", "Week 2", "Week 3", "Week 4"], "values": [79, 80, 81, 82]},
    "Today": {"score": 84, "trend": 2.5, "trend_label": "vs. yesterday", "labels": ["9 AM", "1 PM", "5 PM", "9 PM"], "values": [78, 80, 81, 84]},
    "This Week": {"score": 85, "trend": 1.8, "trend_label": "vs. last week", "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"], "values": [79, 78, 80, 81, 85]},
    "This Quarter": {"score": 83, "trend": 3.2, "trend_label": "vs. last quarter", "labels": ["Jan", "Feb", "Mar"], "values": [76, 79, 83]},
    "This Year": {"score": 84, "trend": 4.1, "trend_label": "vs. last year", "labels": ["Q1", "Q2", "Q3", "Q4"], "values": [75, 77, 80, 84]},
    "All Periods": {"score": 83, "trend": 10.4, "trend_label": "over 5 years", "labels": ["2020", "2021", "2022", "2023", "2024"], "values": [71, 75, 78, 80, 83]}
}

# Fungsi untuk membuat grafik Plotly
def create_health_trend_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['labels'], y=data['values'],
        mode='lines',
        line=dict(color='#34c759', width=2),
        fill='tozeroy',
        fillcolor='rgba(52,199,89,0.1)'
    ))
    fig.update_layout(
        height=120, margin=dict(t=5, b=5, l=5, r=5),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=True, title_font_size=9),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    return fig

def create_sentiment_chart():
    fig = go.Figure(data=[go.Pie(
        labels=['Positive', 'Neutral', 'Negative'],
        values=[np.random.randint(60, 70), np.random.randint(20, 25), np.random.randint(10, 15)],
        hole=.75,
        marker_colors=['#34c759', '#a2a2a7', '#ff3b30'],
        textinfo='none'
    )])
    fig.update_layout(
        height=230, margin=dict(t=10, b=10, l=10, r=10),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_intent_chart():
    labels = ["Info Seeking", "Complaint", "Service Request", "Feedback"]
    values = [np.random.randint(35, 45), np.random.randint(20, 25), np.random.randint(18, 22), np.random.randint(10, 15)]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation='h',
        marker=dict(color='#007aff', line_width=0)
    ))
    fig.update_layout(
        height=230, margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(showgrid=False, showticklabels=True),
        yaxis=dict(showgrid=False),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig
    
def create_volume_chart():
    data = (np.sin(np.linspace(0, 8, 30)) * 150 + 500 + np.random.rand(30) * 50).tolist()
    labels = [f"Day {i+1}" for i in range(30)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=data,
        mode='lines',
        line=dict(color='#007aff', width=2),
        fill='tozeroy',
        fillcolor='rgba(0,122,255,0.1)'
    ))
    fig.update_layout(
        height=230, margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    return fig

def get_bot_response(msg):
    lm = msg.lower()
    if "health score" in lm:
        return "Customer Health Score is 82%, up 1.5% from last month. More details?"
    if "alerts" in lm:
        return "2 critical alerts: Mobile app sentiment spike & Churn risk from billing errors. Details or actions?"
    if "hotspots" in lm:
        return "Hotspots: Overdraft policy confusion (medium impact) & Intl. transfer UI issues (low impact). Explore further?"
    if "thank" in lm:
        return "You're welcome! Anything else?"
    return 'I can help with dashboard insights. Try "summarize alerts", or "top opportunities".'

# ======================================================================================
# 3. SIDEBAR
# Mereplikasi filter dan navigasi
# ======================================================================================

with st.sidebar:
    st.markdown("## VOCAL")
    st.markdown("---")

    # Time Filter
    time_filter = st.selectbox(
        "Time",
        options=["This Month", "Today", "This Week", "This Quarter", "This Year", "All Periods"],
        index=0
    )

    # Product Filter
    product_options = ["myBCA", "BCA Mobile", "KPR", "KKB", "KSM", "Investasi", "Asuransi", "Kartu Kredit"]
    product_filter = st.multiselect("Product", options=product_options, default=["myBCA", "BCA Mobile"])

    # Channel Filter
    channel_options = ["Social Media", "Call Center", "WhatsApp", "Webchat", "VIRA", "E-mail", "Survey Gallup"]
    channel_filter = st.multiselect("Channel", options=channel_options, default=["Social Media"])
    
    st.markdown("---")
    st.markdown("### Menu")
 
    # Menggunakan st.markdown untuk meniru tautan tanpa fungsionalitas navigasi
    # Ini akan mempertahankan tampilan visual tanpa menyebabkan error.
    st.markdown("📊 **Dashboard**")
    st.markdown("📈 Analytics")
    st.markdown("💬 Feedback")
    
    st.markdown("---")
    st.info("👤 **Account:** Sebastian (CX Manager)")


# ======================================================================================
# 4. KONTEN UTAMA
# Mereplikasi tata letak grid dan widget
# ======================================================================================

st.header("Customer Experience Health")
st.write("Real-time Insights & Performance Overview")
st.markdown("---")

# Baris pertama widget
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Customer Health Score")
        
        # Mengambil data berdasarkan filter waktu
        current_health_data = health_score_data[time_filter]
        
        # Metrik
        score = current_health_data['score']
        trend = current_health_data['trend']
        trend_label = current_health_data['trend_label']
        trend_class = "trend-positive" if trend >= 0 else "trend-negative"
        arrow = "↑" if trend >= 0 else "↓"
        
        st.markdown(f'''
        <div style="text-align: center;">
            <span style="font-size: 3rem; font-weight: 500; color: var(--accent-color);">{score}</span>
            <span style="font-size: 1.8rem; color: var(--text-secondary);">%</span>
            <div class="{trend_class} health-trend">
                <span>{arrow} {trend}% {trend_label}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # Grafik
        st.plotly_chart(create_health_trend_chart(current_health_data), use_container_width=True)
        
        st.info("Overall customer satisfaction is strong, showing a positive trend.", icon="✅")


with col2:
    with st.container(border=True):
        st.subheader("Critical Alerts")
        
        st.markdown("""
        <div class="alert-item alert-critical">
            <strong>Sudden Spike in Negative Sentiment</strong>
            <p class="metric-subtitle">Mobile App Update X.Y: 45% negative<br>Issues: Login Failed, App Crashing</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-item alert-high">
            <strong>High Churn Risk Pattern Detected</strong>
            <p class="metric-subtitle">Pattern: Repeated Billing Errors - Savings<br>12 unique customer patterns</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View All Alerts", use_container_width=True, type="primary"):
            st.toast("Navigating to all alerts...")


with col3:
    with st.container(border=True):
        st.subheader("Predictive Hotspots")

        st.warning("New Overdraft Policy Confusion (Medium Impact)")
        st.caption("'Confused' Language: +30% WoW")
        
        st.info("Intl. Transfer UI Issues (Low Impact)")
        st.caption("Task Abandonment: +15% MoM")
        
        if st.button("Create Action", use_container_width=True, type="primary"):
            st.toast("Opening action creation modal...")

# Widget lebar penuh - Customer Voice Snapshot
with st.container(border=True):
    st.subheader("Customer Voice Snapshot")
    snap_col1, snap_col2, snap_col3 = st.columns(3)
    
    with snap_col1:
        st.markdown("<div style='text-align: center'>Sentiment Distribution</div>", unsafe_allow_html=True)
        st.plotly_chart(create_sentiment_chart(), use_container_width=True)

    with snap_col2:
        st.markdown("<div style='text-align: center'>Intent Distribution</div>", unsafe_allow_html=True)
        st.plotly_chart(create_intent_chart(), use_container_width=True)

    with snap_col3:
        st.markdown("<div style='text-align: center'>Volume Trend (30 Days)</div>", unsafe_allow_html=True)
        st.plotly_chart(create_volume_chart(), use_container_width=True)

# Widget lebar penuh - Top Themes
with st.container(border=True):
    st.subheader("Top Customer Themes")
    theme_col1, theme_col2 = st.columns(2)

    with theme_col1:
        st.markdown("#### Top Positive Themes")
        st.success("✅ Fast Customer Service")
        st.success("✅ Easy Mobile Banking")
        st.success("✅ Helpful Staff")

    with theme_col2:
        st.markdown("#### Top Negative Themes")
        st.error("❌ App Technical Issues")
        st.error("❌ Long Wait Times (Call)")
        st.error("❌ Fee Transparency")


# ======================================================================================
# 5. CHATBOT
# Mereplikasi fungsionalitas chatbot menggunakan st.chat
# ======================================================================================
st.markdown("---")
st.subheader("🤖 Ask VIRA, your AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm VIRA. How can I help with the dashboard today?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about insights, alerts..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Menampilkan pesan loading dan mendapatkan respons
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_bot_response(prompt)
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


