import streamlit as st

# 10 Individual Agents + Management Roles
USER_ROLES = {
    "👤 Agent 1": {
        "role": "Agent",
        "description": "Individual performance tracking",
        "agent_id": 1,
        "agent_name": "Agent 1"
    },
    "👤 Agent 2": {
        "role": "Agent",
        "description": "Individual performance tracking", 
        "agent_id": 2,
        "agent_name": "Agent 2"
    },
    "👤 Agent 3": {
        "role": "Agent",
        "description": "Individual performance tracking",
        "agent_id": 3,
        "agent_name": "Agent 3"
    },
    "👤 Agent 4": {
        "role": "Agent",
        "description": "Individual performance tracking",
        "agent_id": 4,
        "agent_name": "Agent 4"
    },
    "👤 Agent 5": {
        "role": "Agent",
        "description": "Individual performance tracking",
        "agent_id": 5,
        "agent_name": "Agent 5"
    },
    "👤 Agent 6": {
        "role": "Agent",
        "description": "Individual performance tracking",
        "agent_id": 6,
        "agent_name": "Agent 6"
    },
    "👤 Agent 7": {
        "role": "Agent",
        "description": "Individual performance tracking",
        "agent_id": 7,
        "agent_name": "Agent 7"
    },
    "👤 Agent 8": {
        "role": "Agent",
        "description": "Individual performance tracking",
        "agent_id": 8,
        "agent_name": "Agent 8"
    },
    "👤 Agent 9": {
        "role": "Agent",
        "description": "Individual performance tracking",
        "agent_id": 9,
        "agent_name": "Agent 9"
    },
    "👤 Agent 10": {
        "role": "Agent",
        "description": "Individual performance tracking",
        "agent_id": 10,
        "agent_name": "Agent 10"
    },
    "👥 Team Lead": {
        "role": "Team Lead", 
        "description": "Team oversight and management",
        "agent_id": None,
        "agent_name": "Team Lead"
    },
    "📈 Manager": {
        "role": "Manager",
        "description": "Department-wide analytics", 
        "agent_id": None,
        "agent_name": "Manager"
    },
    "🏢 Higher Management": {
        "role": "Higher Management",
        "description": "Company-wide insights",
        "agent_id": None,
        "agent_name": "Higher Management"
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
    if 'selected_agent_for_viewing' not in st.session_state:
        st.session_state.selected_agent_for_viewing = "Agent 1"

def role_selector():
    """Display role selector in sidebar with agent selection for higher roles"""
    
    # Sidebar title
    st.sidebar.title("🏢 NSP-CRM")
    st.sidebar.markdown("**AI-Powered CRM System**")
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
    st.session_state.current_user = role_info["agent_name"]
    
    # Agent Selection for Higher Roles (Team Lead and above)
    if role_info["role"] in ["Team Lead", "Manager", "Higher Management"]:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔍 Select Agent to View")
        
        # Get all agent names for selection
        all_agents = [f"Agent {i}" for i in range(1, 11)]
        
        # Agent selector for higher roles
        selected_agent = st.sidebar.selectbox(
            "👤 View Agent Data:",
            ["All Agents"] + all_agents,
            help="Select specific agent to view their performance data"
        )
        
        st.session_state.selected_agent_for_viewing = selected_agent
        
        # Show current selection
        if selected_agent == "All Agents":
            st.sidebar.info("**Viewing:** Company-wide data")
        else:
            st.sidebar.info(f"**Viewing:** {selected_agent}'s performance")
            
    else:
        # Agents can only see their own data
        st.session_state.selected_agent_for_viewing = role_info["agent_name"]
        st.sidebar.markdown("---")
        st.sidebar.info(f"**Viewing:** Your personal data only")
    
    # Display current role info
    st.sidebar.markdown("### 📊 Current Access Level")
    
    if role_info["role"] == "Agent":
        st.sidebar.warning(f"**Role:** {role_info['role']}\n\n**Restriction:** Personal data only\n\n**Agent:** {role_info['agent_name']}")
        
        # Agent-specific information
        st.sidebar.markdown("**👤 Agent Dashboard**")
        st.sidebar.markdown("- ✅ Personal performance metrics")
        st.sidebar.markdown("- ✅ Individual task management") 
        st.sidebar.markdown("- ✅ Personal call analytics")
        st.sidebar.markdown("- ❌ Other agents' data")
        
    elif role_info["role"] == "Team Lead":
        st.sidebar.success(f"**Role:** {role_info['role']}\n\n**Access:** All agents' performance")
        
        st.sidebar.markdown("**👥 Team Lead Dashboard**")
        st.sidebar.markdown("- ✅ All agents performance")
        st.sidebar.markdown("- ✅ Agent comparison metrics")
        st.sidebar.markdown("- ✅ Team task distribution")
        st.sidebar.markdown("- ✅ Agent selection capability")
        
    elif role_info["role"] == "Manager":
        st.sidebar.success(f"**Role:** {role_info['role']}\n\n**Access:** Complete department analytics")
        
        st.sidebar.markdown("**📈 Manager Dashboard**")
        st.sidebar.markdown("- ✅ Department-wide analytics")
        st.sidebar.markdown("- ✅ Resource allocation insights")
        st.sidebar.markdown("- ✅ Performance benchmarking")
        st.sidebar.markdown("- ✅ Agent selection capability")
        
    else:  # Higher Management
        st.sidebar.success(f"**Role:** {role_info['role']}\n\n**Access:** Full system control")
        
        st.sidebar.markdown("**🏢 Executive Dashboard**")
        st.sidebar.markdown("- ✅ Company-wide insights")
        st.sidebar.markdown("- ✅ Strategic forecasting")
        st.sidebar.markdown("- ✅ ROI and growth metrics")
        st.sidebar.markdown("- ✅ Complete system access")
    
    st.sidebar.markdown("---")
    return role_info["role"]

def get_user_role():
    """Get current user role"""
    return st.session_state.user_role

def get_selected_agent():
    """Get currently selected agent for viewing"""
    return st.session_state.selected_agent_for_viewing

def can_view_all_agents(user_role):
    """Check if user role can view all agents"""
    return user_role in ["Team Lead", "Manager", "Higher Management"]
