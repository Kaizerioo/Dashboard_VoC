import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
from streamlit_option_menu import option_menu
from streamlit_chat import message
import streamlit.components.v1 as components

# Set page configuration
st.set_page_config(
    page_title="Voice of Customer Dashboard - Refined Aesthetics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match the original design
st.markdown("""
<style>
    /* Main colors and variables */
    :root {
        --accent-color: #007aff;
        --accent-color-darker: #005ecb;
        --text-primary: #1d1d1f;
        --text-secondary: #4a4a4f;
        --border-color: #d2d2d7;
        --light-border-color: #e5e5ea;
        --card-background: #ffffff;
    }

    /* Main container */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #fafafc;
    }

    /* Headers */
    h1, h2, h3 {
        color: var(--text-primary);
        font-weight: 600;
    }
    h1 {
        font-size: 1.7rem;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    h2 {
        font-size: 1.3rem;
        letter-spacing: -0.01em;
    }
    h3 {
        font-size: 1.05rem;
    }

    /* Dashboard header description */
    .header-desc {
        font-size: 1.05rem;
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
    }

    /* Cards */
    .css-1r6slb0 {
        border-radius: 14px;
        background-color: var(--card-background);
        padding: 1.2rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03), 0 5px 10px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
        border: none;
    }

    /* Widget filters styling */
    .stButton > button {
        background-color: transparent;
        color: var(--text-secondary);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        font-size: 0.78rem;
        padding: 0.4rem 0.8rem;
        margin-right: 0.3rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        border-color: color-mix(in srgb, var(--accent-color) 60%, transparent);
        color: var(--accent-color);
    }

    /* Active widget filter */
    .active-filter {
        background-color: var(--accent-color) !important;
        color: white !important;
        border-color: var(--accent-color) !important;
        font-weight: 500 !important;
    }

    /* Alert styling */
    .alert-item {
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-radius: 10px;
        background-color: var(--card-background);
        border-left: 4px solid;
    }
    .alert-critical {
        border-left-color: #ff3b30;
    }
    .alert-high {
        border-left-color: #ff9500;
    }
    .alert-icon {
        width: 0.6rem;
        height: 0.6rem;
        border-radius: 50%;
        flex-shrink: 0;
        margin-top: 0.3rem;
    }
    .alert-content h4 {
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 0.25rem;
        color: var(--text-primary);
    }

    /* Theme item styling */
    .theme-item {
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.6rem;
        border-radius: 10px;
        font-size: 0.78rem;
    }
    .positive-theme {
        background: rgba(52, 199, 89, 0.12);
        color: #2a703d;
        border: 1px solid rgba(52, 199, 89, 0.25);
    }
    .negative-theme {
        background: rgba(255, 59, 48, 0.12);
        color: #a12a22;
        border: 1px solid rgba(255, 59, 48, 0.25);
    }

    /* Quote styling */
    .quote-item {
        padding: 0.8rem;
        margin-top: 0.8rem;
        border-radius: 10px;
        background: rgba(0, 0, 0, 0.02);
        font-size: 0.78rem;
        color: var(--text-secondary);
        border: 1px solid var(--light-border-color);
        font-style: italic;
        line-height: 1.4;
    }

    /* Health score styling */
    .health-score {
        text-align: center;
        margin: 0.8rem 0;
    }
    .health-score-value {
        font-size: 3rem;
        font-weight: 500;
        color: var(--accent-color);
        margin-bottom: 0.1rem;
        line-height: 1;
    }
    .health-score-value span {
        font-size: 1.8rem;
        color: var(--text-secondary);
    }
    .health-trend {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        color: #34c759;
        font-weight: 400;
        font-size: 0.85rem;
    }
    .health-trend.negative {
        color: #ff3b30;
    }

    /* Metrics styling */
    .metrics-item {
        font-size: 0.78rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }

    /* Opportunity item styling */
    .opportunity-item {
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-radius: 10px;
        background: var(--card-background);
        border: 1px solid var(--light-border-color);
    }
    .opportunity-item h4 {
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 0.4rem;
    }

    /* Widget summary */
    .widget-summary {
        margin-top: 0.8rem;
        padding: 0.8rem;
        background: rgba(0, 0, 0, 0.02);
        border-radius: 10px;
        font-size: 0.85rem;
        color: var(--text-secondary);
        border: 1px solid var(--light-border-color);
        line-height: 1.45;
    }

    /* Impact indicators */
    .impact-indicator {
        padding: 0.25rem 0.6rem;
        border-radius: 14px;
        font-size: 0.7rem;
        font-weight: 500;
        display: inline-block;
    }
    .impact-medium {
        background: rgba(255, 149, 0, 0.18);
        color: #b36500;
    }
    .impact-low {
        background: rgba(52, 199, 89, 0.18);
        color: #2a703d;
    }

    /* Streamlit inputs styling */
    .stSelectbox, .stMultiSelect {
        border-radius: 10px;
    }

    /* Chat container styling */
    .chat-message {
        padding: 1rem;
        border-radius: 0.8rem;
        margin-bottom: 0.8rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message-content {
        border-radius: 0.8rem;
        padding: 0.7rem 1rem;
        max-width: 80%;
        font-size: 0.85rem;
        line-height: 1.45;
    }
    .user-message .chat-message-content {
        background-color: var(--accent-color);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 0.3rem;
    }
    .bot-message .chat-message-content {
        background-color: #e9e9ef;
        color: var(--text-primary);
        border-bottom-left-radius: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'time_filter' not in st.session_state:
    st.session_state.time_filter = 'month'
if 'product_filter' not in st.session_state:
    st.session_state.product_filter = ['all']
if 'channel_filter' not in st.session_state:
    st.session_state.channel_filter = ['all']
if 'health_widget_filter' not in st.session_state:
    st.session_state.health_widget_filter = 'Real-time'
if 'alerts_widget_filter' not in st.session_state:
    st.session_state.alerts_widget_filter = 'Critical'
if 'hotspots_widget_filter' not in st.session_state:
    st.session_state.hotspots_widget_filter = 'Emerging'
if 'snapshot_widget_filter' not in st.session_state:
    st.session_state.snapshot_widget_filter = 'Overview'
if 'themes_widget_filter' not in st.session_state:
    st.session_state.themes_widget_filter = 'Top 10'
if 'opportunity_widget_filter' not in st.session_state:
    st.session_state.opportunity_widget_filter = 'High Value'
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello! I'm VIRA your AI assistant. How can I help with the dashboard today?"}
    ]

# Health score data dictionary
health_score_data = {
    "today": {
        "labels": ["9 AM", "11 AM", "1 PM", "3 PM", "5 PM", "7 PM", "9 PM"],
        "values": [78, 76, 80, 79, 81, 83, 84],
        "score": 84,
        "trend": "+2.5%",
        "trend_positive": True,
        "trend_label": "vs. yesterday",
    },
    "week": {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "values": [79, 78, 80, 81, 83, 84, 85],
        "score": 85,
        "trend": "+1.8%",
        "trend_positive": True,
        "trend_label": "vs. last week",
    },
    "month": {
        "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "values": [79, 80, 81, 82],
        "score": 82,
        "trend": "+1.5%",
        "trend_positive": True,
        "trend_label": "vs. last month",
    },
    "quarter": {
        "labels": ["Jan", "Feb", "Mar"],
        "values": [76, 79, 83],
        "score": 83,
        "trend": "+3.2%",
        "trend_positive": True,
        "trend_label": "vs. last quarter",
    },
    "year": {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "values": [75, 77, 80, 84],
        "score": 84,
        "trend": "+4.1%",
        "trend_positive": True,
        "trend_label": "vs. last year",
    },
    "all": {
        "labels": ["2019", "2020", "2021", "2022", "2023", "2024"],
        "values": [73, 71, 75, 78, 80, 83],
        "score": 83,
        "trend": "+10.4%",
        "trend_positive": True,
        "trend_label": "over 5 years",
    }
}

# Sidebar
with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 1rem;'><h2>VOCAL</h2></div>", unsafe_allow_html=True)

    # Sidebar Navigation
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Analytics", "Feedback", "Alerts", "Reports"],
        icons=["graph-up", "bar-chart", "chat", "exclamation-triangle", "clipboard"],
        menu_icon="cast",
        default_index=0,
    )

    st.markdown("<div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(230, 230, 230, 0.4);'>"
               "<div style='font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em; "
               "color: rgba(255, 255, 255, 0.6); margin-bottom: 0.8rem;'>CUSTOMER INSIGHTS</div></div>", 
               unsafe_allow_html=True)

    insights_menu = option_menu(
        menu_title=None,
        options=["Sentiment Analysis", "Journey Mapping", "Satisfaction Scores", "Theme Analysis"],
        icons=["emoji-smile", "bullseye", "graph-up", "search"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "rgba(255, 255, 255, 0.8)", "font-size": "0.8rem"}, 
            "nav-link": {"font-size": "0.8rem", "text-align": "left", "margin": "0px", "--hover-color": "rgba(255, 255, 255, 0.1)"},
            "nav-link-selected": {"background-color": "#007aff", "font-weight": "normal"},
        }
    )

    st.markdown("<div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(230, 230, 230, 0.4);'>"
               "<div style='font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em; "
               "color: rgba(255, 255, 255, 0.6); margin-bottom: 0.8rem;'>OPERATIONS</div></div>", 
               unsafe_allow_html=True)

    operations_menu = option_menu(
        menu_title=None,
        options=["Real-time Monitoring", "Predictive Analytics", "Performance Metrics", "Action Items"],
        icons=["lightning", "magic", "graph-up", "bullseye"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "rgba(255, 255, 255, 0.8)", "font-size": "0.8rem"}, 
            "nav-link": {"font-size": "0.8rem", "text-align": "left", "margin": "0px", "--hover-color": "rgba(255, 255, 255, 0.1)"},
            "nav-link-selected": {"background-color": "#007aff", "font-weight": "normal"},
        }
    )

    # User profile display
    st.markdown("<div style='margin-top: auto; padding-top: 1rem; border-top: 1px solid rgba(230, 230, 230, 0.4);'></div>", 
               unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(
            f"""
            <div style="
                width: 2.25rem;
                height: 2.25rem;
                border-radius: 50%;
                background: linear-gradient(145deg, #007aff 0%, #005ecb 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 500;
                font-size: 0.9rem;
                margin-left: 0.5rem;
            ">SB</div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="margin-top: 0.25rem;">
                <div style="font-weight: 500; font-size: 0.9rem; color: white;">Sebastian</div>
                <div style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.7);">CX Manager</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Top header - Global Filters
st.markdown("<h1>Customer Experience Health</h1>", unsafe_allow_html=True)
st.markdown("<p class='header-desc'>Real-time Insights & Performance Overview</p>", unsafe_allow_html=True)

# Global filter row
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1, 1, 1, 1])

with filter_col1:
    st.markdown("<label style='font-size: 0.72rem; font-weight: 500; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.04em;'>Time</label>", unsafe_allow_html=True)
    time_options = {
        'all': 'All Periods',
        'today': 'Today',
        'week': 'This Week',
        'month': 'This Month',
        'quarter': 'This Quarter',
        'year': 'This Year'
    }
    time_filter = st.selectbox(
        label="Time Filter",
        options=list(time_options.keys()),
        format_func=lambda x: time_options[x],
        index=list(time_options.keys()).index('month'),
        label_visibility="collapsed"
    )
    st.session_state.time_filter = time_filter

with filter_col2:
    st.markdown("<label style='font-size: 0.72rem; font-weight: 500; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.04em;'>Product</label>", unsafe_allow_html=True)
    product_options = {
        'all': 'All Products',
        'mobile_mybca': 'myBCA',
        'savings_bcamobile': 'BCA Mobile',
        'loans_kpr': 'KPR',
        'loans_kkb': 'KKB',
        'loans_ksm': 'KSM',
        'investasi': 'Investasi',
        'asuransi': 'Asuransi',
        'loans_kmk': 'KMK',
        'kartu_kredit': 'Kartu Kredit',
        'edc_qris': 'EDC & QRIS',
        'poket_valas': 'Poket Valas'
    }
    product_filter = st.multiselect(
        label="Product Filter",
        options=list(product_options.keys()),
        format_func=lambda x: product_options[x],
        default=['all'],
        label_visibility="collapsed"
    )
    if not product_filter:
        product_filter = ['all']
    st.session_state.product_filter = product_filter

with filter_col3:
    st.markdown("<label style='font-size: 0.72rem; font-weight: 500; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.04em;'>Channel</label>", unsafe_allow_html=True)
    channel_options = {
        'all': 'All Channels',
        'social_media': 'Social Media',
        'call_center': 'Call Center',
        'whatsapp': 'WhatsApp',
        'webchat': 'Webchat',
        'vira': 'VIRA',
        'email': 'E-mail',
        'survey_gallup': 'Survey Gallup',
        'survey_bsq': 'Survey BSQ',
        'survey_cx': 'Survey CX'
    }
    channel_filter = st.multiselect(
        label="Channel Filter",
        options=list(channel_options.keys()),
        format_func=lambda x: channel_options[x],
        default=['all'],
        label_visibility="collapsed"
    )
    if not channel_filter:
        channel_filter = ['all']
    st.session_state.channel_filter = channel_filter

# Helper function to create widget filters
def create_widget_filters(options, active_filter, key_prefix):
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        is_active = option == active_filter
        button_style = "active-filter" if is_active else ""
        if cols[i].button(option, key=f"{key_prefix}_{i}", help=option, use_container_width=True):
            return option
    return active_filter

# Dashboard layout with cards
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.markdown("""
    <div style="border-bottom: 1px solid var(--light-border-color); padding-bottom: 0.8rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
        <h3>Customer Health Score</h3>
        <button style="background: rgba(0, 0, 0, 0.04); border: none; padding: 0.5rem 0.8rem; border-radius: 6px; font-size: 0.78rem; color: var(--text-secondary);">Export</button>
    </div>
    """, unsafe_allow_html=True)

    # Widget filters
    health_filter_options = ["Real-time", "Daily Trend", "Comparison"]
    health_widget_filter = create_widget_filters(health_filter_options, st.session_state.health_widget_filter, "health_filter")
    st.session_state.health_widget_filter = health_widget_filter

    # Get health score data based on selected time filter
    health_data = health_score_data.get(st.session_state.time_filter, health_score_data["month"])

    # Display health score
    st.markdown(f"""
    <div class="health-score">
        <div class="health-score-value">
            {health_data["score"]}<span>%</span>
        </div>
        <div class="health-trend {'negative' if not health_data['trend_positive'] else ''}">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">
                {'<line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline>' 
                  if health_data['trend_positive'] 
                  else '<line x1="12" y1="5" x2="12" y2="19"></line><polyline points="5 12 12 19 19 12"></polyline>'}
            </svg>
            <span>{health_data["trend"]} {health_data["trend_label"]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Health trend chart
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.plot(health_data["labels"], health_data["values"], color='#34c759', linewidth=2)
    ax.fill_between(health_data["labels"], health_data["values"], min(health_data["values"])-2, color='#34c759', alpha=0.15)
    ax.set_ylim(min(health_data["values"])-2, max(health_data["values"])+2)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    st.pyplot(fig)

    st.markdown("""
    <div class="widget-summary">
        Overall customer satisfaction is strong, showing a positive trend this month.
    </div>
    """, unsafe_allow_html=True)

# Critical Alerts Widget
with row1_col2:
    st.markdown("""
    <div style="border-bottom: 1px solid var(--light-border-color); padding-bottom: 0.8rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
        <h3>Critical Alerts</h3>
        <button style="background: linear-gradient(180deg, #007aff 0%, #005ecb 100%); border: none; padding: 0.5rem 0.8rem; border-radius: 6px; font-size: 0.78rem; color: white;">Acknowledge All</button>
    </div>
    """, unsafe_allow_html=True)

    # Widget filters
    alert_filter_options = ["Critical", "High", "Medium", "All"]
    alerts_widget_filter = create_widget_filters(alert_filter_options, st.session_state.alerts_widget_filter, "alert_filter")
    st.session_state.alerts_widget_filter = alerts_widget_filter

    # Alert items
    st.markdown("""
    <div class="alert-item alert-critical">
        <div class="alert-icon" style="background: #ff3b30;"></div>
        <div class="alert-content">
            <h4>Sudden Spike in Negative Sentiment</h4>
            <div class="metrics-item">
                Mobile App Update X.Y: 45% negative<br />
                Volume: 150 mentions / 3 hrs<br />
                Issues: Login Failed, App Crashing
            </div>
        </div>
    </div>

    <div class="alert-item alert-high">
        <div class="alert-icon" style="background: #ff9500;"></div>
        <div class="alert-content">
            <h4>High Churn Risk Pattern Detected</h4>
            <div class="metrics-item">
                Pattern: Repeated Billing Errors - Savings<br />
                12 unique customer patterns<br />
                Avg. sentiment: -0.8
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.button("View All Alerts", use_container_width=True)

# Predictive Hotspots Widget
with row1_col3:
    st.markdown("""
    <div style="border-bottom: 1px solid var(--light-border-color); padding-bottom: 0.8rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
        <h3>Predictive Hotspots</h3>
        <button style="background: linear-gradient(180deg, #007aff 0%, #005ecb 100%); border: none; padding: 0.5rem 0.8rem; border-radius: 6px; font-size: 0.78rem; color: white;">Create Action</button>
    </div>
    """, unsafe_allow_html=True)

    # Widget filters
    hotspot_filter_options = ["Emerging", "Trending", "Predicted"]
    hotspots_widget_filter = create_widget_filters(hotspot_filter_options, st.session_state.hotspots_widget_filter, "hotspot_filter")
    st.session_state.hotspots_widget_filter = hotspots_widget_filter

    # Hotspot items
    st.markdown("""
    <div class="hotspot-item">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <h4>New Overdraft Policy Confusion</h4>
            <span class="impact-indicator impact-medium">Medium Impact</span>
        </div>
        <div class="metrics-item">
            'Confused' Language: +30% WoW<br />
            Keywords: "don't understand", "how it works"
        </div>
    </div>

    <div class="hotspot-item">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <h4>Intl. Transfer UI Issues</h4>
            <span class="impact-indicator impact-low">Low Impact</span>
        </div>
        <div class="metrics-item">
            Task Abandonment: +15% MoM<br />
            Negative sentiment: 'Beneficiary Setup'
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="widget-summary">
        Monitor emerging confusion on overdrafts and usability for international transfers.
    </div>
    """, unsafe_allow_html=True)

# Customer Voice Snapshot Widget (Full Width)
st.markdown("""
<div style="border-bottom: 1px solid var(--light-border-color); padding-bottom: 0.8rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
    <h3>Customer Voice Snapshot</h3>
    <div>
        <button style="background: rgba(0, 0, 0, 0.04); border: none; padding: 0.5rem 0.8rem; border-radius: 6px; font-size: 0.78rem; color: var(--text-secondary); margin-right: 0.5rem;">Drill Down</button>
        <button style="background: rgba(0, 0, 0, 0.04); border: none; padding: 0.5rem 0.8rem; border-radius: 6px; font-size: 0.78rem; color: var(--text-secondary);">Export</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Widget filters
snapshot_filter_options = ["Overview", "Sentiment", "Intent", "Volume"]
snapshot_widget_filter = create_widget_filters(snapshot_filter_options, st.session_state.snapshot_widget_filter, "snapshot_filter")
st.session_state.snapshot_widget_filter = snapshot_widget_filter

# Charts for Customer Voice Snapshot
snapshot_col1, snapshot_col2, snapshot_col3 = st.columns(3)

with snapshot_col1:
    st.markdown("<h4 style='margin-bottom: 0.8rem; font-weight: 400; font-size: 0.95rem; color: var(--text-secondary);'>Sentiment Distribution</h4>", unsafe_allow_html=True)

    # Calculate sentiment distribution based on filters
    pM = 1 if 'all' in st.session_state.product_filter else 0.8
    sentiment_data = {
        'Category': ['Positive', 'Neutral', 'Negative'],
        'Value': [
            (60 + random.random() * 10) * pM,
            (20 + random.random() * 5) * pM,
            (10 + random.random() * 5) * pM
        ]
    }
    sentiment_df = pd.DataFrame(sentiment_data)

    # Create pie chart
    fig = px.pie(
        sentiment_df, 
        values='Value', 
        names='Category',
        color='Category',
        color_discrete_map={'Positive': '#34c759', 'Neutral': '#a2a2a7', 'Negative': '#ff3b30'},
        hole=0.7
    )
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        font=dict(size=10),
        height=230
    )
    st.plotly_chart(fig, use_container_width=True)

with snapshot_col2:
    st.markdown("<h4 style='margin-bottom: 0.8rem; font-weight: 400; font-size: 0.95rem; color: var(--text-secondary);'>Intent Distribution</h4>", unsafe_allow_html=True)

    # Create intent data
    intent_data = {
        'Category': ['Info Seeking', 'Complaint', 'Service Request', 'Feedback'],
        'Value': [
            35 + random.random() * 10,
            20 + random.random() * 5,
            20 + random.random() * 5,
            10 + random.random() * 5
        ]
    }
    intent_df = pd.DataFrame(intent_data)

    # Create horizontal bar chart
    fig = px.bar(
        intent_df,
        x='Value',
        y='Category',
        orientation='h',
        color='Category',
        color_discrete_map={
            'Info Seeking': '#007aff',
            'Complaint': '#ff9500',
            'Service Request': '#5856d6',
            'Feedback': '#ffcc00'
        }
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=False),
        font=dict(size=10),
        height=230
    )
    fig.update_traces(marker_line_width=0, marker_line_color='white')
    st.plotly_chart(fig, use_container_width=True)

with snapshot_col3:
    st.markdown("<h4 style='margin-bottom: 0.8rem; font-weight: 400; font-size: 0.95rem; color: var(--text-secondary);'>Volume Trend (30 Days)</h4>", unsafe_allow_html=True)

    # Create volume data
    cF = 1 if 'all' in st.session_state.channel_filter else (0.6 if 'social_media' in st.session_state.channel_filter else 0.9)
    days = list(range(1, 31))
    volume_values = [(400 + random.random() * 300 + i * 5) * cF for i in range(30)]

    volume_data = {
        'Day': days,
        'Volume': volume_values
    }
    volume_df = pd.DataFrame(volume_data)

    # Create area chart
    fig = px.area(
        volume_df,
        x='Day',
        y='Volume',
        line_shape='spline'
    )
    fig.update_traces(
        line_color='#007aff',
        fill='tozeroy',
        fillcolor='rgba(0, 122, 255, 0.18)'
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(showgrid=False, tickmode='linear', dtick=5),
        yaxis=dict(showgrid=True),
        font=dict(size=10),
        height=230
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="widget-summary">
    Positive sentiment leads at 65%. Information-seeking is top intent (40%). Volume shows steady increase.
</div>
""", unsafe_allow_html=True)

# Top Customer Themes Widget (Full Width)
st.markdown("""
<div style="border-bottom: 1px solid var(--light-border-color); padding-bottom: 0.8rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
    <h3>Top Customer Themes</h3>
    <button style="background: linear-gradient(180deg, #007aff 0%, #005ecb 100%); border: none; padding: 0.5rem 0.8rem; border-radius: 6px; font-size: 0.78rem; color: white;">Analyze Themes</button>
</div>
""", unsafe_allow_html=True)

# Widget filters
themes_filter_options = ["Top 10", "Trending", "Emerging", "Declining"]
themes_widget_filter = create_widget_filters(themes_filter_options, st.session_state.themes_widget_filter, "themes_filter")
st.session_state.themes_widget_filter = themes_widget_filter

# Theme lists in two columns
theme_col1, theme_col2 = st.columns(2)

with theme_col1:
    st.markdown("<h4 style='color: #34c759; padding-bottom: 0.5rem;'>Top Positive Themes</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div class="theme-item positive-theme">Fast Customer Service</div>
    <div class="theme-item positive-theme">Easy Mobile Banking</div>
    <div class="theme-item positive-theme">Helpful Staff</div>
    <div class="quote-item">"Support resolved my issue in minutes! So efficient."</div>
    """, unsafe_allow_html=True)

with theme_col2:
    st.markdown("<h4 style='color: #ff3b30; padding-bottom: 0.5rem;'>Top Negative Themes</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div class="theme-item negative-theme">App Technical Issues</div>
    <div class="theme-item negative-theme">Long Wait Times (Call)</div>
    <div class="theme-item negative-theme">Fee Transparency</div>
    <div class="quote-item">"The app keeps crashing after the latest update. Very frustrating."</div>
    """, unsafe_allow_html=True)

# Opportunity Radar Widget (Full Width)
st.markdown("""
<div style="border-bottom: 1px solid var(--light-border-color); padding-bottom: 0.8rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
    <h3>Opportunity Radar</h3>
    <button style="background: linear-gradient(180deg, #007aff 0%, #005ecb 100%); border: none; padding: 0.5rem 0.8rem; border-radius: 6px; font-size: 0.78rem; color: white;">Prioritize</button>
</div>
""", unsafe_allow_html=True)

# Widget filters
opportunity_filter_options = ["High Value", "Quick Wins", "Strategic"]
opportunity_widget_filter = create_widget_filters(opportunity_filter_options, st.session_state.opportunity_widget_filter, "opportunity_filter")
st.session_state.opportunity_widget_filter = opportunity_widget_filter

# Opportunity grid
opportunity_col1, opportunity_col2, opportunity_col3 = st.columns(3)

with opportunity_col1:
    st.markdown("""
    <div class="opportunity-item">
        <h4>🎉 Delightful: Instant Card Activation</h4>
        <div class="metrics-item">
            75 delight mentions this week (Sentiment: +0.95)<br />
            Keywords: "amazing", "so easy", "instant"<br />
            <strong>Action:</strong> Amplify in marketing? Benchmark?
        </div>
    </div>
    """, unsafe_allow_html=True)

with opportunity_col2:
    st.markdown("""
    <div class="opportunity-item">
        <h4>💰 Cross-Sell: Mortgage Inquiries +15%</h4>
        <div class="metrics-item">
            Mortgage info seeking: +15% WoW<br />
            Related: Savings, Financial Planning<br />
            <strong>Action:</strong> Target with relevant mortgage info?
        </div>
    </div>
    """, unsafe_allow_html=True)

with opportunity_col3:
    st.markdown("""
    <div class="opportunity-item">
        <h4>⭐ Service Excellence: Complex Issues</h4>
        <div class="metrics-item">
            25 positive mentions for complex issue resolution<br />
            Agents: A, B, C praised.<br />
            <strong>Action:</strong> Identify best practices? Recognize agents?
        </div>
    </div>
    """, unsafe_allow_html=True)

# Add the chatbot in the expander at the bottom
with st.expander("VIRA - AI Assistant", expanded=False):
    # Display chat messages
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="chat-message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="chat-message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Get user input
    user_input = st.text_input("Ask about insights, alerts...", key="user_input")

    # Handle user input
    if user_input:
        # Add user message to chat history
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        # Generate bot response based on input
        bot_response = get_bot_response(user_input)

        # Add bot response to chat history
        st.session_state.chat_messages.append({"role": "assistant", "content": bot_response})

        # Rerun to display the new messages
        st.experimental_rerun()

# Bot response function
def get_bot_response(message):
    message = message.lower()

    if "health score" in message:
        return "Customer Health Score is 82%, up 1.5% from last month. More details?"

    elif "alerts" in message:
        return "2 critical alerts: Mobile app sentiment spike & Churn risk from billing errors. Details or actions?"

    elif "hotspots" in message:
        return "Hotspots: Overdraft policy confusion (medium impact) & Intl. transfer UI issues (low impact). Explore further?"

    elif "opportunities" in message:
        return "Opportunities: Promote instant card activation, target mortgage inquiries, scale service excellence. Interested in one?"

    elif "thank" in message:
        return "You're welcome! Anything else?"

    else:
        return 'I can help with dashboard insights. Try "health score trends", "summarize alerts", or "top opportunities".'
    
