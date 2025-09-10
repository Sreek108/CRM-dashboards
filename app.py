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
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from data_loader import load_all_data, get_user_specific_data
from auth import initialize_session_state, role_selector, get_user_role
from dashboards import (
    agent_dashboard, team_lead_dashboard, manager_dashboard
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
        st.title("📊 NSP-CRM Dashboard")
    with col2:
        st.metric("Current Role", current_role)
    with col3:
        data_scope = "Personal" if current_role == "Agent" else "Company-wide"
        st.metric("Data Scope", data_scope)
    
    # Role-specific dashboard rendering
    if current_role == "Agent":
        agent_dashboard(user_data, current_role)
    elif current_role == "Team Lead":
        team_lead_dashboard(user_data, current_role)
    else:  # Manager and Higher Management
        manager_dashboard(user_data, current_role)
    
    # Footer with role information
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
