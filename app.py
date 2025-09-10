import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="NSP CRM Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from data_loader import load_all_data, get_user_specific_data
from auth import authenticate_user, get_user_role
from dashboards import (
    lead_status_dashboard, ai_call_activity_dashboard, 
    followup_task_dashboard, agent_availability_dashboard,
    conversion_dashboard, geographic_dashboard, ml_predictions_dashboard
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def main():
    # Authentication
    if not st.session_state.authenticated:
        authenticate_user()
        return
    
    # Load data based on user role
    user_data = get_user_specific_data(
        st.session_state.current_user, 
        st.session_state.user_role
    )
    
    # Sidebar navigation
    st.sidebar.title("🏢 NSP")
    st.sidebar.markdown(f"**User:** {st.session_state.current_user}")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
    st.sidebar.markdown("---")
    
    # Dashboard selection
    dashboard_options = {
        "📊 Lead Status": "lead_status",
        "📞 AI Call Activity": "ai_call_activity", 
        "📅 Follow-up & Tasks": "followup_tasks",
        "🕐 Agent Availability": "agent_availability",
        "💰 Conversion Analysis": "conversion",
        "🌍 Geographic View": "geographic",
        "🤖 ML Predictions": "ml_predictions"
    }
    
    selected_dashboard = st.sidebar.selectbox(
        "Select Dashboard", 
        list(dashboard_options.keys())
    )
    
    # Role-based dashboard rendering
    dashboard_key = dashboard_options[selected_dashboard]
    
    if dashboard_key == "lead_status":
        lead_status_dashboard(user_data, st.session_state.user_role)
    elif dashboard_key == "ai_call_activity":
        ai_call_activity_dashboard(user_data, st.session_state.user_role)
    elif dashboard_key == "followup_tasks":
        followup_task_dashboard(user_data, st.session_state.user_role)
    elif dashboard_key == "agent_availability":
        agent_availability_dashboard(user_data, st.session_state.user_role)
    elif dashboard_key == "conversion":
        conversion_dashboard(user_data, st.session_state.user_role)
    elif dashboard_key == "geographic":
        geographic_dashboard(user_data, st.session_state.user_role)
    elif dashboard_key == "ml_predictions":
        ml_predictions_dashboard(user_data, st.session_state.user_role)
    
    # Logout button
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.current_user = None
        st.rerun()

if __name__ == "__main__":
    main()
