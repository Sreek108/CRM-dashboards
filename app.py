import streamlit as st
from auth import (
    initialize_session_state, role_selector, get_user_level,
    get_selected_agent, can_view_all_agents, is_agent_restricted
)
from data_loader import get_user_specific_data

# -------------------------------------------------------------
# initialise session + sidebar selectors
# -------------------------------------------------------------
initialize_session_state()
current_level = role_selector()            # shows two selectors
viewing_agent = get_selected_agent()

# -------------------------------------------------------------
# fetch data according to the selections
# -------------------------------------------------------------
data = get_user_specific_data(current_level, viewing_agent)

# -------------------------------------------------------------
# HEADER
# -------------------------------------------------------------
st.title("🤖 NSP-CRM Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("User Level", current_level)
col2.metric("Viewing Data", viewing_agent)
status = "🔒 Restricted" if is_agent_restricted() else "🔓 Full Access"
col3.metric("Access", status)

st.divider()

# -------------------------------------------------------------
#  SIMPLE VISUAL (lead status counts)
# -------------------------------------------------------------
st.subheader("Lead Status Breakdown")
counts = data["leads"]["LeadStatus"].value_counts()

if counts.empty:
    st.info("No leads available for this selection.")
else:
    st.bar_chart(counts)

# -------------------------------------------------------------
#  SIMPLE TABLE FOR DEBUG
# -------------------------------------------------------------
st.subheader("Sample Lead Records")
st.dataframe(data["leads"].head())
