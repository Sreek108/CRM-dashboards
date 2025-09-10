import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

@st.cache_data
def load_all_data():
    """Generate synthetic data based on the provided database schema"""
    np.random.seed(42)
    
    # Lead data
    agents = [f"Agent {i}" for i in range(1, 11)]
    lead_stages = ["New", "Qualified", "Nurtured", "Converted"]
    lead_statuses = ["Uncontacted", "Attempted Contact", "Interested", "Not Interested", 
                    "In Discussion", "Won", "Lost"]
    countries = ["Saudi Arabia", "UAE", "India"]
    
    leads_df = pd.DataFrame({
        'LeadId': range(1, 501),
        'FullName': [f"Lead {i}" for i in range(1, 501)],
        'Email': [f"lead{i}@email.com" for i in range(1, 501)],
        'Phone': [f"+966-{np.random.randint(100000, 999999)}" for _ in range(500)],
        'Company': [f"Company {i%50}" for i in range(500)],
        'LeadStage': np.random.choice(lead_stages, 500, p=[0.4, 0.25, 0.2, 0.15]),
        'LeadStatus': np.random.choice(lead_statuses, 500),
        'AssignedTo': np.random.choice(agents, 500),
        'Country': np.random.choice(countries, 500, p=[0.5, 0.3, 0.2]),
        'CreatedDate': [datetime.now() - timedelta(days=x) for x in np.random.randint(1, 90, 500)],
        'RevenuePotential': np.random.uniform(1000, 50000, 500)
    })
    
    # Call records
    call_statuses = ["Completed", "Missed", "Declined", "Failed"]
    sentiments = ["Positive", "Neutral", "Negative"]
    
    calls_df = pd.DataFrame({
        'LeadCallId': range(1, 1001),
        'LeadId': np.random.choice(leads_df['LeadId'], 1000),
        'AssignedTo': np.random.choice(agents, 1000),
        'CallDateTime': [datetime.now() - timedelta(days=x, hours=y) 
                        for x, y in zip(np.random.randint(1, 30, 1000), 
                                       np.random.randint(0, 24, 1000))],
        'DurationSeconds': np.random.randint(30, 1800, 1000),
        'CallStatus': np.random.choice(call_statuses, 1000, p=[0.6, 0.2, 0.1, 0.1]),
        'Sentiment': np.random.choice(sentiments, 1000, p=[0.4, 0.4, 0.2]),
        'CallSummary': [f"Call summary for call {i}" for i in range(1, 1001)]
    })
    
    # Tasks/Schedule
    task_types = ["Call", "Email", "Meeting", "Demo", "WhatsApp"]
    task_statuses = ["Pending", "In Progress", "Completed", "Cancelled", "Overdue"]
    
    tasks_df = pd.DataFrame({
        'ScheduleId': range(1, 301),
        'LeadId': np.random.choice(leads_df['LeadId'], 300),
        'TaskType': np.random.choice(task_types, 300),
        'ScheduleTitle': [f"Task {i}" for i in range(1, 301)],
        'ScheduledDate': [datetime.now() + timedelta(days=x) 
                         for x in np.random.randint(-5, 15, 300)],
        'TaskStatus': np.random.choice(task_statuses, 300, p=[0.3, 0.2, 0.3, 0.1, 0.1]),
        'AssignedTo': np.random.choice(agents, 300)
    })
    
    # Agent availability (synthetic)
    availability_data = []
    for agent in agents:
        for day in range(7):
            date = datetime.now() - timedelta(days=day)
            for hour in range(9, 18):  # 9 AM to 6 PM
                availability_data.append({
                    'Agent': agent,
                    'Date': date.date(),
                    'Hour': hour,
                    'Status': np.random.choice(['Available', 'Busy', 'Break'], p=[0.6, 0.3, 0.1])
                })
    
    availability_df = pd.DataFrame(availability_data)
    
    return leads_df, calls_df, tasks_df, availability_df

def get_user_specific_data(username, role):
    """Filter data based on user role with enhanced role descriptions"""
    leads_df, calls_df, tasks_df, availability_df = load_all_data()
    
    if role == "Agent":
        # Agent sees only their own data
        agent_name = f"Agent {st.session_state.agent_id}"
        return {
            'leads': leads_df[leads_df['AssignedTo'] == agent_name],
            'calls': calls_df[calls_df['AssignedTo'] == agent_name], 
            'tasks': tasks_df[tasks_df['AssignedTo'] == agent_name],
            'availability': availability_df[availability_df['Agent'] == agent_name],
            'scope': 'personal',
            'description': f'Personal performance data for {agent_name}'
        }
    elif role == "Team Lead":
        # Team Lead sees first 3 agents (their team)
        team_agents = ['Agent 1', 'Agent 2', 'Agent 3']
        return {
            'leads': leads_df[leads_df['AssignedTo'].isin(team_agents)],
            'calls': calls_df[calls_df['AssignedTo'].isin(team_agents)], 
            'tasks': tasks_df[tasks_df['AssignedTo'].isin(team_agents)],
            'availability': availability_df[availability_df['Agent'].isin(team_agents)],
            'scope': 'team',
            'description': 'Team performance data (3 agents)'
        }
    elif role == "Manager":
        # Manager sees larger subset (department level)
        dept_agents = [f'Agent {i}' for i in range(1, 8)]  # First 7 agents
        return {
            'leads': leads_df[leads_df['AssignedTo'].isin(dept_agents)],
            'calls': calls_df[calls_df['AssignedTo'].isin(dept_agents)], 
            'tasks': tasks_df[tasks_df['AssignedTo'].isin(dept_agents)],
            'availability': availability_df[availability_df['Agent'].isin(dept_agents)],
            'scope': 'department',
            'description': 'Department data (7 agents)'
        }
    else:  # Higher Management
        # Higher Management sees all data
        return {
            'leads': leads_df,
            'calls': calls_df,
            'tasks': tasks_df, 
            'availability': availability_df,
            'scope': 'organization',
            'description': 'Complete organizational data (all agents)'
        }
