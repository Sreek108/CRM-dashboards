import streamlit as st

# Define all user roles and agents
USER_ROLES = {
    "Agent 1": {"role": "Agent", "desc": "Individual performance tracking", "agent_name": "Agent 1"},
    "Agent 2": {"role": "Agent", "desc": "Individual performance tracking", "agent_name": "Agent 2"},
    "Agent 3": {"role": "Agent", "desc": "Individual performance tracking", "agent_name": "Agent 3"},
    "Agent 4": {"role": "Agent", "desc": "Individual performance tracking", "agent_name": "Agent 4"},
    "Agent 5": {"role": "Agent", "desc": "Individual performance tracking", "agent_name": "Agent 5"},
    "Agent 6": {"role": "Agent", "desc": "Individual performance tracking", "agent_name": "Agent 6"},
    "Agent 7": {"role": "Agent", "desc": "Individual performance tracking", "agent_name": "Agent 7"},
    "Agent 8": {"role": "Agent", "desc": "Individual performance tracking", "agent_name": "Agent 8"},
    "Agent 9": {"role": "Agent", "desc": "Individual performance tracking", "agent_name": "Agent 9"},
    "Agent 10": {"role": "Agent", "desc": "Individual performance tracking", "agent_name": "Agent 10"},
    "Team Lead": {"role": "Team Lead", "desc": "Team oversight and management", "agent_name": None},
    "Manager": {"role": "Manager", "desc": "Department-wide analytics", "agent_name": None},
    "Higher Management": {"role": "Higher Management", "desc": "Company-wide insights", "agent_name": None}
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'user_role' not in st.session_state:
        st.session_state.user_role = "Agent 1"
    if 'current_user' not in st.session_state:
        st.session_state.current_user = "Agent 1"
    if 'selected_agent_for_viewing' not in st.session_state:
        st.session_state.selected_agent_for_viewing = "Agent 1"

def role_selector():
    """Display separate role and agent selectors in sidebar"""
    
    st.sidebar.title("🏢 NSP-CRM")
    st.sidebar.markdown("**AI-Powered CRM System**")
    st.sidebar.markdown("---")
    
    # ROLE SELECTOR
    st.sidebar.markdown("### 👤 Select User Role")
    role_options = list(USER_ROLES.keys())
    selected_role_key = st.sidebar.selectbox(
        "Choose your role:",
        role_options,
        help="Select your organizational level"
    )
    
    # Update session state
    role_info = USER_ROLES[selected_role_key]
    st.session_state.user_role = role_info["role"]
    st.session_state.current_user = selected_role_key
    
    # Show role description
    st.sidebar.info(f"**Access:** {role_info['desc']}")
    st.sidebar.markdown("---")
    
    # AGENT SELECTOR (only for Team Lead and above)
    if role_info["role"] in ["Team Lead", "Manager", "Higher Management"]:
        st.sidebar.markdown("### 🔍 Select Agent to View")
        
        # Get all agent options
        agent_options = ["All Agents"] + [key for key in USER_ROLES.keys() if USER_ROLES[key]["role"] == "Agent"]
        
        selected_agent = st.sidebar.selectbox(
            "View data for:",
            agent_options,
            help="Select specific agent or view all agents"
        )
        
        st.session_state.selected_agent_for_viewing = selected_agent
        
        # Visual indicator
        if selected_agent == "All Agents":
            st.sidebar.success("👥 **Viewing:** All agents data")
        else:
            st.sidebar.warning(f"👤 **Viewing:** {selected_agent}'s data")
    
    else:
        # AGENT ROLE - Restricted to own data
        st.session_state.selected_agent_for_viewing = selected_role_key
        st.sidebar.error(f"🔒 **Restricted:** {selected_role_key} data only")
    
    st.sidebar.markdown("---")
    
    # ACCESS LEVEL DISPLAY
    st.sidebar.markdown("### 📊 Access Level")
    
    if role_info["role"] == "Agent":
        st.sidebar.markdown("🔴 **Restricted Access**")
        st.sidebar.markdown("- ✅ Personal performance")
        st.sidebar.markdown("- ❌ Other agents' data")
    elif role_info["role"] == "Team Lead":
        st.sidebar.markdown("🟡 **Team Access**")
        st.sidebar.markdown("- ✅ All team agents")
        st.sidebar.markdown("- ✅ Performance comparison")
    elif role_info["role"] == "Manager":
        st.sidebar.markdown("🟠 **Department Access**")
        st.sidebar.markdown("- ✅ Full analytics suite")
        st.sidebar.markdown("- ✅ All agent selection")
    else:  # Higher Management
        st.sidebar.markdown("🟢 **Full System Access**")
        st.sidebar.markdown("- ✅ Complete system control")
        st.sidebar.markdown("- ✅ All dashboards")
    
    return role_info["role"]

def get_user_role():
    """Get current user role"""
    return st.session_state.get('user_role', 'Agent 1')

def can_view_all_agents(user_role=None):
    """Check if user role can view all agents"""
    if user_role is None:
        user_role = st.session_state.get('user_role', 'Agent 1')
    return user_role in ["Team Lead", "Manager", "Higher Management"]

def get_selected_agent():
    """Get currently selected agent for viewing"""
    return st.session_state.get('selected_agent_for_viewing', 'Agent 1')
