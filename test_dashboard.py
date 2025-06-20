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

# <-- PERUBAHAN: Menambahkan aturan CSS untuk sidebar sticky -->
st.markdown("""
<style>
    /* ... [ SEMUA GAYA CSS DARI SEBELUMNYA TETAP DI SINI ] ... */
    :root {
        --font-family-apple: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        --card-background: #ffffff;
        --text-primary: #1d1d1f;
        --text-secondary: #4a4a4f;
        --accent-color: #007aff;
    }
    body {
        font-family: var(--font-family-apple);
        background-color: #f2f4f6;
    }
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--card-background);
        border-radius: 14px;
        padding: 1rem 1.2rem 1.2rem 1.2rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03), 0 5px 10px rgba(0, 0, 0, 0.06);
        border: 1px solid #d2d2d7;
    }
    h3 {
        font-size: 1.05rem;
        font-weight: 500;
        color: var(--text-primary);
        letter-spacing: -0.01em;
        margin-bottom: 0.5rem;
    }
    [data-testid="stHorizontalBlock"] {
        gap: 1.2rem;
    }
    
    /* === CSS BARU UNTUK MEMBUAT SIDEBAR KANAN STICKY === */
    /* Ini menargetkan kolom kedua dari tata letak utama */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
        position: sticky;
        top: 60px; /* Jarak dari atas viewport */
        height: 90vh; /* Tinggi maksimum adalah 90% dari tinggi layar */
        overflow-y: auto; /* Tambahkan scrollbar internal jika konten chatbot panjang */
    }
</style>
""", unsafe_allow_html=True)


# ======================================================================================
# 2. DATA MOCK & FUNGSI BANTU
# ======================================================================================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm VIRA. How can I help?"}]

# ... [FUNGSI DATA MOCK & GRAFIK DARI SEBELUMNYA TETAP SAMA] ...
health_score_data = {
    "This Month": {"score": 82, "trend": 1.5, "trend_label": "vs. last month", "labels": ["Week 1", "Week 2", "Week 3", "Week 4"], "values": [79, 80, 81, 82]},
    "Today": {"score": 84, "trend": 2.5, "trend_label": "vs. yesterday", "labels": ["9 AM", "1 PM", "5 PM", "9 PM"], "values": [78, 80, 81, 84]},
    "This Week": {"score": 85, "trend": 1.8, "trend_label": "vs. last week", "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"], "values": [79, 78, 80, 81, 85]},
    "This Quarter": {"score": 83, "trend": 3.2, "trend_label": "vs. last quarter", "labels": ["Jan", "Feb", "Mar"], "values": [76, 79, 83]},
    "This Year": {"score": 84, "trend": 4.1, "trend_label": "vs. last year", "labels": ["Q1", "Q2", "Q3", "Q4"], "values": [75, 77, 80, 84]},
    "All Periods": {"score": 83, "trend": 10.4, "trend_label": "over 5 years", "labels": ["2020", "2021", "2022", "2023", "2024"], "values": [71, 75, 78, 80, 83]}
}

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
# 3. SIDEBAR KIRI (NAVIGASI & FILTER)
# ======================================================================================
with st.sidebar:
    st.markdown("## VOCAL")
    st.markdown("---")

    # Filter
    time_filter = st.selectbox("Time", options=["This Month", "Today", "This Week", "This Quarter", "This Year", "All Periods"], index=0)
    product_options = ["myBCA", "BCA Mobile", "KPR", "KKB", "KSM", "Investasi", "Asuransi", "Kartu Kredit"]
    product_filter = st.multiselect("Product", options=product_options, default=["myBCA", "BCA Mobile"])
    channel_options = ["Social Media", "Call Center", "WhatsApp", "Webchat", "VIRA", "E-mail", "Survey Gallup"]
    channel_filter = st.multiselect("Channel", options=channel_options, default=["Social Media"])
    
    st.markdown("---")
    st.markdown("### Menu")
    st.markdown("📊 **Dashboard**")
    st.markdown("📈 Analytics")
    st.markdown("💬 Feedback")
    
    st.markdown("---")
    st.info("👤 **Account:** Sebastian (CX Manager)")


# ======================================================================================
# 4. TATA LETAK UTAMA DENGAN KOLOM KANAN
# ======================================================================================

st.header("Customer Experience Health")
st.write("Real-time Insights & Performance Overview")

main_content, chat_sidebar = st.columns([2.5, 1], gap="large")

# Semua konten dasbor sekarang masuk ke kolom 'main_content'
with main_content:
    st.markdown("---")
    # Baris pertama widget
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("Customer Health Score")
            current_health_data = health_score_data[time_filter]
            score = current_health_data['score']
            trend = current_health_data['trend']
            trend_label = current_health_data['trend_label']
            
            st.metric(
                label="Real-time Score", 
                value=f"{score}%", 
                delta=f"{trend}% {trend_label}"
            )
            st.plotly_chart(create_health_trend_chart(current_health_data), use_container_width=True)
            st.info("Overall customer satisfaction is strong.", icon="✅")

    with col2:
        with st.container(border=True):
            st.subheader("Critical Alerts")
            st.error("Spike in Negative Sentiment: 45% neg.")
            st.warning("High Churn Risk Pattern Detected.")
            if st.button("View All Alerts", use_container_width=True, type="primary"):
                st.toast("Navigating to all alerts...")

    with col3:
        with st.container(border=True):
            st.subheader("Predictive Hotspots")
            st.warning("New Overdraft Policy Confusion")
            st.info("Intl. Transfer UI Issues")
            if st.button("Create Action", use_container_width=True, type="primary"):
                st.toast("Opening action creation modal...")

    # Widget lebar penuh - Customer Voice Snapshot
    with st.container(border=True):
        st.subheader("Customer Voice Snapshot")
        snap_col1, snap_col2, snap_col3 = st.columns(3)
        with snap_col1:
            st.markdown("<div style='text-align: center'>Sentiment</div>", unsafe_allow_html=True)
            st.plotly_chart(create_sentiment_chart(), use_container_width=True)
        with snap_col2:
            st.markdown("<div style='text-align: center'>Intent</div>", unsafe_allow_html=True)
            st.plotly_chart(create_intent_chart(), use_container_width=True)
        with snap_col3:
            st.markdown("<div style='text-align: center'>Volume Trend</div>", unsafe_allow_html=True)
            st.plotly_chart(create_volume_chart(), use_container_width=True)
            
    # Widget lebar penuh - Top Themes
    with st.container(border=True):
        st.subheader("Top Customer Themes")
        theme_col1, theme_col2 = st.columns(2)
        with theme_col1:
            st.markdown("#### Top Positive Themes")
            st.success("✅ Fast Customer Service")
            st.success("✅ Easy Mobile Banking")
        with theme_col2:
            st.markdown("#### Top Negative Themes")
            st.error("❌ App Technical Issues")
            st.error("❌ Long Wait Times (Call)")


# Logika chatbot sekarang ada di dalam kolom 'chat_sidebar'
with chat_sidebar:
    # Menggunakan st.container untuk memberikan latar belakang dan border
    with st.container(border=True):
        st.markdown("<h5>🤖 VIRA AI Assistant</h5>", unsafe_allow_html=True)
        
        # Tampilkan riwayat obrolan
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Input dari pengguna
        if prompt := st.chat_input("Ask about insights..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_bot_response(prompt)
                    st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
