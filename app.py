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
from auth import initialize_session_state, role_selector, get_user_role, can_view_all_agents, get_selected_agent
from dashboards import (
    agent_dashboard, team_lead_dashboard, manager_dashboard,
    admin_dashboard, lead_import_dashboard, ai_operations_dashboard,
    multichannel_dashboard, realtime_monitoring_dashboard
)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Role selector in sidebar (now with two separate selectors)
    current_role = role_selector()
    
    # Load data based on selections
    user_data = get_user_specific_data(
        st.session_state.get('selected_agent', 'Agent 1'), 
        current_role
    )
    
    # Enhanced main dashboard header
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.title("🤖 NSP-CRM Dashboard")
        st.caption("AI-Powered Customer Relationship Management")
    with col2:
        st.metric("User Level", current_role)
    with col3:
        viewing_agent = get_selected_agent()
        st.metric("Viewing Data", viewing_agent)
    with col4:
        restriction_status = "🔒 Restricted" if is_agent_restricted() else "🔓 Full Access"
        st.metric("Access Level", restriction_status)
    
    # Show data access notification
    if current_role == "Agent":
        st.error(f"🔒 **Data Restriction Active**: You can only view your personal performance data ({get_selected_agent()}). Other agents' data is not accessible.")
    elif get_selected_agent() != 'All Agents':
        st.info(f"👁️ **Specific Agent View**: Currently displaying data for {get_selected_agent()}. Use the sidebar to switch agents or view all agents.")
    else:
        st.success(f"👥 **All Agents View**: Displaying company-wide data across all agents.")
    
    # Rest of your dashboard code...
    # Role-specific dashboard rendering
    if current_role == "Agent":
        agent_dashboard(user_data, current_role)
    elif current_role == "Team Lead":
        team_lead_dashboard(user_data, current_role)
    elif current_role == "Manager":
        manager_dashboard(user_data, current_role)
    else:  # Higher Management
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
        
        # Simple agent performance overview using existing data
        leads_df = user_data['leads']
        calls_df = user_data['calls']
        
        if not leads_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Agent conversion rates
                agent_conversion = leads_df.groupby('AssignedTo').agg({
                    'LeadId': 'count',
                    'LeadStatus': lambda x: (x == 'Won').sum()
                }).reset_index()
                agent_conversion.columns = ['Agent', 'Total_Leads', 'Won_Leads']
                agent_conversion['Conversion_Rate'] = (agent_conversion['Won_Leads'] / agent_conversion['Total_Leads'] * 100).round(1)
                
                fig_conversion = px.bar(agent_conversion, x='Agent', y='Conversion_Rate',
                                      title="Conversion Rate by Agent (%)")
                st.plotly_chart(fig_conversion, use_container_width=True)
            
            with col2:
                # Agent call success rates
                agent_calls = calls_df.groupby('AssignedTo').agg({
                    'LeadCallId': 'count',
                    'CallStatus': lambda x: (x == 'Completed').sum()
                }).reset_index()
                agent_calls.columns = ['Agent', 'Total_Calls', 'Successful_Calls']
                agent_calls['Success_Rate'] = (agent_calls['Successful_Calls'] / agent_calls['Total_Calls'] * 100).round(1)
                
                fig_calls = px.bar(agent_calls, x='Agent', y='Success_Rate',
                                 title="Call Success Rate by Agent (%)")
                st.plotly_chart(fig_calls, use_container_width=True)
            
            # Combine the data for summary table
            summary_table = agent_conversion.merge(agent_calls, on='Agent', how='outer').fillna(0)
            st.dataframe(summary_table)
        
        st.markdown("---")
    
    # Rest of the function remains the same...
    main_tabs = st.tabs([
        "📊 Analytics Hub",
        "🤖 AI Operations", 
        "📥 Lead Import",
        "📱 Multi-Channel",
        "🔧 System Admin",
        "📡 Real-time Monitor"
    ])
    
    with main_tabs[0]:
        manager_dashboard(user_data, user_role)
    
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

