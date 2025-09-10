import streamlit as st

def initialize_session_state():
    """Initialize session state variables"""
    if 'user_role' not in st.session_state:
        st.session_state.user_role = "Agent"
    if 'selected_agent_id' not in st.session_state:
        st.session_state.selected_agent_id = 1
    if 'viewing_agent' not in st.session_state:
        st.session_state.viewing_agent = "Agent 1"

def role_selector():
    """Display separate role and agent selectors in sidebar"""
    
    st.sidebar.title("🏢 NSP-CRM")
    st.sidebar.markdown("**AI-Powered CRM System**")
    st.sidebar.markdown("---")
    
    # SEPARATE ROLE SELECTOR
    st.sidebar.markdown("### 👤 User Role")
    role_options = ["Agent", "Team Lead", "Manager", "Higher Management"]
    selected_role = st.sidebar.selectbox(
        "Select your role:",
        role_options,
        help="Choose your organizational level"
    )
    
    st.session_state.user_role = selected_role
    
    # Show role description
    role_descriptions = {
        "Agent": "Personal performance tracking only",
        "Team Lead": "Team oversight and management", 
        "Manager": "Department-wide analytics",
        "Higher Management": "Company-wide insights & full system control"
    }
    
    st.sidebar.info(f"**Access Level:** {role_descriptions[selected_role]}")
    
    st.sidebar.markdown("---")
    
    # SEPARATE AGENT SELECTOR (only for Team Lead+)
    if selected_role in ["Team Lead", "Manager", "Higher Management"]:
        st.sidebar.markdown("### 🔍 Agent Selection")
        
        agent_options = ["All Agents"] + [f"Agent {i}" for i in range(1, 11)]
        
        selected_agent = st.sidebar.selectbox(
            "View data for:",
            agent_options,
            help="Select specific agent or view all agents"
        )
        
        st.session_state.viewing_agent = selected_agent
        
        # Visual indicator of current selection
        if selected_agent == "All Agents":
            st.sidebar.success("👥 **Viewing:** Company-wide data")
        else:
            st.sidebar.warning(f"👤 **Viewing:** {selected_agent}'s data only")
    
    else:
        # AGENT ROLE - Restricted to own data
        st.sidebar.markdown("### 🔒 Data Access")
        agent_id = st.session_state.get('selected_agent_id', 1)
        assigned_agent = f"Agent {agent_id}"
        
        st.session_state.viewing_agent = assigned_agent
        
        st.sidebar.error(f"🔒 **Restricted to:** {assigned_agent} (Your data only)")
        st.sidebar.markdown("*Cannot view other agents' data*")
    
    st.sidebar.markdown("---")
    
    # ACCESS LEVEL SUMMARY
    st.sidebar.markdown("### 📊 Current Access Level")
    
    access_info = {
        "Agent": {
            "icon": "🔴",
            "level": "Restricted Access",
            "permissions": ["✅ Personal performance", "✅ Own tasks & calls", "❌ Other agents' data", "❌ System administration"]
        },
        "Team Lead": {
            "icon": "🟡", 
            "level": "Team Access",
            "permissions": ["✅ All team agents", "✅ Performance comparison", "✅ Task management", "❌ System configuration"]
        },
        "Manager": {
            "icon": "🟠",
            "level": "Department Access", 
            "permissions": ["✅ Full analytics suite", "✅ All agent selection", "✅ Advanced reporting", "✅ Limited admin access"]
        },
        "Higher Management": {
            "icon": "🟢",
            "level": "Full System Access",
            "permissions": ["✅ Complete system control", "✅ All dashboards", "✅ System administration", "✅ Advanced AI operations"]
        }
    }
    
    info = access_info[selected_role]
    st.sidebar.markdown(f"{info['icon']} **{info['level']}**")
    
    for permission in info['permissions']:
        st.sidebar.markdown(f"  {permission}")
    
    return selected_role

def get_user_role():
    """Get current user role"""
    return st.session_state.user_role

def get_viewing_agent():
    """Get currently selected agent for viewing"""
    return st.session_state.viewing_agent
