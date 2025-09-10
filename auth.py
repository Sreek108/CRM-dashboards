import streamlit as st

# ──────────────────────────────────────────────────────────────
#  SET-UP
# ──────────────────────────────────────────────────────────────
AGENTS = [f"Agent {i}" for i in range(1, 11)]
LEVELS = ["Agent", "Team Lead", "Manager", "Higher Management"]

DESC = {
    "Agent": "🔴 Personal data only",
    "Team Lead": "🟡 Team-level access",
    "Manager": "🟠 Department access",
    "Higher Management": "🟢 Full system access"
}

def initialize_session_state() -> None:
    """Safe defaults for every new browser session."""
    defaults = {
        "user_level": "Agent",
        "selected_agent": "Agent 1",   # default personal id
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ──────────────────────────────────────────────────────────────
#  SIDEBAR WIDGETS
# ──────────────────────────────────────────────────────────────
def role_selector() -> str:
    st.sidebar.title("🏢 NSP-CRM")
    st.sidebar.caption("AI-Powered CRM System")
    st.sidebar.divider()

    # selector #1 – user level
    level = st.sidebar.selectbox("🎯 Choose your role", LEVELS,
                                 index=LEVELS.index(st.session_state.user_level),
                                 key="sel_level")
    st.session_state.user_level = level
    st.sidebar.info(DESC[level])

    st.sidebar.divider()

    # selector #2 – agent (visible only for TL+)
    if level != "Agent":
        agent_choice = st.sidebar.selectbox(
            "👤 Data for which agent?",
            ["All Agents"] + AGENTS,
            index=0 if st.session_state.selected_agent == "All Agents"
                   else AGENTS.index(st.session_state.selected_agent) + 1,
            key="sel_agent")
        st.session_state.selected_agent = agent_choice
        tag = "All agents" if agent_choice == "All Agents" else agent_choice
        st.sidebar.success(f"Viewing: {tag}")
    else:
        # lock to own identity
        st.session_state.selected_agent = st.sidebar.selectbox(
            "👤 Your agent id", AGENTS,
            index=AGENTS.index(st.session_state.selected_agent),
            disabled=True)
        st.sidebar.error("Restricted to personal data")

    st.sidebar.divider()
    return level

# ──────────────────────────────────────────────────────────────
#  SMALL HELPERS
# ──────────────────────────────────────────────────────────────
def get_user_level() -> str:
    return st.session_state.user_level

def get_selected_agent() -> str:
    return st.session_state.selected_agent

def can_view_all_agents() -> bool:
    return st.session_state.user_level in ["Team Lead", "Manager", "Higher Management"]

def is_agent_restricted() -> bool:
    """True only when the current viewer is an ordinary Agent."""
    return st.session_state.user_level == "Agent"
