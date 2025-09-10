import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

@st.cache_data
def load_all_data():
    """Generate synthetic data for 10 agents based on the provided database schema"""
    np.random.seed(42)
    
    # All 10 agents
    agents = [f"Agent {i}" for i in range(1, 11)]
    lead_stages = ["New", "Qualified", "Nurtured", "Converted"]
    lead_statuses = ["Uncontacted", "Attempted Contact", "Interested", "Not Interested", 
                    "In Discussion", "Won", "Lost"]
    countries = ["Saudi Arabia", "UAE", "India"]
    
    # Generate more leads for 10 agents
    random_days = np.random.randint(1, 90, 1000)
    creation_dates = [datetime.now() - timedelta(days=int(x)) for x in random_days]
    
    leads_df = pd.DataFrame({
        'LeadId': range(1, 1001),
        'FullName': [f"Lead {i}" for i in range(1, 1001)],
        'Email': [f"lead{i}@email.com" for i in range(1, 1001)],
        'Phone': [f"+966-{np.random.randint(100000, 999999)}" for _ in range(1000)],
        'Company': [f"Company {i%100}" for i in range(1000)],
        'LeadStage': np.random.choice(lead_stages, 1000, p=[0.4, 0.25, 0.2, 0.15]),
        'LeadStatus': np.random.choice(lead_statuses, 1000),
        'AssignedTo': np.random.choice(agents, 1000),
        'Country': np.random.choice(countries, 1000, p=[0.5, 0.3, 0.2]),
        'CreatedDate': creation_dates,
        'RevenuePotential': np.random.uniform(1000, 50000, 1000)
    })
    
    # Call records for 10 agents
    call_statuses = ["Completed", "Missed", "Declined", "Failed"]
    sentiments = ["Positive", "Neutral", "Negative"]
    
    # Generate call dates
    call_days = np.random.randint(1, 30, 2000)
    call_hours = np.random.randint(0, 24, 2000)
    call_dates = [datetime.now() - timedelta(days=int(x), hours=int(y)) 
                  for x, y in zip(call_days, call_hours)]
    
    calls_df = pd.DataFrame({
        'LeadCallId': range(1, 2001),
        'LeadId': np.random.choice(leads_df['LeadId'], 2000),
        'AssignedTo': np.random.choice(agents, 2000),
        'CallDateTime': call_dates,
        'DurationSeconds': np.random.randint(30, 1800, 2000),
        'CallStatus': np.random.choice(call_statuses, 2000, p=[0.6, 0.2, 0.1, 0.1]),
        'Sentiment': np.random.choice(sentiments, 2000, p=[0.4, 0.4, 0.2]),
        'CallSummary': [f"Call summary for call {i}" for i in range(1, 2001)]
    })
    
    # Tasks/Schedule for 10 agents
    task_types = ["Call", "Email", "Meeting", "Demo", "WhatsApp"]
    task_statuses = ["Pending", "In Progress", "Completed", "Cancelled", "Overdue"]
    
    # Generate scheduled dates
    schedule_days = np.random.randint(-5, 15, 600)
    scheduled_dates = [datetime.now() + timedelta(days=int(x)) for x in schedule_days]
    
    tasks_df = pd.DataFrame({
        'ScheduleId': range(1, 601),
        'LeadId': np.random.choice(leads_df['LeadId'], 600),
        'TaskType': np.random.choice(task_types, 600),
        'ScheduleTitle': [f"Task {i}" for i in range(1, 601)],
        'ScheduledDate': scheduled_dates,
        'TaskStatus': np.random.choice(task_statuses, 600, p=[0.3, 0.2, 0.3, 0.1, 0.1]),
        'AssignedTo': np.random.choice(agents, 600)
    })
    
    # Agent availability for 10 agents
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
    """Filter data based on user role and selected agent with strict access control"""
    leads_df, calls_df, tasks_df, availability_df = load_all_data()
    
    # Get selected agent for viewing
    selected_agent = st.session_state.get('selected_agent', 'Agent 1')
    
    if role == "Agent":
        # STRICT RESTRICTION: Agents can ONLY see their own data
        agent_name = selected_agent  # This will be their fixed agent
        
        filtered_data = {
            'leads': leads_df[leads_df['AssignedTo'] == agent_name],
            'calls': calls_df[calls_df['AssignedTo'] == agent_name], 
            'tasks': tasks_df[tasks_df['AssignedTo'] == agent_name],
            'availability': availability_df[availability_df['Agent'] == agent_name],
            'scope': 'personal',
            'description': f'Personal data for {agent_name} only',
            'viewing_agent': agent_name,
            'can_select_agent': False
        }
        
        return filtered_data
        
    elif role in ["Team Lead", "Manager", "Higher Management"]:
        # Higher roles can select agents
        if selected_agent == "All Agents":
            # Show all agents
            return {
                'leads': leads_df,
                'calls': calls_df,
                'tasks': tasks_df,
                'availability': availability_df,
                'scope': 'all_agents',
                'description': 'All agents performance data',
                'viewing_agent': 'All Agents',
                'can_select_agent': True
            }
        else:
            # Show specific agent data
            return {
                'leads': leads_df[leads_df['AssignedTo'] == selected_agent],
                'calls': calls_df[calls_df['AssignedTo'] == selected_agent],
                'tasks': tasks_df[tasks_df['AssignedTo'] == selected_agent],
                'availability': availability_df[availability_df['Agent'] == selected_agent],
                'scope': 'selected_agent',
                'description': f'Performance data for {selected_agent}',
                'viewing_agent': selected_agent,
                'can_select_agent': True
            }


def get_agent_performance_summary():
    """Get summary of all agents for comparison (only for Team Lead+)"""
    if st.session_state.user_role == "Agent":
        return None  # Agents cannot access this
    
    leads_df, calls_df, tasks_df, availability_df = load_all_data()
    
    # Agent performance summary
    agent_summary = []
    for i in range(1, 11):
        agent_name = f"Agent {i}"
        agent_leads = leads_df[leads_df['AssignedTo'] == agent_name]
        agent_calls = calls_df[calls_df['AssignedTo'] == agent_name]
        
        summary = {
            'Agent': agent_name,
            'Total_Leads': len(agent_leads),
            'Won_Leads': len(agent_leads[agent_leads['LeadStatus'] == 'Won']),
            'Total_Calls': len(agent_calls),
            'Successful_Calls': len(agent_calls[agent_calls['CallStatus'] == 'Completed']),
        }
        
        summary['Conversion_Rate'] = (summary['Won_Leads'] / summary['Total_Leads'] * 100) if summary['Total_Leads'] > 0 else 0
        summary['Call_Success_Rate'] = (summary['Successful_Calls'] / summary['Total_Calls'] * 100) if summary['Total_Calls'] > 0 else 0
        
        agent_summary.append(summary)
    
    return pd.DataFrame(agent_summary)
