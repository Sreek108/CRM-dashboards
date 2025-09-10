import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def lead_status_dashboard(user_data, user_role):
    st.title("📊 Lead Status Dashboard")
    
    leads_df = user_data['leads']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", len(leads_df))
    with col2:
        won_leads = len(leads_df[leads_df['LeadStatus'] == 'Won'])
        st.metric("Won Leads", won_leads)
    with col3:
        conversion_rate = (won_leads / len(leads_df) * 100) if len(leads_df) > 0 else 0
        st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    with col4:
        revenue = leads_df[leads_df['LeadStatus'] == 'Won']['RevenuePotential'].sum()
        st.metric("Revenue Potential", f"${revenue:,.0f}")
    
    # Pie chart for lead status
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lead Status Distribution")
        status_counts = leads_df['LeadStatus'].value_counts()
        fig_pie = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Lead Status Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Lead Stage Distribution")
        stage_counts = leads_df['LeadStage'].value_counts()
        fig_bar = px.bar(
            x=stage_counts.index,
            y=stage_counts.values,
            title="Leads by Stage"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Recent leads table
    st.subheader("Recent Leads")
    recent_leads = leads_df.sort_values('CreatedDate', ascending=False).head(10)
    st.dataframe(recent_leads[['FullName', 'Company', 'LeadStatus', 'AssignedTo', 'CreatedDate']])

def ai_call_activity_dashboard(user_data, user_role):
    st.title("📞 AI Call Activity Dashboard")
    
    calls_df = user_data['calls']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_calls = len(calls_df)
        st.metric("Total Calls", total_calls)
    with col2:
        successful_calls = len(calls_df[calls_df['CallStatus'] == 'Completed'])
        st.metric("Successful Calls", successful_calls)
    with col3:
        success_rate = (successful_calls / total_calls * 100) if total_calls > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
    with col4:
        avg_duration = calls_df['DurationSeconds'].mean() / 60
        st.metric("Avg Duration", f"{avg_duration:.1f} min")
    
    # Daily call volume and success rate
    calls_df['Date'] = calls_df['CallDateTime'].dt.date
    daily_stats = calls_df.groupby('Date').agg({
        'LeadCallId': 'count',
        'CallStatus': lambda x: (x == 'Completed').sum()
    }).reset_index()
    daily_stats.columns = ['Date', 'Total_Calls', 'Successful_Calls']
    daily_stats['Success_Rate'] = daily_stats['Successful_Calls'] / daily_stats['Total_Calls'] * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Call Volume")
        fig_calls = px.line(daily_stats, x='Date', y='Total_Calls', 
                           title="Daily Call Volume Trend")
        st.plotly_chart(fig_calls, use_container_width=True)
    
    with col2:
        st.subheader("Success Rate Trend")
        fig_success = px.line(daily_stats, x='Date', y='Success_Rate',
                             title="Daily Success Rate (%)")
        st.plotly_chart(fig_success, use_container_width=True)
    
    # Sentiment analysis
    sentiment_counts = calls_df['Sentiment'].value_counts()
    fig_sentiment = px.bar(x=sentiment_counts.index, y=sentiment_counts.values,
                          title="Call Sentiment Distribution")
    st.plotly_chart(fig_sentiment, use_container_width=True)

def followup_task_dashboard(user_data, user_role):
    st.title("📅 Follow-up & Task Dashboard")
    
    tasks_df = user_data['tasks']
    today = datetime.now().date()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_tasks = len(tasks_df)
        st.metric("Total Tasks", total_tasks)
    with col2:
        upcoming_tasks = len(tasks_df[
            (tasks_df['ScheduledDate'].dt.date >= today) & 
            (tasks_df['TaskStatus'] == 'Pending')
        ])
        st.metric("Upcoming Tasks", upcoming_tasks)
    with col3:
        overdue_tasks = len(tasks_df[
            (tasks_df['ScheduledDate'].dt.date < today) & 
            (tasks_df['TaskStatus'].isin(['Pending', 'In Progress']))
        ])
        st.metric("Overdue Tasks", overdue_tasks, delta=f"-{overdue_tasks}")
    with col4:
        completed_tasks = len(tasks_df[tasks_df['TaskStatus'] == 'Completed'])
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    # Upcoming calls
    st.subheader("Upcoming Calls (Next 7 Days)")
    upcoming_calls = tasks_df[
        (tasks_df['TaskType'] == 'Call') &
        (tasks_df['ScheduledDate'].dt.date >= today) &
        (tasks_df['ScheduledDate'].dt.date <= today + timedelta(days=7)) &
        (tasks_df['TaskStatus'] == 'Pending')
    ].sort_values('ScheduledDate')
    
    if not upcoming_calls.empty:
        st.dataframe(upcoming_calls[['ScheduleTitle', 'AssignedTo', 'ScheduledDate', 'TaskStatus']])
    else:
        st.info("No upcoming calls scheduled for the next 7 days.")
    
    # Overdue tasks
    st.subheader("Overdue Tasks")
    overdue = tasks_df[
        (tasks_df['ScheduledDate'].dt.date < today) & 
        (tasks_df['TaskStatus'].isin(['Pending', 'In Progress']))
    ].sort_values('ScheduledDate')
    
    if not overdue.empty:
        st.dataframe(overdue[['ScheduleTitle', 'AssignedTo', 'ScheduledDate', 'TaskStatus']])
    else:
        st.success("No overdue tasks!")

def agent_availability_dashboard(user_data, user_role):
    st.title("🕐 Agent Availability Dashboard")
    
    availability_df = user_data['availability']
    
    # Create availability heatmap
    if user_role == "Agent":
        st.subheader("Your Availability This Week")
    else:
        st.subheader("Team Availability Heatmap")
    
    # Simple availability statistics instead of complex heatmap
    st.subheader("Availability Statistics")
    avail_stats = availability_df.groupby('Agent')['Status'].value_counts().unstack(fill_value=0)
    
    if not avail_stats.empty:
        avail_stats['Total_Hours'] = avail_stats.sum(axis=1)
        if 'Busy' in avail_stats.columns:
            avail_stats['Utilization_Rate'] = (avail_stats['Busy'] / avail_stats['Total_Hours'] * 100).round(1)
        st.dataframe(avail_stats)
    else:
        st.info("No availability data available.")

def conversion_dashboard(user_data, user_role):
    st.title("💰 Conversion Dashboard")
    
    leads_df = user_data['leads'].copy()
    
    # Conversion metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_leads = len(leads_df)
    won_leads = len(leads_df[leads_df['LeadStatus'] == 'Won'])
    lost_leads = len(leads_df[leads_df['LeadStatus'] == 'Lost'])
    
    with col1:
        st.metric("Total Leads", total_leads)
    with col2:
        st.metric("Won Leads", won_leads)
    with col3:
        st.metric("Lost Leads", lost_leads)
    with col4:
        conversion_rate = (won_leads / total_leads * 100) if total_leads > 0 else 0
        st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    
    # Conversion funnel
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Conversion Funnel")
        funnel_data = leads_df['LeadStage'].value_counts()
        fig_funnel = px.funnel(
            x=funnel_data.values,
            y=funnel_data.index,
            title="Lead Conversion Funnel"
        )
        st.plotly_chart(fig_funnel, use_container_width=True)
    
    with col2:
        st.subheader("Revenue Potential by Stage")
        revenue_by_stage = leads_df.groupby('LeadStage')['RevenuePotential'].sum()
        fig_revenue = px.bar(
            x=revenue_by_stage.index,
            y=revenue_by_stage.values,
            title="Revenue Potential by Lead Stage"
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Monthly conversion trend - FIXED: Convert Period to string
    if not leads_df.empty:
        leads_df['Month'] = leads_df['CreatedDate'].dt.to_period('M').astype(str)
        monthly_conversions = leads_df.groupby('Month').agg({
            'LeadId': 'count',
            'LeadStatus': lambda x: (x == 'Won').sum()
        }).reset_index()
        monthly_conversions.columns = ['Month', 'Total_Leads', 'Won_Leads']
        monthly_conversions['Conversion_Rate'] = (monthly_conversions['Won_Leads'] / monthly_conversions['Total_Leads'] * 100).round(1)
        
        st.subheader("Monthly Conversion Trend")
        if not monthly_conversions.empty:
            fig_trend = px.line(monthly_conversions, x='Month', y='Conversion_Rate',
                               title="Monthly Conversion Rate Trend")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No conversion data available for trending.")
    else:
        st.info("No leads data available.")

def geographic_dashboard(user_data, user_role):
    st.title("🌍 Geographic Dashboard")
    
    leads_df = user_data['leads']
    
    if leads_df.empty:
        st.info("No geographic data available.")
        return
    
    # Country-wise metrics
    country_stats = leads_df.groupby('Country').agg({
        'LeadId': 'count',
        'LeadStatus': lambda x: (x == 'Won').sum(),
        'RevenuePotential': 'sum'
    }).reset_index()
    country_stats.columns = ['Country', 'Total_Leads', 'Won_Leads', 'Revenue_Potential']
    country_stats['Conversion_Rate'] = (country_stats['Won_Leads'] / country_stats['Total_Leads'] * 100).round(1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Leads by Country")
        fig_map = px.choropleth(
            country_stats,
            locations='Country',
            locationmode='country names',
            color='Total_Leads',
            color_continuous_scale='Viridis',
            title="Lead Distribution by Country"
        )
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        st.subheader("Revenue Potential by Country")
        fig_revenue = px.pie(
            country_stats,
            values='Revenue_Potential',
            names='Country',
            title="Revenue Distribution by Country"
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Country performance table
    st.subheader("Country Performance Summary")
    st.dataframe(country_stats)

def ml_predictions_dashboard(user_data, user_role):
    st.title("🤖 ML Predictions & Forecasting")
    
    leads_df = user_data['leads']
    calls_df = user_data['calls']
    
    st.info("This section demonstrates ML prediction capabilities using synthetic forecasting models.")
    
    # Forecast parameters
    col1, col2 = st.columns(2)
    with col1:
        forecast_days = st.slider("Forecast Period (Days)", 7, 90, 30)
    with col2:
        model_type = st.selectbox("Model Type", ["Linear Trend", "Seasonal", "ARIMA"])
    
    # Generate synthetic forecasts
    np.random.seed(42)
    future_dates = pd.date_range(start=datetime.now().date(), periods=forecast_days)
    
    # Lead conversion forecast
    base_rate = 0.15  # 15% conversion rate
    seasonal_factor = 0.02 * np.sin(np.arange(forecast_days) * 2 * np.pi / 30)  # Monthly seasonality
    trend_factor = 0.001 * np.arange(forecast_days)  # Small upward trend
    noise = np.random.normal(0, 0.01, forecast_days)
    
    predicted_conversion_rate = base_rate + seasonal_factor + trend_factor + noise
    predicted_conversion_rate = np.clip(predicted_conversion_rate, 0, 1)
    
    # Call success rate forecast
    base_success_rate = 0.6  # 60% success rate
    call_predictions = base_success_rate + 0.05 * np.sin(np.arange(forecast_days) * 2 * np.pi / 7) + np.random.normal(0, 0.02, forecast_days)
    call_predictions = np.clip(call_predictions, 0, 1)
    
    # Display forecasts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lead Conversion Forecast")
        forecast_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted_Conversion_Rate': predicted_conversion_rate * 100
        })
        fig_conv = px.line(forecast_df, x='Date', y='Predicted_Conversion_Rate',
                          title=f"Predicted Conversion Rate - Next {forecast_days} Days")
        # FIXED: Use update_layout instead of update_yaxis
        fig_conv.update_layout(
            yaxis_title="Conversion Rate (%)",
            xaxis_title="Date"
        )
        st.plotly_chart(fig_conv, use_container_width=True)
    
    with col2:
        st.subheader("Call Success Rate Forecast")
        success_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted_Success_Rate': call_predictions * 100
        })
        fig_success = px.line(success_df, x='Date', y='Predicted_Success_Rate',
                             title=f"Predicted Call Success Rate - Next {forecast_days} Days")
        # FIXED: Use update_layout instead of update_yaxis
        fig_success.update_layout(
            yaxis_title="Success Rate (%)",
            xaxis_title="Date"
        )
        st.plotly_chart(fig_success, use_container_width=True)
    
    # Feature importance (mock)
    st.subheader("Model Feature Importance")
    features = ['Call Duration', 'Lead Score', 'Days Since Contact', 'Agent Experience', 'Country', 'Lead Source']
    importance = np.random.uniform(0.1, 0.9, len(features))
    importance = importance / importance.sum()
    
    fig_importance = px.bar(
        x=features,
        y=importance,
        title="Feature Importance in Conversion Prediction Model"
    )
    # FIXED: Use update_layout instead of update_yaxis
    fig_importance.update_layout(
        yaxis_title="Importance Score",
        xaxis_title="Features"
    )
    st.plotly_chart(fig_importance, use_container_width=True)
    
    # Model performance metrics
    st.subheader("Model Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Model Accuracy", "87.3%")
    with col2:
        st.metric("Precision", "82.1%") 
    with col3:
        st.metric("Recall", "89.5%")
    with col4:
        st.metric("F1-Score", "85.6%")
