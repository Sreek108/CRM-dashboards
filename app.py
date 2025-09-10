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
    page_title="NSP-CRM Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from data_loader import load_all_data, get_user_specific_data
from auth import initialize_session_state, role_selector, get_user_role
from dashboards import (
    agent_dashboard, team_lead_dashboard, manager_dashboard,
    admin_dashboard, lead_import_dashboard, ai_operations_dashboard,
    multichannel_dashboard, realtime_monitoring_dashboard
)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Role selector in sidebar
    current_role = role_selector()
    
    # Load data based on user role
    user_data = get_user_specific_data(
        st.session_state.current_user, 
        current_role
    )
    
    # Main dashboard header with workflow indicator
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.title("🤖 NSP-CRM Dashboard")
        st.caption("AI-Powered Customer Relationship Management")
    with col2:
        st.metric("Current Role", current_role)
    with col3:
        data_scope = "Personal" if current_role == "Agent" else "Company-wide"
        st.metric("Data Scope", data_scope)
    with col4:
        # System status indicator
        st.metric("AI System", "🟢 Online", delta="Active")
    
    # Enhanced role-specific dashboard rendering
    if current_role == "Agent":
        agent_dashboard(user_data, current_role)
    elif current_role == "Team Lead":
        team_lead_dashboard(user_data, current_role)
    elif current_role == "Manager":
        manager_dashboard(user_data, current_role)
    else:  # Higher Management - Full system access
        higher_management_dashboard(user_data, current_role)
    
    # Footer with system information
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🔄 Workflow Status:** All systems operational")
    with col2:
        st.markdown("**📊 Data Sync:** Last updated: " + datetime.now().strftime("%H:%M:%S"))
    with col3:
        st.markdown("**🤖 AI Engine:** GPT-4 Powered calling system")

def higher_management_dashboard(user_data, user_role):
    """Enhanced Higher Management dashboard with full workflow control"""
    
    st.markdown("### 🏢 Executive Dashboard - Complete System Overview")
    st.markdown("---")
    
    # Enhanced navigation for full system access
    main_tabs = st.tabs([
        "📊 Analytics Hub",
        "🤖 AI Operations", 
        "📥 Lead Import",
        "📱 Multi-Channel",
        "🔧 System Admin",
        "📡 Real-time Monitor"
    ])
    
    with main_tabs[0]:
        manager_dashboard(user_data, user_role)  # Existing analytics
    
    with main_tabs[1]:
        ai_operations_dashboard(user_data, user_role)
    
    with main_tabs[2]:
        lead_import_dashboard(user_data, user_role)
    
    with main_tabs[3]:
        multichannel_dashboard(user_data, user_role)
    
    with main_tabs[4]:
        admin_dashboard(user_data, user_role)
    
    with main_tabs[5]:
        realtime_monitoring_dashboard(user_data, user_role)

if __name__ == "__main__":
    main()
