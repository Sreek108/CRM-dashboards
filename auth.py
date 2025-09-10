import streamlit as st

def initialize_session_state():
    """Initialize session state variables"""
    if 'user_level' not in st.session_state:
        st.session_state.user_level = "Agent"
    if 'selected_agent' not in st.session_state:
        st.session_state.selected_agent = "Agent 1"
    if 'agent_restriction' not in st.session_state:
        st.session_state.agent_restriction = True

def role_selector():
    """Display two separate selectors in sidebar"""
    
    st.sidebar.title("🏢 NSP-CRM")
    st.sidebar.markdown("**AI-Powered CRM System**")
    st.sidebar.markdown("---")
    
    # SELECTOR 1: USER LEVEL (Always visible)
    st.sidebar.markdown("### 🎯 User Level")
    user_levels = ["Agent", "Team Lead", "Manager", "Higher Management"]
    
    selected_level = st.sidebar.selectbox(
        "Select your access level:",
        user_levels,
        key="user_level_selector",
        help="Choose your organizational role"
    )
    
    st.session_state.user_level = selected_level
    
    # Show access description
    level_descriptions = {
        "Agent": "🔴 Personal data access only",
        "Team Lead": "🟡 Team management access",
        "Manager": "🟠 Department-wide access", 
        "Higher Management": "🟢 Full system access"
    }
    
    st.sidebar.info(level_descriptions[selected_level])
    
    st.sidebar.markdown("---")
    
    # SELECTOR 2: AGENT SELECTION (Conditional visibility)
    st.sidebar.markdown("### 👤 Agent Selection")
    
    # Agent options
    agent_options = [f"Agent {i}" for i in range(1, 11)]
    
    if selected_level == "Agent":
        # For Agent level - Fixed selection, no choice
        st.sidebar.markdown("**Your Agent:**")
        agent_choice = st.sidebar.selectbox(
            "Agent (Fixed):",
            agent_options,
            index=0,  # Default to Agent 1
            key="agent_selector_fixed",
            disabled=True,  # Cannot change
            help="Agents can only view their own data"
        )
        
        st.session_state.selected_agent = agent_choice
        st.session_state.agent_restriction = True
        
        st.sidebar.error("🔒 **Restriction:** You can only view your own data")
    
    else:
        # For Team Lead and above - Full selection
        st.sidebar.markdown("**Select Agent to View:**")
        all_options = ["All Agents"] + agent_options
        
        agent_choice = st.sidebar.selectbox(
            "Choose agent data:",
            all_options,
            key="agent_selector_flexible",
            help="Select specific agent or view all agents"
        )
        
        st.session_state.selected_agent = agent_choice
        st.session_state.agent_restriction = False
        
        if agent_choice == "All Agents":
            st.sidebar.success("👥 **Viewing:** All agents data")
        else:
            st.sidebar.warning(f"👤 **Viewing:** {agent_choice}'s data only")
    
    st.sidebar.markdown("---")
    
    # ACCESS SUMMARY
    st.sidebar.markdown("### 📋 Access Summary")
    
    # Current selections summary
    st.sidebar.markdown(f"**User Level:** {selected_level}")
    st.sidebar.markdown(f"**Viewing Data:** {st.session_state.selected_agent}")
    
    # Permissions matrix
    permissions = {
        "Agent": ["✅ Personal metrics", "✅ Own tasks", "❌ Other agents", "❌ System config"],
        "Team Lead": ["✅ Team data", "✅ Agent comparison", "✅ Task management", "❌ Full system"],
        "Manager": ["✅ All analytics", "✅ Agent selection", "✅ Reporting", "✅ Config access"],
        "Higher Management": ["✅ Full control", "✅ All dashboards", "✅ System admin", "✅ AI operations"]
    }
    
    st.sidebar.markdown("**Current Permissions:**")
    for permission in permissions[selected_level]:
        st.sidebar.markdown(f"  {permission}")
    
    return selected_level

def get_user_role():
    """Get current user level"""
    return st.session_state.get('user_level', 'Agent')

def get_selected_agent():
    """Get currently selected agent for viewing"""
    return st.session_state.get('selected_agent', 'Agent 1')

def can_view_all_agents(user_role=None):
    """Check if user can view all agents"""
    if user_role is None:
        user_role = get_user_role()
    return user_role in ["Team Lead", "Manager", "Higher Management"]

def is_agent_restricted():
    """Check if current user is restricted to personal data only"""
    return st.session_state.get('agent_restriction', True)
