import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def manager_dashboard(user_data, user_role):
    """Enhanced Manager Dashboard with specific requested components"""
    
    st.markdown("### 🏢 Manager Dashboard - Complete Analytics Suite")
    st.markdown("---")
    
    leads_df = user_data['leads']
    tasks_df = user_data['tasks']
    calls_df = user_data['calls']
    availability_df = user_data['availability']
    
    # Top-level KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_leads = len(leads_df)
        st.metric("Total Leads", f"{total_leads:,}")
    with col2:
        won_leads = len(leads_df[leads_df['LeadStatus'] == 'Won'])
        st.metric("Won Leads", f"{won_leads:,}")
    with col3:
        conversion_rate = (won_leads / total_leads * 100) if total_leads > 0 else 0
        st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    with col4:
        revenue = leads_df[leads_df['LeadStatus'] == 'Won']['RevenuePotential'].sum()
        st.metric("Revenue Potential", f"${revenue:,.0f}")
    with col5:
        active_agents = leads_df['AssignedTo'].nunique()
        st.metric("Active Agents", active_agents)
    
    st.markdown("---")
    
    # MANAGER-SPECIFIC DASHBOARD TABS
    manager_tabs = st.tabs([
        "📊 Lead Status",
        "📞 AI Call Activity", 
        "📅 Follow-up & Tasks",
        "🕐 Agent Availability",
        "💰 Conversion Analysis",
        "🌍 Geographic View"
    ])
    
    with manager_tabs[0]:
        lead_status_manager_dashboard(leads_df)
    
    with manager_tabs[1]:
        ai_call_activity_manager_dashboard(calls_df)
    
    with manager_tabs[2]:
        followup_task_manager_dashboard(tasks_df)
    
    with manager_tabs[3]:
        agent_availability_manager_dashboard(availability_df)
    
    with manager_tabs[4]:
        conversion_manager_dashboard(leads_df)
    
    with manager_tabs[5]:
        geographic_manager_dashboard(leads_df)

def lead_status_manager_dashboard(leads_df):
    """Lead Status Dashboard - Manager Level"""
    st.header("📊 Lead Status Dashboard")
    
    # Map lead statuses to requested categories
    status_mapping = {
        'Uncontacted': 'New',
        'Attempted Contact': 'New',
        'Interested': 'Interested', 
        'In Discussion': 'In Progress',
        'Won': 'Closed',
        'Lost': 'Closed',
        'Not Interested': 'Closed'
    }
    
    leads_df = leads_df.copy()
    leads_df['MappedStatus'] = leads_df['LeadStatus'].map(status_mapping)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lead Status Distribution (New, In Progress, Interested, Closed)")
        
        # Pie chart with requested categories
        mapped_counts = leads_df['MappedStatus'].value_counts()
        
        fig_pie = px.pie(
            values=mapped_counts.values,
            names=mapped_counts.index,
            title="Lead Status Distribution",
            color_discrete_map={
                'New': '#87CEEB',
                'In Progress': '#FFB347', 
                'Interested': '#98FB98',
                'Closed': '#DDA0DD'
            }
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Lead Status by Agent")
        
        # Agent performance breakdown
        agent_status = leads_df.groupby(['AssignedTo', 'MappedStatus']).size().unstack(fill_value=0)
        
        fig_agent_status = px.bar(
            agent_status,
            title="Lead Status Distribution by Agent",
            color_discrete_map={
                'New': '#87CEEB',
                'In Progress': '#FFB347',
                'Interested': '#98FB98', 
                'Closed': '#DDA0DD'
            }
        )
        st.plotly_chart(fig_agent_status, use_container_width=True)
    
    # Detailed status table
    st.subheader("Detailed Lead Status Breakdown")
    detailed_status = leads_df.groupby(['MappedStatus', 'LeadStatus']).size().reset_index()
    detailed_status.columns = ['Category', 'Specific_Status', 'Count']
    st.dataframe(detailed_status, use_container_width=True)

def ai_call_activity_manager_dashboard(calls_df):
    """AI Call Activity Dashboard - Manager Level"""
    st.header("📞 AI Call Activity Dashboard")
    
    # Daily/Weekly call metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_calls = len(calls_df)
        st.metric("Total Calls", f"{total_calls:,}")
    with col2:
        successful_calls = len(calls_df[calls_df['CallStatus'] == 'Completed'])
        st.metric("Successful Calls", f"{successful_calls:,}")
    with col3:
        success_rate = (successful_calls / total_calls * 100) if total_calls > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
    with col4:
        avg_duration = calls_df['DurationSeconds'].mean() / 60
        st.metric("Avg Duration", f"{avg_duration:.1f} min")
    
    # Daily/Weekly analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Calls Made")
        
        # Daily call volume
        calls_df['Date'] = calls_df['CallDateTime'].dt.date
        daily_calls = calls_df.groupby('Date').size().reset_index()
        daily_calls.columns = ['Date', 'Calls_Made']
        
        fig_daily = px.line(
            daily_calls, 
            x='Date', 
            y='Calls_Made',
            title="Daily Call Volume Trend",
            markers=True
        )
        fig_daily.update_layout(yaxis_title="Calls Made")
        st.plotly_chart(fig_daily, use_container_width=True)
    
    with col2:
        st.subheader("Weekly Success Rate")
        
        # Weekly success rate
        calls_df['Week'] = calls_df['CallDateTime'].dt.to_period('W').astype(str)
        weekly_success = calls_df.groupby('Week').agg({
            'LeadCallId': 'count',
            'CallStatus': lambda x: (x == 'Completed').sum()
        }).reset_index()
        weekly_success.columns = ['Week', 'Total_Calls', 'Successful_Calls']
        weekly_success['Success_Rate'] = (weekly_success['Successful_Calls'] / weekly_success['Total_Calls'] * 100).round(1)
        
        fig_weekly = px.bar(
            weekly_success,
            x='Week',
            y='Success_Rate', 
            title="Weekly Call Success Rate",
            color='Success_Rate',
            color_continuous_scale='Viridis'
        )
        fig_weekly.update_layout(yaxis_title="Success Rate (%)")
        st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Agent performance comparison
    st.subheader("Agent Call Performance Comparison")
    agent_calls = calls_df.groupby('AssignedTo').agg({
        'LeadCallId': 'count',
        'CallStatus': lambda x: (x == 'Completed').sum(),
        'DurationSeconds': 'mean'
    }).reset_index()
    agent_calls.columns = ['Agent', 'Total_Calls', 'Successful_Calls', 'Avg_Duration']
    agent_calls['Success_Rate'] = (agent_calls['Successful_Calls'] / agent_calls['Total_Calls'] * 100).round(1)
    agent_calls['Avg_Duration'] = (agent_calls['Avg_Duration'] / 60).round(1)
    
    st.dataframe(agent_calls, use_container_width=True)

def followup_task_manager_dashboard(tasks_df):
    """Follow-up & Task Dashboard - Manager Level"""
    st.header("📅 Follow-up & Task Dashboard")
    
    today = datetime.now().date()
    
    # Task metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        upcoming_calls = len(tasks_df[
            (tasks_df['TaskType'] == 'Call') &
            (tasks_df['ScheduledDate'].dt.date >= today) &
            (tasks_df['TaskStatus'] == 'Pending')
        ])
        st.metric("Upcoming Calls", upcoming_calls)
    
    with col2:
        overdue_tasks = len(tasks_df[
            (tasks_df['ScheduledDate'].dt.date < today) &
            (tasks_df['TaskStatus'].isin(['Pending', 'In Progress']))
        ])
        st.metric("Overdue Tasks", overdue_tasks, delta=f"-{overdue_tasks}" if overdue_tasks > 0 else "0")
    
    with col3:
        completed_today = len(tasks_df[
            (tasks_df['ScheduledDate'].dt.date == today) &
            (tasks_df['TaskStatus'] == 'Completed')
        ])
        st.metric("Completed Today", completed_today)
    
    with col4:
        total_tasks = len(tasks_df)
        completed_tasks = len(tasks_df[tasks_df['TaskStatus'] == 'Completed'])
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Overall Completion Rate", f"{completion_rate:.1f}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upcoming Calls (Next 7 Days)")
        
        upcoming_calls_detail = tasks_df[
            (tasks_df['TaskType'] == 'Call') &
            (tasks_df['ScheduledDate'].dt.date >= today) &
            (tasks_df['ScheduledDate'].dt.date <= today + timedelta(days=7)) &
            (tasks_df['TaskStatus'] == 'Pending')
        ].sort_values('ScheduledDate')
        
        if not upcoming_calls_detail.empty:
            st.dataframe(upcoming_calls_detail[['ScheduleTitle', 'AssignedTo', 'ScheduledDate', 'TaskType']])
        else:
            st.info("No upcoming calls scheduled for the next 7 days.")
    
    with col2:
        st.subheader("Overdue Tasks by Agent")
        
        overdue_by_agent = tasks_df[
            (tasks_df['ScheduledDate'].dt.date < today) &
            (tasks_df['TaskStatus'].isin(['Pending', 'In Progress']))
        ].groupby('AssignedTo').size().reset_index()
        overdue_by_agent.columns = ['Agent', 'Overdue_Count']
        
        if not overdue_by_agent.empty:
            fig_overdue = px.bar(
                overdue_by_agent,
                x='Agent',
                y='Overdue_Count',
                title="Overdue Tasks by Agent",
                color='Overdue_Count',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig_overdue, use_container_width=True)
        else:
            st.success("🎉 No overdue tasks!")

def agent_availability_manager_dashboard(availability_df):
    """Agent Availability Dashboard - Manager Level"""
    st.header("🕐 Agent Availability Dashboard")
    
    if availability_df.empty:
        st.warning("No availability data available.")
        return
    
    # Availability metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_slots = len(availability_df)
        st.metric("Total Time Slots", f"{total_slots:,}")
    
    with col2:
        busy_slots = len(availability_df[availability_df['Status'] == 'Busy'])
        utilization = (busy_slots / total_slots * 100) if total_slots > 0 else 0
        st.metric("Overall Utilization", f"{utilization:.1f}%")
    
    with col3:
        available_slots = len(availability_df[availability_df['Status'] == 'Available'])
        st.metric("Available Slots", f"{available_slots:,}")
    
    st.subheader("Agent Availability Heatmap (Free/Busy Slots)")
    
    # Create availability heatmap
    availability_pivot = availability_df.pivot_table(
        index='Agent',
        columns=['Date', 'Hour'],
        values='Status',
        aggfunc='first'
    )
    
    # Convert status to numeric for heatmap
    status_mapping = {'Available': 0, 'Busy': 1, 'Break': 0.5}
    availability_numeric = availability_pivot.replace(status_mapping)
    
    # Create heatmap
    fig_heatmap = px.imshow(
        availability_numeric.values,
        labels=dict(x="Time Slots", y="Agents", color="Status"),
        x=[f"{date} {hour}:00" for date, hour in availability_numeric.columns],
        y=availability_numeric.index,
        color_continuous_scale="RdYlGn_r",
        title="Agent Availability Heatmap (Red=Busy, Green=Available)"
    )
    fig_heatmap.update_xaxes(tickangle=45)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Agent utilization summary
    st.subheader("Agent Utilization Summary")
    agent_util = availability_df.groupby('Agent')['Status'].value_counts().unstack(fill_value=0)
    if 'Busy' in agent_util.columns and 'Available' in agent_util.columns:
        agent_util['Total_Hours'] = agent_util.sum(axis=1)
        agent_util['Utilization_Rate'] = (agent_util['Busy'] / agent_util['Total_Hours'] * 100).round(1)
    
    st.dataframe(agent_util, use_container_width=True)

def conversion_manager_dashboard(leads_df):
    """Conversion Dashboard - Manager Level"""
    st.header("💰 Conversion Dashboard")
    
    # Conversion metrics
    total_leads = len(leads_df)
    converted_leads = len(leads_df[leads_df['LeadStatus'] == 'Won'])
    dropped_leads = len(leads_df[leads_df['LeadStatus'] == 'Lost'])
    in_progress_leads = total_leads - converted_leads - dropped_leads
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Leads", f"{total_leads:,}")
    with col2:
        st.metric("Converted", f"{converted_leads:,}", delta=f"{(converted_leads/total_leads*100):.1f}%")
    with col3:
        st.metric("Dropped", f"{dropped_leads:,}", delta=f"-{(dropped_leads/total_leads*100):.1f}%")
    with col4:
        st.metric("In Progress", f"{in_progress_leads:,}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Leads: Converted vs Dropped vs In Progress")
        
        conversion_data = pd.DataFrame({
            'Status': ['Converted', 'Dropped', 'In Progress'],
            'Count': [converted_leads, dropped_leads, in_progress_leads],
            'Percentage': [
                converted_leads/total_leads*100,
                dropped_leads/total_leads*100, 
                in_progress_leads/total_leads*100
            ]
        })
        
        fig_conversion = px.bar(
            conversion_data,
            x='Status',
            y='Count',
            title="Lead Conversion Status",
            color='Status',
            color_discrete_map={
                'Converted': '#90EE90',
                'Dropped': '#FFB6C1',
                'In Progress': '#87CEEB'
            }
        )
        st.plotly_chart(fig_conversion, use_container_width=True)
    
    with col2:
        st.subheader("Revenue Potential Analysis")
        
        # Revenue by status
        revenue_by_status = leads_df.groupby('LeadStatus')['RevenuePotential'].sum().reset_index()
        revenue_by_status = revenue_by_status.sort_values('RevenuePotential', ascending=False)
        
        fig_revenue = px.bar(
            revenue_by_status,
            x='LeadStatus',
            y='RevenuePotential',
            title="Revenue Potential by Lead Status",
            color='RevenuePotential',
            color_continuous_scale='Viridis'
        )
        fig_revenue.update_layout(yaxis_title="Revenue Potential ($)")
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Conversion funnel
    st.subheader("Conversion Funnel Analysis")
    funnel_data = leads_df['LeadStage'].value_counts().reset_index()
    funnel_data.columns = ['Stage', 'Count']
    
    fig_funnel = px.funnel(
        funnel_data,
        x='Count',
        y='Stage',
        title="Lead Conversion Funnel"
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

def geographic_manager_dashboard(leads_df):
    """Geographic Dashboard - Manager Level"""
    st.header("🌍 Geographic Dashboard")
    
    # Country-wise analysis
    country_stats = leads_df.groupby('Country').agg({
        'LeadId': 'count',
        'LeadStatus': lambda x: (x == 'Won').sum(),
        'RevenuePotential': 'sum'
    }).reset_index()
    country_stats.columns = ['Country', 'Total_Leads', 'Won_Leads', 'Revenue_Potential']
    country_stats['Response_Rate'] = (country_stats['Won_Leads'] / country_stats['Total_Leads'] * 100).round(1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lead Distribution by Country")
        
        fig_map = px.choropleth(
            country_stats,
            locations='Country',
            locationmode='country names',
            color='Total_Leads',
            hover_data=['Won_Leads', 'Response_Rate'],
            color_continuous_scale='Viridis',
            title="Leads by Country (Broker/Lead Distribution)"
        )
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        st.subheader("Response Rate by Country")
        
        fig_response = px.bar(
            country_stats,
            x='Country',
            y='Response_Rate',
            title="Country Response Rates",
            color='Response_Rate',
            color_continuous_scale='RdYlGn'
        )
        fig_response.update_layout(yaxis_title="Response Rate (%)")
        st.plotly_chart(fig_response, use_container_width=True)
    
    # Detailed country performance
    st.subheader("Country Performance Summary")
    st.dataframe(country_stats, use_container_width=True)
    
    # Revenue distribution pie chart
    st.subheader("Revenue Distribution by Country")
    fig_revenue_pie = px.pie(
        country_stats,
        values='Revenue_Potential',
        names='Country',
        title="Revenue Potential Distribution by Country"
    )
    st.plotly_chart(fig_revenue_pie, use_container_width=True)

# Keep existing agent_dashboard and team_lead_dashboard functions unchanged...
# [Previous dashboard functions remain the same]

def agent_dashboard(user_data, user_role):
    """Agent dashboard with personal data only"""
    st.markdown("### 👤 Agent Dashboard - Personal Performance")
    st.markdown("---")
    
    leads_df = user_data['leads']
    tasks_df = user_data['tasks']
    calls_df = user_data['calls']
    
    # Personal metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("My Leads", len(leads_df))
    with col2:
        my_won = len(leads_df[leads_df['LeadStatus'] == 'Won'])
        st.metric("Leads Won", my_won)
    with col3:
        my_calls = len(calls_df)
        st.metric("Total Calls", my_calls)
    with col4:
        pending_tasks = len(tasks_df[tasks_df['TaskStatus'] == 'Pending'])
        st.metric("Pending Tasks", pending_tasks)
    
    # Agent tabs
    tab1, tab2, tab3 = st.tabs(["📋 My Leads", "📅 My Tasks", "🤖 My Performance"])
    
    with tab1:
        if not leads_df.empty:
            status_counts = leads_df['LeadStatus'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No leads assigned yet.")
    
    with tab2:
        if not tasks_df.empty:
            st.dataframe(tasks_df[['ScheduleTitle', 'TaskType', 'ScheduledDate', 'TaskStatus']])
        else:
            st.info("No tasks assigned yet.")
    
    with tab3:
        st.metric("Personal Performance Score", "85.3%", delta="2.1%")

def team_lead_dashboard(user_data, user_role):
    """Team lead dashboard with team management features"""
    st.markdown("### 👥 Team Lead Dashboard - Team Management")
    st.markdown("---")
    
    leads_df = user_data['leads']
    
    # Team metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Team Leads", len(leads_df))
    with col2:
        team_agents = leads_df['AssignedTo'].nunique()
        st.metric("Active Agents", team_agents)
    with col3:
        won_leads = len(leads_df[leads_df['LeadStatus'] == 'Won'])
        conversion_rate = (won_leads / len(leads_df) * 100) if len(leads_df) > 0 else 0
        st.metric("Team Conversion Rate", f"{conversion_rate:.1f}%")
    
    # Agent performance comparison
    st.subheader("Team Performance Overview")
    if not leads_df.empty:
        agent_performance = leads_df.groupby('AssignedTo').agg({
            'LeadId': 'count',
            'LeadStatus': lambda x: (x == 'Won').sum()
        }).reset_index()
        agent_performance.columns = ['Agent', 'Total_Leads', 'Won_Leads']
        agent_performance['Conversion_Rate'] = (agent_performance['Won_Leads'] / agent_performance['Total_Leads'] * 100).round(1)
        
        fig = px.bar(agent_performance, x='Agent', y='Conversion_Rate', title="Agent Conversion Rates")
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(agent_performance)

# Simplified placeholder functions for other enhanced dashboards
def admin_dashboard(user_data, user_role):
    st.header("🔧 System Administration")
    st.info("System configuration, user management, and administrative tools.")

def lead_import_dashboard(user_data, user_role):
    st.header("📥 Lead Import Management")
    st.info("Excel upload, validation, and lead creation tools.")

def ai_operations_dashboard(user_data, user_role):
    st.header("🤖 AI Operations Center")
    st.info("AI calling system management and monitoring.")

def multichannel_dashboard(user_data, user_role):
    st.header("📱 Multi-Channel Communications")
    st.info("SMS, WhatsApp, and email campaign management.")

def realtime_monitoring_dashboard(user_data, user_role):
    st.header("📡 Real-time System Monitoring")
    st.info("Live system monitoring and performance tracking.")
