import streamlit as st

# User database with roles
USER_DATABASE = {
    "agent1": {"password": "pass123", "role": "Agent", "agent_id": 1},
    "agent2": {"password": "pass123", "role": "Agent", "agent_id": 2}, 
    "agent3": {"password": "pass123", "role": "Agent", "agent_id": 3},
    "teamlead1": {"password": "lead123", "role": "Team Lead", "agent_id": None},
    "manager1": {"password": "mgr123", "role": "Manager", "agent_id": None},
    "admin": {"password": "admin123", "role": "Higher Management", "agent_id": None}
}

def authenticate_user():
    st.title("🔐 NSP - Login")
    st.markdown("### Welcome to CRM Dashboard")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("#### Please enter your credentials")
        username = st.text_input("NSP")
        password = st.text_input("1234", type="password")
        
        if st.button("Login", use_container_width=True):
            if username in USER_DATABASE and USER_DATABASE[username]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.current_user = username
                st.session_state.user_role = USER_DATABASE[username]["role"]
                st.session_state.agent_id = USER_DATABASE[username]["agent_id"]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials!")
        
        # Demo credentials
        st.markdown("---")
        st.markdown("**Demo Credentials:**")
        st.markdown("- Agent: `agent1` / `pass123`")
        st.markdown("- Team Lead: `teamlead1` / `lead123`")
        st.markdown("- Manager: `manager1` / `mgr123`")
        st.markdown("- Admin: `admin` / `admin123`")

def get_user_role():
    return st.session_state.user_role
