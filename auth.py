import streamlit as st

# User roles with descriptions
USER_ROLES = {
    "👤 Agent": {
        "role": "Agent",
        "description": "Individual performance tracking",
        "agent_id": 1
    },
    "👥 Team Lead": {
        "role": "Team Lead", 
        "description": "Team oversight and management",
        "agent_id": None
    },
    "📈 Manager": {
        "role": "Manager",
        "description": "Department-wide analytics", 
        "agent_id": None
    },
    "🏢 Higher Management": {
        "role": "Higher Management",
        "description": "Company-wide insights",
        "agent_id": None
    }
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'user_role' not in st.session_state:
        st.session_state.user_role = "Agent"
    if 'current_user' not in st.session_state:
        st.session_state.current_user = "Agent 1"
    if 'agent_id' not in st.session_state:
        st.session_state.agent_id = 1

def role_selector():
    """Display role selector in sidebar"""
    st.sidebar.title("🏢 Quara Finance")
    st.sidebar.markdown("**CRM Dashboard**")
    st.sidebar.markdown("---")
    
    # Role selection
    selected_role_key = st.sidebar.selectbox(
        "👤 Select User Role",
        list(USER_ROLES.keys()),
        help="Choose your organizational level to view relevant dashboards"
    )
    
    # Update session state based on selection
    role_info = USER_ROLES[selected_role_key]
    st.session_state.user_role = role_info["role"]
    st.session_state.agent_id = role_info["agent_id"]
    
    # Set current user based on role
    if role_info["role"] == "Agent":
        st.session_state.current_user = f"Agent {role_info['agent_id']}"
    else:
        st.session_state.current_user = role_info["role"]
    
    # Display current role info
    st.sidebar.markdown("### 📊 Current View")
    st.sidebar.info(f"**Role:** {role_info['role']}\n\n**Access:** {role_info['description']}")
    
    # Role-specific information
    if role_info["role"] == "Agent":
        st.sidebar.markdown("**👤 Agent Dashboard**")
        st.sidebar.markdown("- Personal performance metrics")
        st.sidebar.markdown("- Individual task management")
        st.sidebar.markdown("- Personal call analytics")
    elif role_info["role"] == "Team Lead":
        st.sidebar.markdown("**👥 Team Lead Dashboard**")
        st.sidebar.markdown("- Team performance overview")
        st.sidebar.markdown("- Agent comparison metrics")
        st.sidebar.markdown("- Team task distribution")
    elif role_info["role"] == "Manager":
        st.sidebar.markdown("**📈 Manager Dashboard**")
        st.sidebar.markdown("- Department-wide analytics")
        st.sidebar.markdown("- Resource allocation insights")
        st.sidebar.markdown("- Performance benchmarking")
    else:  # Higher Management
        st.sidebar.markdown("**🏢 Executive Dashboard**")
        st.sidebar.markdown("- Company-wide insights")
        st.sidebar.markdown("- Strategic forecasting")
        st.sidebar.markdown("- ROI and growth metrics")
    
    st.sidebar.markdown("---")
    return role_info["role"]

def get_user_role():
    """Get current user role"""
    return st.session_state.user_role
