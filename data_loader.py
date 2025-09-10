import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# -------------------------------------------------------------
# quick synthetic dataset (replace with real DB calls)
# -------------------------------------------------------------
@st.cache_data
def load_all_data():
    np.random.seed(0)
    agents = [f"Agent {i}" for i in range(1, 11)]

    leads = pd.DataFrame({
        "LeadId": range(1, 501),
        "AssignedTo": np.random.choice(agents, 500),
        "LeadStatus": np.random.choice(
            ["Uncontacted", "Interested", "Won", "Lost", "In Discussion"], 500),
        "CreatedDate": [datetime.now() - timedelta(days=int(x))
                        for x in np.random.randint(1, 90, 500)],
        "RevenuePotential": np.random.uniform(1_000, 10_000, 500)
    })

    calls = pd.DataFrame({
        "CallId": range(1, 1001),
        "AssignedTo": np.random.choice(agents, 1_000),
        "CallStatus": np.random.choice(
            ["Completed", "Missed", "Failed"], 1_000, p=[0.6, 0.3, 0.1]),
        "CallDateTime": [datetime.now() - timedelta(hours=int(x))
                         for x in np.random.randint(1, 720, 1_000)],
        "DurationSec": np.random.randint(30, 600, 1_000)
    })

    return leads, calls

# -------------------------------------------------------------
# role-aware filter
# -------------------------------------------------------------
def get_user_specific_data(user_level: str, selected_agent: str):
    leads, calls = load_all_data()

    if user_level == "Agent":
        # STRICT personal filter
        leads = leads[leads.AssignedTo == selected_agent]
        calls = calls[calls.AssignedTo == selected_agent]
    elif selected_agent != "All Agents":
        leads = leads[leads.AssignedTo == selected_agent]
        calls = calls[calls.AssignedTo == selected_agent]

    return {"leads": leads, "calls": calls}
