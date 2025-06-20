# -*- coding: utf-8 -*-
"""
main.py

A Streamlit web application for a Voice of Customer (VOC) Dashboard.

This application visualizes customer interaction data from various channels,
displaying metrics on customer health, sentiment, intent, and volume. It features
interactive filters and an AI-powered chat assistant (VIRA) in a right-hand sidebar.
"""

# --- IMPORTS ---
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from openai import OpenAI
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- CONFIGURATION ---

# Streamlit Page Configuration
st.set_page_config(
    page_title="Voice of Customer Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed" # Sidebar default disembunyikan karena tidak digunakan
)

# Google Sheets API Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1V5cRgnnN5GTFsD9bR05hLzsKRWkhdEy3LhuTvSnUyIM' # Replace with your actual Spreadsheet ID
RANGE_NAME = 'sheet1!A:H'

# NVIDIA API Configuration
NVIDIA_API_KEY = "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" # Replace with your NVIDIA API key or use st.secrets
SYSTEM_PROMPT_VIRA = """
Anda adalah VIRA, seorang konsultan virtual untuk Bank BCA.
Tugas utama Anda adalah menganalisis data dasbor yang disediakan dan memberikan wawasan, ringkasan, serta saran yang relevan.
Fokuslah pada metrik seperti skor kesehatan (jika ada), tren, sentimen pelanggan, niat panggilan, dan volume panggilan berdasarkan data yang disaring.
Selalu dasarkan jawaban Anda pada data yang diberikan dalam `dashboard_state`.
Gunakan bahasa Indonesia yang sopan dan mudah dimengerti.
Jika ada pertanyaan yang tidak dapat dijawab dari data dasbor, sampaikan dengan sopan bahwa informasi tersebut tidak tersedia dalam tampilan dasbor saat ini atau minta pengguna untuk memberikan detail lebih lanjut.
Berikan analisis yang ringkas namun mendalam.
Jika ada pertanyaan yang diluar konteks analisis anda, sampaikan bahwa itu diluar kapabilitas anda untuk menjelaskannya.
PENTING:
Sebelum memberikan jawaban akhir kepada pengguna, Anda BOLEH melakukan analisis internal atau "berpikir".
Jika Anda melakukan proses berpikir internal, *JANGAN* tuliskan pemikiran tersebut.
Jika tidak ada proses berpikir khusus atau analisis internal yang perlu dituliskan, langsung berikan jawaban.
"""

# --- CUSTOM STYLING (CSS) ---
st.markdown("""
<style>
    /* Hide default sidebar */
    .css-1d391kg {
        display: none;
    }
    .stApp {
        background-color: #f5f5f7;
        color: #1d1d1f;
    }
    .stButton>button {
        background-color: #007aff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #005bb5;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        height: 100%;
    }
    .metric-title {
        font-size: 18px;
        font-weight: bold;
        color: #1d1d1f;
    }
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #1d1d1f;
    }
    .metric-trend-positive {
        color: #34c759;
        font-size: 16px;
        font-weight: 500;
    }
    .metric-trend-negative {
        color: #ff3b30;
        font-size: 16px;
        font-weight: 500;
    }
    /* Style for the new right-hand chat sidebar */
    .chat-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        height: 100vh; /* Make it full height */
        overflow-y: auto; /* Allow scrolling within the chat */
    }
    .navbar-item {
        padding: 10px;
        border-radius: 8px;
        background-color: #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)


# --- DATA LOADING ---

@st.cache_data(ttl=600)
def load_data_from_google_sheets():
    try:
        # Access individual fields from the TOML table
        gcp_creds_table = st.secrets["gcp_service_account_credentials"]

        # Reconstruct the JSON structure expected by from_service_account_info
        creds_info = {
            "type": gcp_creds_table["type"],
            "project_id": gcp_creds_table["project_id"],
            "private_key_id": gcp_creds_table["private_key_id"],
            "private_key": gcp_creds_table["private_key"].replace('\\n', '\n'),
            "private_key": gcp_creds_table["private_key"].replace('\\n', '\n'), # Important: unescape \n for from_service_account_info
            "client_email": gcp_creds_table["client_email"],
            "client_id": gcp_creds_table["client_id"],
            "auth_uri": gcp_creds_table["auth_uri"],
            "token_uri": gcp_creds_table["token_uri"],
            "auth_provider_x509_cert_url": gcp_creds_table["auth_provider_x509_cert_url"],
            "client_x509_cert_url": gcp_creds_table["client_x509_cert_url"],
            "universe_domain": gcp_creds_table["universe_domain"]
        }
        creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values or len(values) < 2: # Check for header and at least one data row
            st.error("No data or only header found in the Google Sheet.")
            return pd.DataFrame(columns=['Date', 'Product', 'Channel', 'Sentimen', 'Intent', 'Interaction ID', 'Details', 'Customer ID']) # Ensure essential columns exist

        df = pd.DataFrame(values[1:], columns=values[0])

        # Standardize column names and types
        expected_columns = {
            'Date': 'datetime64[ns]',
            'Product': 'str',
            'Channel': 'str',
            'Sentimen': 'str',
            'Intent': 'str',
            'Interaction ID': 'str',
            'Details': 'str',
            'Customer ID': 'str'
        }
        # Ensure all expected columns exist, fill with NA if not
        for col, dtype in expected_columns.items():
            if col not in df.columns:
                df[col] = pd.NA
            if col == 'Date':
                 # Attempt to parse 'Date' with multiple formats
                try:
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce') # General parser first
                except Exception: # If general fails, try specific
                    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
        creds = service_account.Credentials.from_service_account_info(
            creds_info, scopes=SCOPES)

        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            st.error("No data found in the Google Sheet.")
            return pd.DataFrame()
        else:
            df = pd.DataFrame(values[1:], columns=values[0])
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
                df.dropna(subset=['Date'], inplace=True)
            elif col in ['Product', 'Channel']:
                df[col] = df[col].astype(str).str.lower().str.replace(" ", "_").str.strip()
            elif col == 'Sentimen':
                df[col] = df[col].astype(str).str.capitalize().str.strip()
                # Standardize sentiment values
                sentiment_mapping = {
                    "Positive": "Positif", "Positive ": "Positif",
                    "Negative": "Negatif", "Negative ": "Negatif",
                    "Neutral": "Netral", "Neutral ": "Netral",
                }
                df['Sentimen'] = df['Sentimen'].replace(sentiment_mapping)
            else:
                df[col] = df[col].astype(str).str.strip()
        return df
                st.warning("Column 'Date' not found in Google Sheet. Time filtering will not work correctly.")
            if 'Product' in df.columns:
                df['Product'] = df['Product'].astype(str).str.lower().str.replace(" ", "_")
            if 'Channel' in df.columns:
                df['Channel'] = df['Channel'].astype(str).str.lower().str.replace(" ", "_")
            if 'Sentimen' in df.columns:
                df['Sentimen'] = df['Sentimen'].astype(str).str.capitalize()
            if 'Intent' in df.columns:
                df['Intent'] = df['Intent'].astype(str)
            return df
    except KeyError as e:
        st.error(f"Missing secret: {e}. Please ensure 'gcp_service_account_credentials' and potentially 'google_sheets' config are set in your Streamlit secrets.")
        return pd.DataFrame(columns=['Date', 'Product', 'Channel', 'Sentimen', 'Intent']) # Return empty DF with expected columns
        st.error(f"Missing secret: {e}. Please ensure 'gcp_service_account_credentials' is set in your Streamlit secrets.")
        return pd.DataFrame()
    except json.JSONDecodeError:
        st.error("Error decoding GCP credentials from Streamlit secrets. Please check the format in secrets.toml.")
        return pd.DataFrame(columns=['Date', 'Product', 'Channel', 'Sentimen', 'Intent'])
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data from Google Sheets: {e}")
        # Log full error for debugging if needed: print(f"Full GSheets Error: {e}", file=sys.stderr)
        return pd.DataFrame(columns=['Date', 'Product', 'Channel', 'Sentimen', 'Intent'])
        return pd.DataFrame()
@st.cache_data
def generate_health_score_data():
    """Generates static sample data for the Customer Health Score."""
    return {
        "today": {"labels": ["9 AM", "11 AM", "1 PM", "3 PM", "5 PM", "7 PM", "9 PM"], "values": [78, 76, 80, 79, 81, 83, 84], "score": 84, "trend": "+2.5%", "trend_positive": True, "trend_label": "vs. yesterday"},
        "week": {"labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "values": [79, 78, 80, 81, 83, 84, 85], "score": 85, "trend": "+1.8%", "trend_positive": True, "trend_label": "vs. last week"},
        "month": {"labels": ["Week 1", "Week 2", "Week 3", "Week 4"], "values": [79, 80, 81, 82], "score": 82, "trend": "+1.5%", "trend_positive": True, "trend_label": "vs. last month"},
        "quarter": {"labels": ["Jan", "Feb", "Mar"], "values": [76, 79, 83], "score": 83, "trend": "+3.2%", "trend_positive": True, "trend_label": "vs. last quarter"},
        "year": {"labels": ["Q1", "Q2", "Q3", "Q4"], "values": [75, 77, 80, 84], "score": 84, "trend": "+4.1%", "trend_positive": True, "trend_label": "vs. last year"},
        "all": {"labels": ["2019", "2020", "2021", "2022", "2023", "2024"], "values": [73, 71, 75, 78, 80, 83], "score": 83, "trend": "+10.4%", "trend_positive": True, "trend_label": "over 5 years"},
    }


# --- AI ASSISTANT SETUP ---

def initialize_llm_client():
    """Initializes and returns the OpenAI client for NVIDIA API."""
    return OpenAI(
        [span_43](start_span)base_url="https://integrate.api.nvidia.com/v1", #[span_43](end_span)
        [span_44](start_span)api_key=NVIDIA_API_KEY #[span_44](end_span)
    )

def generate_llm_response(client, user_prompt: str, dashboard_state: dict):
    """
    Generates a streamed response from the LLM based on the user prompt and dashboard state.

    Args:
        client: The initialized OpenAI client.
        user_prompt (str): The user's question.
        dashboard_state (dict): A dictionary summarizing the current dashboard view.

    Yields:
        str: Chunks of the response from the LLM.
    """
    dashboard_summary = f"""
    Ringkasan tampilan dasbor saat ini:
    - Periode: {dashboard_state.get('time_period_label_llm', 'N/A')}
    - Skor Kesehatan: {dashboard_state.get('score', 'N/A')}% (Tren: {dashboard_state.get('trend', 'N/A')})
    - Total Interaksi: {dashboard_state.get('total_interactions', 'N/A')}
    - Distribusi Sentimen: {'; '.join([f'{k}: {v}' for k, v in dashboard_state.get('sentiment_summary', {}).items()]) if dashboard_state.get('sentiment_summary') else 'Tidak ada data.'}
    - Distribusi Niat: {'; '.join([f'{k}: {v}' for k, v in dashboard_state.get('intent_summary', {}).items()]) if dashboard_state.get('intent_summary') else 'Tidak ada data.'}
    - Ringkasan Volume: {dashboard_state.get('volume_summary', 'N/A')}
    [span_45](start_span)""" #[span_45](end_span)
    messages = [
        [span_46](start_span){"role": "system", "content": SYSTEM_PROMPT_VIRA}, #[span_46](end_span)
        [span_47](start_span){"role": "user", "content": f"{dashboard_summary}\n\nPertanyaan Pengguna: \"{user_prompt}\""} #[span_47](end_span)
    ]

    try:
        completion = client.chat.completions.create(
            [span_48](start_span)model="nvidia/llama-3.1-nemotron-nano-vl-8b-v1", #[span_48](end_span)
            [span_49](start_span)messages=messages, #[span_49](end_span)
            [span_50](start_span)temperature=0.5, #[span_50](end_span)
            [span_51](start_span)top_p=0.7, #[span_51](end_span)
            [span_52](start_span)max_tokens=1024, #[span_52](end_span)
            [span_53](start_span)stream=True #[span_53](end_span)
        )
        [span_54](start_span)for chunk in completion: #[span_54](end_span)
            [span_55](start_span)if chunk.choices[0].delta and chunk.choices[0].delta.content is not None: #[span_55](end_span)
                [span_56](start_span)yield chunk.choices[0].delta.content #[span_56](end_span)
    [span_57](start_span)except Exception as e: #[span_57](end_span)
        error_message = f"Maaf, terjadi kesalahan saat menghubungi layanan AI: {str(e)}. Silakan coba lagi nanti." [span_58](start_span)#
        st.error(error_message)
        yield ""

# --- CHARTING FUNCTIONS ---

def create_health_score_chart(data):
    """Creates the Plotly figure for the health score chart."""
    fig = go.Figure() #[span_58](end_span)
    fig.add_trace(go.Scatter(
        [span_59](start_span)x=data["labels"], y=data["values"], mode='lines', fill='tozeroy', #[span_59](end_span)
        [span_60](start_span)fillcolor='rgba(52,199,89,0.18)', line=dict(color='#34c759', width=2.5) #[span_60](end_span)
    ))
    fig.update_layout(
        [span_61](start_span)height=150, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', #[span_61](end_span)
        [span_62](start_span)plot_bgcolor='rgba(0,0,0,0)', #[span_62](end_span)
        [span_63](start_span)xaxis=dict(showgrid=False, showticklabels=True, tickfont=dict(color='#4a4a4f', size=10)), #[span_63](end_span)
        [span_64](start_span)yaxis=dict(showgrid=True, gridcolor='#e5e5ea', showticklabels=True, tickfont=dict(color='#4a4a4f', size=10), #[span_64](end_span)
                   [span_65](start_span)range=[min(data["values"]) - 2, max(data["values"]) + 2]) #[span_65](end_span)
    )
    return fig

def create_sentiment_pie_chart(data):
    """Creates the Plotly figure for the sentiment distribution pie chart."""
    [span_66](start_span)if not data.empty and data['Category'].iloc[0] != 'No Data': #[span_66](end_span)
        [span_67](start_span)fig = px.pie(data, values='Value', names='Category', #[span_67](end_span)
                     color='Category',
                     [span_68](start_span)color_discrete_map={'Positif': '#34c759', 'Netral': '#a2a2a7', 'Negatif': '#ff3b30', 'Unknown': '#cccccc'}, #[span_68](end_span)
                     [span_69](start_span)hole=0.7) #[span_69](end_span)
        fig.update_layout(
            [span_70](start_span)height=230, margin=dict(l=20, r=20, t=20, b=20), #[span_70](end_span)
            [span_71](start_span)paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', #[span_71](end_span)
            [span_72](start_span)legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5, font=dict(size=11)), #[span_72](end_span)
            [span_73](start_span)showlegend=True) #[span_73](end_span)
        fig.update_traces(textinfo='percent', textfont_size=12, insidetextorientation='radial')
    else:
        [span_74](start_span)fig = go.Figure(go.Indicator(mode="number", value=0, title={"text": "No Sentiment Data"})) #[span_74](end_span)
        [span_75](start_span)fig.update_layout(height=230, margin=dict(l=20, r=20, t=40, b=20)) #[span_75](end_span)
    return fig

def create_intent_bar_chart(data):
    """Creates the Plotly figure for the intent distribution bar chart."""
    [span_76](start_span)if not data.empty and data['Intent'].iloc[0] != 'No Data': #[span_76](end_span)
        [span_77](start_span)intent_color_map = {'Informasi': '#007aff', 'Keluhan': '#ff9500', 'Permohonan': '#5856d6', 'Layanan umum': '#ffcc00', 'Penutupan': '#ff3b30'} #[span_77](end_span)
        [span_78](start_span)fig = px.bar(data, y='Intent', x='Value', orientation='h', color='Intent', color_discrete_map=intent_color_map) #[span_78](end_span)
        fig.update_layout(
            [span_79](start_span)height=230, margin=dict(l=0, r=10, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', #[span_79](end_span)
            [span_80](start_span)plot_bgcolor='rgba(0,0,0,0)', showlegend=False, #[span_80](end_span)
            [span_81](start_span)xaxis=dict(title=None, showgrid=True, gridcolor='#e5e5ea'), #[span_81](end_span)
            [span_82](start_span)yaxis=dict(title=None, categoryorder='total ascending')) #[span_82](end_span)
        [span_83](start_span)fig.update_traces(width=0.6) #[span_83](end_span)
    else:
        [span_84](start_span)fig = go.Figure(go.Indicator(mode="number", value=0, title={"text": "No Intent Data"})) #[span_84](end_span)
        [span_85](start_span)fig.update_layout(height=230, margin=dict(l=20, r=20, t=40, b=20)) #[span_85](end_span)
    return fig

def create_volume_line_chart(data, period_label):
    """Creates the Plotly figure for the volume trend line chart."""
    [span_86](start_span)if not data.empty and data['Volume'].sum() > 0: #[span_86](end_span)
        [span_87](start_span)fig = px.line(data, x='Day', y='Volume', line_shape='spline', markers=True) #[span_87](end_span)
        [span_88](start_span)fig.update_traces(line_color='#007aff', fill='tozeroy', fillcolor='rgba(0,122,255,0.18)', mode='lines+markers') #[span_88](end_span)
        y_min, y_max = data['Volume'].min(), data['Volume'].max()
        padding = (y_max - y_min) * 0.1
        [span_89](start_span)y_range = [max(0, y_min - padding), y_max + padding + 1] #[span_89](end_span)
        fig.update_layout(
            [span_90](start_span)height=230, margin=dict(l=0, r=10, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', #[span_90](end_span)
            [span_91](start_span)plot_bgcolor='rgba(0,0,0,0)', #[span_91](end_span)
            [span_92](start_span)xaxis=dict(title=None, showgrid=False), #[span_92](end_span)
            [span_93](start_span)yaxis=dict(title=None, showgrid=True, gridcolor='#e5e5ea', range=y_range) #[span_93](end_span)
        )
    else:
        [span_94](start_span)fig = go.Figure(go.Indicator(mode="number", value=0, title={"text": "No Volume Data"})) #[span_94](end_span)
        [span_95](start_span)fig.update_layout(height=230, margin=dict(l=20, r=20, t=40, b=20)) #[span_95](end_span)
    return fig


# --- UI HELPER FUNCTIONS ---

def render_navbar():
    """Renders the top navigation bar."""
    st.title("VOCAL")
    st.markdown("Customer Experience Health Dashboard")
    st.markdown("---")
    
    nav_cols = st.columns(5)
    with nav_cols[0]:
        with st.container(border=True):
            st.markdown("###### Menu")
            page = st.selectbox("Navigate", ["Dashboard", "Analytics", "Feedback", "Alerts", "Reports"], key="menu_nav", label_visibility="collapsed")
    with nav_cols[1]:
        with st.container(border=True):
            st.markdown("###### Customer Insights")
            st.selectbox("Insights", ["Sentiment Analysis", "Journey Mapping", "Satisfaction Scores", "Theme Analysis"], key="insights_nav", label_visibility="collapsed")
    with nav_cols[2]:
        with st.container(border=True):
            st.markdown("###### Operations")
            [span_96](start_span)st.selectbox("Operations", ["Real-time Monitoring", "Predictive Analytics", "Performance Metrics", "Action Items"], key="ops_nav", label_visibility="collapsed") #[span_96](end_span)
    with nav_cols[3]:
        with st.container(border=True):
            st.markdown("###### Configuration")
            st.selectbox("Config", ["Settings", "User Management", "Security", "Help & Support"], key="config_nav", label_visibility="collapsed")
    with nav_cols[4]:
        with st.container(border=True):
             st.markdown("**Sebastian**")
             st.markdown("CX Manager")
    
    st.markdown("---")
    return page

def render_metric_card_header(title, view_options, view_key):
    """Renders the header for a metric card with a title and radio button view selector."""
    [span_97](start_span)st.markdown(f'<p class="metric-title">{title}</p>', unsafe_allow_html=True) #[span_97](end_span)
    if view_options:
        st.radio("View", view_options, horizontal=True, key=view_key, label_visibility="collapsed")

def render_metric_card_footer():
    """Renders the closing div for a metric card."""
    st.markdown('</div>', unsafe_allow_html=True)


# --- MAIN APPLICATION ---

def main():
    """The main function to run the Streamlit application."""
    master_df = load_data_from_google_sheets()

    # Define main layout: 70% for content, 30% for chat sidebar
    main_content, chat_sidebar_container = st.columns([0.7, 0.3], gap="large")

    with main_content:
        page = render_navbar()

        if page == "Dashboard":
            # --- FILTERS ---
            filter_cols = st.columns(3)
            with filter_cols[0]:
                time_period_option = st.selectbox(
                    "TIME PERIOD",
                    [span_98](start_span)["All Periods", "Today", "This Week", "This Month", "This Quarter", "This Year"], #[span_98](end_span)
                    [span_99](start_span)index=3, #[span_99](end_span)
                    [span_100](start_span)key="time_filter" #[span_100](end_span)
                )
            
            available_products = sorted(list(master_df['Product'].str.replace("_", " ").str.title().unique())) if not master_df.empty and 'Product' in master_df.columns else ["N/A"]
            with filter_cols[1]:
                [span_101](start_span)selected_products = st.multiselect("PRODUCT", ["All Products"] + available_products, default=["All Products"], key="product_filter") #[span_101](end_span)

            available_channels = sorted(list(master_df['Channel'].str.replace("_", " ").str.title().unique())) if not master_df.empty and 'Channel' in master_df.columns else ["N/A"]
            with filter_cols[2]:
                [span_102](start_span)selected_channels = st.multiselect("CHANNEL", ["All Channels"] + available_channels, default=["All Channels"], key="channel_filter") #[span_102](end_span)

            # --- FILTERING LOGIC ---
            [span_103](start_span)filtered_df = master_df.copy() #[span_103](end_span)
            [span_104](start_span)if not filtered_df.empty and 'Date' in filtered_df.columns: #[span_104](end_span)
                [span_105](start_span)today = pd.Timestamp('today').normalize() #[span_105](end_span)
                [span_106](start_span)if time_period_option == "Today": #[span_106](end_span)
                    [span_107](start_span)filtered_df = filtered_df[filtered_df['Date'] == today] #[span_107](end_span)
                [span_108](start_span)elif time_period_option == "This Week": #[span_108](end_span)
                    [span_109](start_span)start_of_week = today - pd.to_timedelta(today.dayofweek, unit='D') #[span_109](end_span)
                    [span_110](start_span)end_of_week = start_of_week + pd.to_timedelta(6, unit='D') #[span_110](end_span)
                    [span_111](start_span)filtered_df = filtered_df[(filtered_df['Date'] >= start_of_week) & (filtered_df['Date'] <= end_of_week)] #[span_111](end_span)
                [span_112](start_span)elif time_period_option == "This Month": #[span_112](end_span)
                    [span_113](start_span)start_of_month = today.replace(day=1) #[span_113](end_span)
                    [span_114](start_span)end_of_month = start_of_month + pd.DateOffset(months=1) - pd.DateOffset(days=1) #[span_114](end_span)
                    [span_115](start_span)filtered_df = filtered_df[(filtered_df['Date'] >= start_of_month) & (filtered_df['Date'] <= end_of_month)] #[span_115](end_span)
                [span_116](start_span)elif time_period_option == "This Quarter": #[span_116](end_span)
                    [span_117](start_span)start_of_quarter = today.to_period('Q').start_time #[span_117](end_span)
                    [span_118](start_span)end_of_quarter = today.to_period('Q').end_time #[span_118](end_span)
                    [span_119](start_span)filtered_df = filtered_df[(filtered_df['Date'] >= start_of_quarter) & (filtered_df['Date'] <= end_of_quarter)] #[span_119](end_span)
                [span_120](start_span)elif time_period_option == "This Year": #[span_120](end_span)
                    [span_121](start_span)start_of_year = today.replace(month=1, day=1) #[span_121](end_span)
                    [span_122](start_span)end_of_year = today.replace(month=12, day=31) #[span_122](end_span)
                    [span_123](start_span)filtered_df = filtered_df[(filtered_df['Date'] >= start_of_year) & (filtered_df['Date'] <= end_of_year)] #[span_123](end_span)
            
            [span_124](start_span)if "All Products" not in selected_products and selected_products: #[span_124](end_span)
                [span_125](start_span)selected_products_internal = [p.lower().replace(" ", "_") for p in selected_products] #[span_125](end_span)
                [span_126](start_span)filtered_df = filtered_df[filtered_df['Product'].isin(selected_products_internal)] #[span_126](end_span)
            
            [span_127](start_span)if "All Channels" not in selected_channels and selected_channels: #[span_127](end_span)
                [span_128](start_span)selected_channels_internal = [c.lower().replace(" ", "_") for c in selected_channels] #[span_128](end_span)
                [span_129](start_span)filtered_df = filtered_df[filtered_df['Channel'].isin(selected_channels_internal)] #[span_129](end_span)

            # --- DATA PREPARATION FOR CHARTS & LLM ---
            [span_130](start_span)health_score_data_source = generate_health_score_data() #[span_130](end_span)
            [span_131](start_span)time_period_map = {"All Periods": "all", "Today": "today", "This Week": "week", "This Month": "month", "This Quarter": "quarter", "This Year": "year"} #[span_131](end_span)
            [span_132](start_span)current_health_data = health_score_data_source.get(time_period_map.get(time_period_option, "month")) #[span_132](end_span)

            sentiment_summary = {}
            [span_133](start_span)if not filtered_df.empty and 'Sentimen' in filtered_df.columns: #[span_133](end_span)
                [span_134](start_span)sentiment_counts = filtered_df['Sentimen'].value_counts() #[span_134](end_span)
                [span_135](start_span)sentiment_data = sentiment_counts.reset_index() #[span_135](end_span)
                [span_136](start_span)sentiment_data.columns = ['Category', 'Value'] #[span_136](end_span)
                [span_137](start_span)total_sentiment = sentiment_counts.sum() #[span_137](end_span)
                [span_138](start_span)if total_sentiment > 0: #[span_138](end_span)
                    [span_139](start_span)sentiment_summary = {k: f"{(v/total_sentiment*100):.1f}% ({v} mentions)" for k, v in sentiment_counts.items()} #[span_139](end_span)
            else:
                [span_140](start_span)sentiment_data = pd.DataFrame({'Category': ['No Data'], 'Value': [1]}) #[span_140](end_span)

            intent_summary = {}
            [span_141](start_span)if not filtered_df.empty and 'Intent' in filtered_df.columns: #[span_141](end_span)
                [span_142](start_span)intent_counts = filtered_df['Intent'].value_counts().nlargest(5) #[span_142](end_span)
                [span_143](start_span)intent_data = intent_counts.reset_index() #[span_143](end_span)
                [span_144](start_span)intent_data.columns = ['Intent', 'Value'] #[span_144](end_span)
                [span_145](start_span)total_intent = intent_counts.sum() #[span_145](end_span)
                [span_146](start_span)if total_intent > 0: #[span_146](end_span)
                    [span_147](start_span)intent_summary = {k: f"{(v/total_intent*100):.1f}% ({v} mentions)" for k, v in intent_counts.items()} #[span_147](end_span)
            else:
                [span_148](start_span)intent_data = pd.DataFrame({'Intent': ['No Data'], 'Value': [1]}) #[span_148](end_span)

            volume_summary = "Date column missing or no data." [span_149](start_span)#
            if not filtered_df.empty and 'Date' in filtered_df.columns: #[span_149](end_span)
                [span_150](start_span)volume_over_time = filtered_df.groupby(filtered_df['Date'].dt.date)['Date'].count() #[span_150](end_span)
                [span_151](start_span)volume_data = volume_over_time.reset_index(name='Volume') #[span_151](end_span)
                [span_152](start_span)volume_data.columns = ['Day', 'Volume'] #[span_152](end_span)
                [span_153](start_span)if not volume_data.empty: #[span_153](end_span)
                    volume_summary = f"Volume trend over period: Min daily {volume_data['Volume'].min()}, Max daily {volume_data['Volume'].max()}, Avg daily {volume_data['Volume'].mean():.1f}. Total {volume_data['Volume'].sum()} interactions." [span_154](start_span)#
            else:
                volume_data = pd.DataFrame({'Day': [pd.Timestamp('today').date()], 'Volume': [0]}) #[span_154](end_span)
            
            # --- TOP ROW WIDGETS ---
            top_row = st.columns(3)
            with top_row[0]:
                [span_155](start_span)st.markdown('<div class="metric-card">', unsafe_allow_html=True) #[span_155](end_span)
                render_metric_card_header("Customer Health Score", ["Real-time", "Trend"], "health_view")
                [span_156](start_span)score_cols = st.columns([1, 2]) #[span_156](end_span)
                with score_cols[0]:
                    [span_157](start_span)st.markdown(f'<div class="metric-value">{current_health_data["score"]}%</div>', unsafe_allow_html=True) #[span_157](end_span)
                with score_cols[1]:
                    [span_158](start_span)trend_icon = "↑" if current_health_data["trend_positive"] else "↓" #[span_158](end_span)
                    [span_159](start_span)trend_class = "metric-trend-positive" if current_health_data["trend_positive"] else "metric-trend-negative" #[span_159](end_span)
                    [span_160](start_span)st.markdown(f'<div class="{trend_class}">{trend_icon} {current_health_data["trend"]} {current_health_data["trend_label"]}</div>', unsafe_allow_html=True) #[span_160](end_span)
                [span_161](start_span)st.plotly_chart(create_health_score_chart(current_health_data), use_container_width=True, config={'displayModeBar': False}) #[span_161](end_span)
                render_metric_card_footer()

            with top_row[1]:
                [span_162](start_span)st.markdown('<div class="metric-card">', unsafe_allow_html=True) #[span_162](end_span)
                render_metric_card_header("Critical Alerts", ["Critical", "High", "All"], "alert_view")
                st.markdown("""
                **Sudden Spike in Negative Sentiment** - *Mobile App Update X.Y: 45% negative* - *Volume: 150 mentions / 3 hrs*
                ---
                **High Churn Risk Pattern Detected** - *Pattern: Repeated Billing Errors - Savings*
                - *12 unique customer patterns*
                [span_163](start_span)""") #[span_163](end_span)
                [span_164](start_span)st.button("View All Alerts", type="primary", key="view_alerts") #[span_164](end_span)
                render_metric_card_footer()

            with top_row[2]:
                [span_165](start_span)st.markdown('<div class="metric-card">', unsafe_allow_html=True) #[span_165](end_span)
                render_metric_card_header("Predictive Hotspots", ["Emerging", "Trending"], "hotspot_view")
                st.markdown("""
                **New Overdraft Policy Confusion** - *'Confused' Language: +30% WoW*
                - *Keywords: "don't understand", "how it works"*
                ---
                **Intl. Transfer UI Issues** - *Task Abandonment: +15% MoM*
                - *Negative sentiment: 'Beneficiary Setup'*
                [span_166](start_span)""") #[span_166](end_span)
                st.button("Investigate Hotspots", key="investigate_hotspots")
                render_metric_card_footer()

            # --- CUSTOMER VOICE SNAPSHOT ---
            [span_167](start_span)st.markdown("## Customer Voice Snapshot") #[span_167](end_span)
            snapshot_cols = st.columns(3)
            with snapshot_cols[0]:
                [span_168](start_span)st.markdown('<div class="metric-card">', unsafe_allow_html=True) #[span_168](end_span)
                render_metric_card_header("Sentiment Distribution", None, None)
                [span_169](start_span)st.plotly_chart(create_sentiment_pie_chart(sentiment_data), use_container_width=True, config={'displayModeBar': False}) #[span_169](end_span)
                render_metric_card_footer()

            with snapshot_cols[1]:
                [span_170](start_span)st.markdown('<div class="metric-card">', unsafe_allow_html=True) #[span_170](end_span)
                render_metric_card_header("Top 5 Intent Distribution", None, None)
                [span_171](start_span)st.plotly_chart(create_intent_bar_chart(intent_data), use_container_width=True, config={'displayModeBar': False}) #[span_171](end_span)
                render_metric_card_footer()

            with snapshot_cols[2]:
                [span_172](start_span)st.markdown('<div class="metric-card">', unsafe_allow_html=True) #[span_172](end_span)
                render_metric_card_header(f"Volume Trend ({time_period_option})", None, None)
                [span_173](start_span)st.plotly_chart(create_volume_line_chart(volume_data, time_period_option), use_container_width=True, config={'displayModeBar': False}) #[span_173](end_span)
                render_metric_card_footer()
        else:
            [span_174](start_span)st.markdown(f"## {page}") #[span_174](end_span)
            [span_175](start_span)st.write("This section is currently under development. Please select 'Dashboard' from the navbar.") #[span_175](end_span)
    
    # --- VIRA CHATBOT IN RIGHT SIDEBAR ---
    with chat_sidebar_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.header("🤖 VIRA - AI Assistant")
        st.markdown("---")
        
        [span_176](start_span)if "messages" not in st.session_state: #[span_176](end_span)
            [span_177](start_span)st.session_state.messages = [{"role": "assistant", "content": "Halo! Saya VIRA, asisten AI Anda. Ada yang bisa saya bantu terkait data di dasbor ini?"}] #[span_177](end_span)

        [span_178](start_span)for message in st.session_state.messages: #[span_178](end_span)
            [span_179](start_span)with st.chat_message(message["role"]): #[span_179](end_span)
                [span_180](start_span)st.markdown(message["content"]) #[span_180](end_span)

        [span_181](start_span)if prompt := st.chat_input("Ask about insights, alerts, or trends..."): #[span_181](end_span)
            [span_182](start_span)st.session_state.messages.append({"role": "user", "content": prompt}) #[span_182](end_span)
            [span_183](start_span)with st.chat_message("user"): #[span_183](end_span)
                [span_184](start_span)st.markdown(prompt) #[span_184](end_span)

            [span_185](start_span)with st.chat_message("assistant"): #[span_185](end_span)
                [span_186](start_span)message_placeholder = st.empty() #[span_186](end_span)
                [span_187](start_span)full_response = "" #[span_187](end_span)
                
                # Re-fetch the latest data for LLM context before generating response
                # This ensures the chatbot uses the currently displayed data
                health_score_data_source_chat = generate_health_score_data()
                time_period_map_chat = {"All Periods": "all", "Today": "today", "This Week": "week", "This Month": "month", "This Quarter": "quarter", "This Year": "year"}
                current_health_data_chat = health_score_data_source_chat.get(time_period_map_chat.get(st.session_state.time_filter, "month"))
                
                dashboard_state_for_llm = {
                    **[span_188](start_span)current_health_data_chat, #[span_188](end_span)
                    [span_189](start_span)"time_period_label_llm": st.session_state.time_filter, #[span_189](end_span)
                    [span_190](start_span)"total_interactions": len(filtered_df), #[span_190](end_span)
                    [span_191](start_span)"sentiment_summary": sentiment_summary, #[span_191](end_span)
                    [span_192](start_span)"intent_summary": intent_summary, #[span_192](end_span)
                    [span_193](start_span)"volume_summary": volume_summary, #[span_193](end_span)
                }
                
                llm_client = initialize_llm_client()
                [span_194](start_span)stream = generate_llm_response(llm_client, prompt, dashboard_state_for_llm) #[span_194](end_span)
                [span_195](start_span)for chunk in stream: #[span_195](end_span)
                    [span_196](start_span)full_response += chunk #[span_196](end_span)
                    [span_197](start_span)message_placeholder.markdown(full_response + "▌") #[span_197](end_span)
                [span_198](start_span)message_placeholder.markdown(full_response) #[span_198](end_span)
            [span_199](start_span)st.session_state.messages.append({"role": "assistant", "content": full_response}) #[span_199](end_span)
        
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
