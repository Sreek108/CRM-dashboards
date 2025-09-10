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
from data_loader import load_all_data, get_user_specific_data, get_agent_performance_summary
from auth import initialize_session_state, role_selector, get_user_role, can_view_all_agents
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
    
    # Load data based on user role and selected agent
    user_data = get_user_specific_data(
        st.session_state.current_user, 
        current_role
    )
    
    # Enhanced main dashboard header with agent info
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.title("🤖 NSP-CRM Dashboard")
        st.caption("AI-Powered Customer Relationship Management")
    with col2:
        st.metric("Current Role", current_role)
    with col3:
        viewing_agent = user_data.get('viewing_agent', 'Unknown')
        st.metric("Viewing Data", viewing_agent)
    with col4:
        # System status indicator
        st.metric("AI System", "🟢 Online", delta="Active")
    
    # Show data restriction notice for agents
    if current_role == "Agent":
        st.info(f"🔒 **Data Restriction Active**: You can only view your personal performance data. Other agents' data is not accessible.")
    elif user_data.get('viewing_agent') != 'All Agents':
        st.info(f"👁️ **Viewing Specific Agent**: Currently displaying data for {user_data.get('viewing_agent')}. Use the sidebar to switch agents or view all agents.")
    
    # Role-specific dashboard rendering
    if current_role == "Agent":
        agent_dashboard(user_data, current_role)
    elif current_role == "Team Lead":
        team_lead_dashboard(user_data, current_role)
    elif current_role == "Manager":
        manager_dashboard(user_data, current_role)
    else:  # Higher Management - Full system access
        higher_management_dashboard(user_data, current_role)
    
    # Footer with system and security information
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🔄 Workflow Status:** All systems operational")
    with col2:
        st.markdown("**📊 Data Sync:** Last updated: " + datetime.now().strftime("%H:%M:%S"))
    with col3:
        security_level = "🔴 Restricted" if current_role == "Agent" else "🟢 Full Access"
        st.markdown(f"**🔒 Security Level:** {security_level}")

def higher_management_dashboard(user_data, user_role):
    """Enhanced Higher Management dashboard with agent selection capabilities"""
    
    st.markdown("### 🏢 Executive Dashboard - System Overview")
    st.markdown("---")
    
    # Show agent performance comparison if viewing all agents
    if user_data.get('viewing_agent') == 'All Agents':
        st.subheader("📊 All Agents Performance Overview")
        
        agent_summary = get_agent_performance_summary()
        if agent_summary is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_conversion = px.bar(agent_summary, x='Agent', y='Conversion_Rate',
                                      title="Conversion Rate by Agent (%)")
                st.plotly_chart(fig_conversion, use_container_width=True)
            
            with col2:
                fig_calls = px.bar(agent_summary, x='Agent', y='Call_Success_Rate',
                                 title="Call Success Rate by Agent (%)")
                st.plotly_chart(fig_calls, use_container_width=True)
            
            st.dataframe(agent_summary)
        
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
