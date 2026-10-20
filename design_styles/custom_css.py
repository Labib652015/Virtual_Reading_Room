import streamlit as st

def apply_custom_design():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css?family=Inter:wght@400;500;600;700&display=swap');
    *{ font-family: 'Inter', sans-serif; }
    .stApp {
    background-color: #062c18 !important;
}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A2540 0%, #081B2E 100%);
        color: white;
        padding-top: 1rem;
    }
    section[data-testid="stSidebar"] .stButton button {
        background: rgba(255, 255, 255, 0.07) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        text-align: left !important;
        width: 100% !important;
        padding: 10px 15px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        margin-bottom: 4px;
        transition: all 0.3s ease;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #FFFFFF !important;
        transform: translateX(4px);
    }
    .dashboard-card {
        background: #1e293b;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #334155;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        color: #f8fafc;
    }
    .main-title {
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #38ef7d, #11998e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px !important;
        padding-bottom: 5px;
    }
    .sub-header {
        font-size: 1.1rem !important;
        color: #8b949e !important;
        margin-bottom: 20px !important;
    }
    .book-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .btn-link {
        display: inline-block;
        background: linear-gradient(135deg, #1f6feb 0%, #1158c7 100%);
        color: #ffffff !important;
        padding: 8px 16px;
        border-radius: 8px;
        text-decoration: none !important;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)