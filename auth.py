import streamlit as st

# Define all user roles
USER_ROLES = {
    "Agent 1": {"role": "Agent", "desc": "Individual performance", "agent_name": "Agent 1"},
    "Agent 2": {"role": "Agent", "desc": "Individual performance", "agent_name": "Agent 2"},
    "Agent 3": {"role": "Agent", "desc": "Individual performance", "agent_name": "Agent 3"},
    "Agent 4": {"role": "Agent", "desc": "Individual performance", "agent_name": "Agent 4"},
    "Agent 5": {"role": "Agent", "desc": "Individual performance", "agent_name": "Agent 5"},
    "Agent 6": {"role": "Agent", "desc": "Individual performance", "agent_name": "Agent 6"},
    "Agent 7": {"role": "Agent", "desc": "Individual performance", "agent_name": "Agent 7"},
    "Agent 8": {"role": "Agent", "desc": "Individual performance", "agent_name": "Agent 8"},
    "Agent 9": {"role": "Agent", "desc": "Individual performance", "agent_name": "Agent 9"},
    "Agent 10": {"role": "Agent", "desc": "Individual performance", "agent_name": "Agent 10"},
    "Team Lead": {"role": "Team Lead", "desc": "Team management", "agent_name": None},
    "Manager": {"role": "Manager", "desc": "Department analytics", "agent_name": None},
    "Higher Management": {"role": "Higher Management", "desc": "Full access", "agent_name": None}
}

def initialize_session_state():
    """Initialize session state variables"""
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = "Agent"
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = "Agent 1"
    if "selected_agent" not in st.session_state:
        st.session_state["selected_agent"] = "Agent 1"

def role_selector():
    """Display two separate selectors in sidebar"""
    st.sidebar.title("🏢 NSP-CRM")
    st.sidebar.markdown("**AI-Powered CRM System**")
    st.sidebar.markdown("---")
    
    # SELECTOR 1: User Level
    st.sidebar.markdown("### 🎯 User Level")
    user_levels = ["Agent", "Team Lead", "Manager", "Higher Management"]
    
    selected_level = st.sidebar.selectbox(
        "Select your role:",
        user_levels,
        key="user_level_selector"
    )
    
    st.session_state["user_role"] = selected_level
    
    # Show access description
    level_descriptions = {
        "Agent": "🔴 Personal data access only",
        "Team Lead": "🟡 Team management access",
        "Manager": "🟠 Department-wide access", 
        "Higher Management": "🟢 Full system access"
    }
    
    st.sidebar.info(level_descriptions[selected_level])
    st.sidebar.markdown("---")
    
    # SELECTOR 2: Agent Selection
    st.sidebar.markdown("### 👤 Agent Selection")
    
    agent_options = [f"Agent {i}" for i in range(1, 11)]
    
    if selected_level == "Agent":
        # For Agent - Fixed selection
        agent_choice = st.sidebar.selectbox(
            "Your Agent (Fixed):",
            agent_options,
            index=0,
            disabled=True,
            key="agent_fixed"
        )
        st.session_state["selected_agent"] = agent_choice
        st.sidebar.error("🔒 **Restriction:** Personal data only")
    else:
        # For higher roles - Full selection
        all_options = ["All Agents"] + agent_options
        agent_choice = st.sidebar.selectbox(
            "Choose agent data:",
            all_options,
            key="agent_flexible"
        )
        st.session_state["selected_agent"] = agent_choice
        
        if agent_choice == "All Agents":
            st.sidebar.success("👥 **Viewing:** All agents")
        else:
            st.sidebar.warning(f"👤 **Viewing:** {agent_choice}")
    
    st.sidebar.markdown("---")
    return selected_level

def get_user_role():
    """Get current user role"""
    return st.session_state.get("user_role", "Agent")

def get_selected_agent():
    """Get selected agent"""
    return st.session_state.get("selected_agent", "Agent 1")

def can_view_all_agents():
    """Check if user can view all agents"""
    return st.session_state.get("user_role", "Agent") in ["Team Lead", "Manager", "Higher Management"]

def is_agent_restricted():
    """Check if user is restricted to personal data"""
    return st.session_state.get("user_role", "Agent") == "Agent"
