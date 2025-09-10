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
    page_title="Quara Finance - CRM Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from data_loader import load_all_data, get_user_specific_data
from auth import initialize_session_state, role_selector, get_user_role
from dashboards import (
    lead_status_dashboard, ai_call_activity_dashboard, 
    followup_task_dashboard, agent_availability_dashboard,
    conversion_dashboard, geographic_dashboard, ml_predictions_dashboard
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
    
    # Main dashboard header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("📊 Quara Finance CRM Dashboard")
    with col2:
        st.metric("Current Role", current_role)
    with col3:
        st.metric("Data Scope", 
                 "Personal" if current_role == "Agent" else "Organization")
    
    # Dashboard navigation tabs
    dashboard_tabs = st.tabs([
        "📋 Lead Status",
        "📞 Call Activity", 
        "📅 Tasks & Follow-up",
        "🕐 Availability",
        "💰 Conversion",
        "🌍 Geographic",
        "🤖 ML Predictions"
    ])
    
    # Render dashboards in tabs
    with dashboard_tabs[0]:
        lead_status_dashboard(user_data, current_role)
    
    with dashboard_tabs[1]:
        ai_call_activity_dashboard(user_data, current_role)
    
    with dashboard_tabs[2]:
        followup_task_dashboard(user_data, current_role)
    
    with dashboard_tabs[3]:
        agent_availability_dashboard(user_data, current_role)
    
    with dashboard_tabs[4]:
        conversion_dashboard(user_data, current_role)
    
    with dashboard_tabs[5]:
        geographic_dashboard(user_data, current_role)
    
    with dashboard_tabs[6]:
        ml_predictions_dashboard(user_data, current_role)
    
    # Footer with role switch help
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666666; font-size: 14px;'>
        💡 <strong>Tip:</strong> Use the role selector in the sidebar to switch between different organizational levels and explore various dashboard views.
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
