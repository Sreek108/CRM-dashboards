import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

@st.cache_data
def load_all_data():
    """Generate sample data"""
    np.random.seed(42)
    agents = [f"Agent {i}" for i in range(1, 11)]
    
    leads_df = pd.DataFrame({
        'LeadId': range(1, 101),
        'AssignedTo': np.random.choice(agents, 100),
        'LeadStatus': np.random.choice(['New', 'In Progress', 'Interested', 'Closed'], 100),
        'Revenue': np.random.uniform(1000, 10000, 100)
    })
    
    return leads_df

def get_user_specific_data(role, selected_agent):
    """Filter data based on role and selection"""
    leads_df = load_all_data()
    
    if role == "Agent":
        # Restrict to personal data only
        return leads_df[leads_df['AssignedTo'] == selected_agent]
    elif selected_agent == "All Agents":
        # Return all data
        return leads_df
    else:
        # Return specific agent data
        return leads_df[leads_df['AssignedTo'] == selected_agent]
