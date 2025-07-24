import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="ERP IPGFLEXO",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    # Inyección de CSS para branding corporativo IPGFLEXO
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');
        html, body, [class*='css'] { font-family: 'Open Sans', sans-serif; }
        .main-header { background: transparent; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; }
        .main-header h1 { color: black; text-align: center; margin: 0; font-weight: 600; }
        .css-1d391kg { background: linear-gradient(180deg, #00356B 0%, #00356B88 100%); }
        .sidebar-logo { text-align: center; padding: 1rem 0; border-bottom: 2px solid #E7343F; margin-bottom: 1rem; }
        .stButton > button { background: #E7343F; color: white; border: none; border-radius: 6px; font-weight: 600; transition: all 0.3s ease; }
        .stButton > button:hover { background: #C12128; transform: translateY(-2px); box-shadow: 0 4px 8px rgba(231, 52, 63, 0.3); }
        .stButton > button[kind="secondary"] { background: #00356B; color: white; }
        .stButton > button[kind="secondary"]:hover { background: #002244; }
        .stDataFrame { border: 1px solid #E7343F22; border-radius: 8px; }
        .stDataFrame ::-webkit-scrollbar { width: 30px !important; height: 30px !important; }
        .stDataFrame ::-webkit-scrollbar-track { background: #f1f1f1 !important; border-radius: 8px !important; }
        .stDataFrame ::-webkit-scrollbar-thumb { background: #888 !important; border-radius: 8px !important; border: 2px solid #f1f1f1 !important; }
        .stDataFrame ::-webkit-scrollbar-thumb:hover { background: #555 !important; }
        .stDataFrame { scrollbar-width: thick !important; scrollbar-color: #888 #f1f1f1 !important; }
        .stSelectbox > div > div { border-color: #00356B44; }
        .stTextInput > div > div > input { border-color: #00356B44; }
        .section-header { background: linear-gradient(90deg, #00356B11 0%, transparent 100%); padding: 0.5rem 1rem; border-left: 4px solid #E7343F; margin: 1rem 0; }
        .stTextInput label:has-text("*"), .stSelectbox label:has-text("*"), .stTextArea label:has-text("*"), .stNumberInput label:has-text("*"), .stDateInput label:has-text("*") { color: #E7343F !important; font-weight: 600 !important; }
        div[data-testid="stTextInput"]:has(label:contains("*")) input, div[data-testid="stSelectbox"]:has(label:contains("*")) > div, div[data-testid="stTextArea"]:has(label:contains("*")) textarea, div[data-testid="stNumberInput"]:has(label:contains("*")) input, div[data-testid="stDateInput"]:has(label:contains("*")) input { border-color: #E7343F44 !important; box-shadow: 0 0 0 1px rgba(231, 52, 63, 0.1) !important; }
        </style>
    """, unsafe_allow_html=True)

def main_header():
    st.markdown("""
        <div class='main-header'>
            <h1>🏭 IPGFLEXO ERP</h1>
        </div>
    """, unsafe_allow_html=True)

def sidebar_logo():
    st.markdown('<div class="sidebar-logo"><h2>🏭 IPGFLEXO</h2></div>', unsafe_allow_html=True) 