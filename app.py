import streamlit as st
from auth import initialize_session_state, role_selector, get_user_role, get_selected_agent, is_agent_restricted

# Configure page
st.set_page_config(
    page_title="NSP-CRM Dashboard",
    page_icon="🤖",
    layout="wide"
)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Display selectors in sidebar
    current_role = role_selector()
    selected_agent = get_selected_agent()
    
    # Main dashboard header
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.title("🤖 NSP-CRM Dashboard")
        st.caption("AI-Powered Customer Relationship Management")
    
    with col2:
        st.metric("User Level", current_role)
    
    with col3:
        st.metric("Viewing Data", selected_agent)
    
    with col4:
        access_status = "🔒 Restricted" if is_agent_restricted() else "🔓 Full Access"
        st.metric("Access Level", access_status)
    
    # Show access information
    if current_role == "Agent":
        st.error(f"🔒 **Data Restriction**: You can only view your personal data ({selected_agent})")
    elif selected_agent == "All Agents":
        st.success("👥 **All Agents View**: Displaying company-wide data")
    else:
        st.info(f"👤 **Single Agent View**: Displaying data for {selected_agent}")
    
    st.markdown("---")
    
    # Sample dashboard content
    if current_role == "Agent":
        agent_dashboard()
    elif current_role == "Team Lead":
        team_lead_dashboard()
    else:
        manager_dashboard()

def agent_dashboard():
    """Agent-specific dashboard"""
    st.subheader("👤 Agent Dashboard - Personal Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("My Leads", "47")
    with col2:
        st.metric("Leads Won", "5")
    with col3:
        st.metric("Success Rate", "10.6%")
    with col4:
        st.metric("Revenue", "$144,173")
    
    st.info("✅ Personal dashboard loaded successfully!")

def team_lead_dashboard():
    """Team Lead dashboard"""
    st.subheader("👥 Team Lead Dashboard - Team Management")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Team Leads", "127")
    with col2:
        st.metric("Active Agents", "3")
    with col3:
        st.metric("Team Success", "73.4%")
    with col4:
        st.metric("Team Revenue", "$892,456")
    
    st.success("✅ Team Lead dashboard loaded successfully!")

def manager_dashboard():
    """Manager/Higher Management dashboard"""
    st.subheader("🏢 Management Dashboard - Company Analytics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Leads", "1,247")
    with col2:
        st.metric("Won Leads", "234")
    with col3:
        st.metric("Conversion Rate", "18.8%")
    with col4:
        st.metric("Revenue", "$2.4M")
    with col5:
        st.metric("Active Agents", "10")
    
    # Manager-specific dashboard tabs
    tab1, tab2, tab3 = st.tabs(["📊 Lead Status", "📞 Call Activity", "💰 Conversion"])
    
    with tab1:
        st.info("📊 Lead Status Dashboard - Pie chart with New, In Progress, Interested, Closed")
    
    with tab2:
        st.info("📞 AI Call Activity Dashboard - Daily/weekly calls and success rates")
    
    with tab3:
        st.info("💰 Conversion Dashboard - Leads converted vs dropped, revenue potential")
    
    st.success("✅ Management dashboard loaded successfully!")

if __name__ == "__main__":
    main()
