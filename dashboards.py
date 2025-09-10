import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time

# [Keep existing agent_dashboard, team_lead_dashboard, manager_dashboard functions from previous version]

def lead_import_dashboard(user_data, user_role):
    """Lead Import Management Dashboard"""
    st.header("📥 Lead Import Management")
    
    # Import Status Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Imports Today", "847", delta="23")
    with col2:
        st.metric("Validation Success", "94.2%", delta="1.8%")
    with col3:
        st.metric("Duplicates Found", "52", delta="-8")
    with col4:
        st.metric("Processing Queue", "12", delta="-5")
    
    # Import workflow tabs
    import_tabs = st.tabs(["📤 Upload Center", "✅ Validation Results", "🔍 Deduplication", "📋 Lead Creation"])
    
    with import_tabs[0]:
        st.subheader("📤 Excel Upload Center")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Upload New Lead File**")
            uploaded_file = st.file_uploader("Choose Excel file", type=['xlsx', 'csv'])
            
            if uploaded_file:
                st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                
                # Simulated upload progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                if st.button("Process Upload"):
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        status_text.text(f'Processing... {i+1}%')
                        time.sleep(0.01)
                    st.success("Upload processed successfully!")
        
        with col2:
            st.markdown("**Recent Upload History**")
            upload_history = pd.DataFrame({
                'Timestamp': [
                    '2025-09-10 16:30:12', '2025-09-10 14:15:33', '2025-09-10 11:22:45'
                ],
                'Filename': ['leads_batch_147.xlsx', 'morning_leads.csv', 'partner_leads_sept.xlsx'],
                'Records': [234, 156, 389],
                'Status': ['✅ Completed', '✅ Completed', '⚠️ In Progress']
            })
            st.dataframe(upload_history)
    
    with import_tabs[1]:
        st.subheader("✅ Validation Results")
        
        # Validation metrics
        col1, col2 = st.columns(2)
        
        with col1:
            validation_data = pd.DataFrame({
                'Field': ['Email Format', 'Phone Number', 'Company Name', 'Country Code'],
                'Valid': [832, 791, 847, 823],
                'Invalid': [15, 56, 0, 24],
                'Success Rate': ['98.2%', '93.4%', '100%', '97.2%']
            })
            st.dataframe(validation_data)
        
        with col2:
            # Validation pie chart
            fig_validation = px.pie(
                values=[832, 15], 
                names=['Valid Records', 'Invalid Records'],
                title="Overall Validation Status"
            )
            st.plotly_chart(fig_validation, use_container_width=True)
    
    with import_tabs[2]:
        st.subheader("🔍 Deduplication Analysis")
        
        # Duplicate detection results
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Duplicate Detection Summary**")
            dedup_metrics = {
                'Total Records Scanned': 847,
                'Exact Duplicates Found': 23,
                'Partial Matches': 29,
                'Unique Records': 795,
                'Merge Candidates': 12
            }
            
            for metric, value in dedup_metrics.items():
                st.metric(metric, value)
        
        with col2:
            st.markdown("**Duplicate Categories**")
            duplicate_types = pd.DataFrame({
                'Type': ['Email Match', 'Phone Match', 'Name + Company', 'Full Record'],
                'Count': [18, 12, 15, 7],
                'Action': ['Auto-merge', 'Review', 'Auto-merge', 'Skip']
            })
            st.dataframe(duplicate_types)
    
    with import_tabs[3]:
        st.subheader("📋 Lead Creation Pipeline")
        
        # Lead creation workflow
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Lead Creation Status**")
            creation_flow = pd.DataFrame({
                'Stage': ['Validated Records', 'Scoring Applied', 'Agent Assigned', 'Queue Ready'],
                'Count': [795, 795, 789, 789],
                'Status': ['✅ Complete', '✅ Complete', '⚠️ In Progress', '⏳ Pending']
            })
            st.dataframe(creation_flow)
        
        with col2:
            # Lead scoring distribution
            scoring_dist = pd.DataFrame({
                'Score Range': ['HOT (16-20)', 'WARM (12-16)', 'COLD (5-11)', 'DEAD (0-4)'],
                'Count': [89, 234, 356, 116]
            })
            
            fig_scoring = px.bar(scoring_dist, x='Score Range', y='Count',
                               title="Lead Scoring Distribution")
            st.plotly_chart(fig_scoring, use_container_width=True)

def ai_operations_dashboard(user_data, user_role):
    """AI Calling Operations Dashboard"""
    st.header("🤖 AI Calling Operations Center")
    
    # AI Operations KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Active AI Agents", "8", delta="2")
    with col2:
        st.metric("Calls in Queue", "234", delta="-45")
    with col3:
        st.metric("Avg Call Duration", "3.2 min", delta="0.3 min")
    with col4:
        st.metric("Success Rate", "73.4%", delta="2.1%")
    with col5:
        st.metric("System Uptime", "99.8%", delta="0.1%")
    
    # AI Operations tabs
    ai_tabs = st.tabs([
        "🎯 Queue Management", 
        "⏰ Working Hours", 
        "📞 Call Execution", 
        "📊 AI Monitoring",
        "🔧 System Config"
    ])
    
    with ai_tabs[0]:
        st.subheader("🎯 AI Call Queue Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Current Queue Status**")
            queue_data = pd.DataFrame({
                'Priority': ['HIGH', 'MEDIUM', 'LOW'],
                'Pending Calls': [45, 128, 61],
                'Estimated Time': ['15 min', '45 min', '82 min'],
                'AI Agents Assigned': [3, 4, 1]
            })
            st.dataframe(queue_data)
            
            # Queue management controls
            st.markdown("**Queue Controls**")
            if st.button("🚀 Boost Queue Processing"):
                st.success("Queue processing boosted! Additional AI agents activated.")
            
            if st.button("⏸️ Pause Queue"):
                st.warning("Queue paused for maintenance.")
        
        with col2:
            # Queue visualization
            fig_queue = px.bar(queue_data, x='Priority', y='Pending Calls',
                              title="Call Queue by Priority")
            st.plotly_chart(fig_queue, use_container_width=True)
            
            # AI agent status
            st.markdown("**AI Agent Status**")
            agent_status = pd.DataFrame({
                'Agent ID': [f'AI-{i:03d}' for i in range(1, 9)],
                'Status': ['Active', 'Active', 'Active', 'Active', 'Idle', 'Active', 'Maintenance', 'Active'],
                'Current Call': ['Lead-2341', 'Lead-2342', 'Lead-2343', 'Lead-2344', '-', 'Lead-2345', '-', 'Lead-2346'],
                'Calls Today': [45, 52, 38, 41, 23, 47, 0, 39]
            })
            st.dataframe(agent_status)
    
    with ai_tabs[1]:
        st.subheader("⏰ Working Hours Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Global Working Hours**")
            
            # Time zone settings
            timezone = st.selectbox("Primary Timezone", 
                                   ["Asia/Riyadh", "Asia/Dubai", "Asia/Kolkata"])
            
            start_time = st.time_input("Working Hours Start", datetime.strptime("09:00", "%H:%M").time())
            end_time = st.time_input("Working Hours End", datetime.strptime("18:00", "%H:%M").time())
            
            weekend_days = st.multiselect("Weekend Days", 
                                         ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                         default=["Friday", "Saturday"])
            
            if st.button("Update Working Hours"):
                st.success("Working hours updated successfully!")
        
        with col2:
            st.markdown("**Country-Specific Settings**")
            country_hours = pd.DataFrame({
                'Country': ['Saudi Arabia', 'UAE', 'India'],
                'Local Time': ['16:30', '17:30', '18:00'],
                'Status': ['✅ Active', '✅ Active', '🔴 After Hours'],
                'Next Available': ['-', '-', '09:30 tomorrow']
            })
            st.dataframe(country_hours)
    
    with ai_tabs[2]:
        st.subheader("📞 Call Execution Monitoring")
        
        # Real-time call execution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Live Call Execution**")
            
            # Simulated real-time calls
            if st.button("🔄 Refresh Live Calls"):
                live_calls = pd.DataFrame({
                    'AI Agent': ['AI-001', 'AI-002', 'AI-003', 'AI-004'],
                    'Lead Name': ['John Smith', 'Sarah Ahmed', 'Mike Johnson', 'Fatima Ali'],
                    'Duration': ['00:02:45', '00:01:23', '00:04:12', '00:00:47'],
                    'Status': ['In Progress', 'In Progress', 'In Progress', 'Connecting'],
                    'Sentiment': ['Positive', 'Neutral', 'Interested', 'Pending']
                })
                st.dataframe(live_calls)
        
        with col2:
            # Call execution metrics
            execution_metrics = pd.DataFrame({
                'Metric': ['Connection Success', 'Call Completion', 'Positive Response', 'Callback Requested'],
                'Today': ['89.2%', '76.4%', '34.7%', '12.8%'],
                'Yesterday': ['87.5%', '74.1%', '32.3%', '11.9%'],
                'Change': ['+1.7%', '+2.3%', '+2.4%', '+0.9%']
            })
            st.dataframe(execution_metrics)
    
    with ai_tabs[3]:
        st.subheader("📊 AI Performance Monitoring")
        
        # AI performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            # AI call success over time
            hours = [f"{i:02d}:00" for i in range(9, 18)]
            success_rates = np.random.uniform(65, 85, len(hours))
            
            fig_performance = px.line(x=hours, y=success_rates,
                                    title="AI Call Success Rate - Today")
            fig_performance.update_layout(xaxis_title="Hour", yaxis_title="Success Rate (%)")
            st.plotly_chart(fig_performance, use_container_width=True)
        
        with col2:
            # Sentiment analysis
            sentiments = ['Positive', 'Neutral', 'Negative', 'Interested', 'Not Interested']
            sentiment_counts = [145, 98, 23, 67, 89]
            
            fig_sentiment = px.pie(values=sentiment_counts, names=sentiments,
                                 title="Call Sentiment Distribution")
            st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with ai_tabs[4]:
        st.subheader("🔧 AI System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**AI Model Settings**")
            
            model_version = st.selectbox("AI Model Version", 
                                       ["GPT-4-Turbo", "GPT-4", "Custom-CRM-v2.1"])
            
            conversation_style = st.selectbox("Conversation Style",
                                            ["Professional", "Friendly", "Direct", "Consultative"])
            
            retry_attempts = st.slider("Max Retry Attempts", 1, 5, 3)
            
            call_timeout = st.slider("Call Timeout (minutes)", 1, 10, 5)
            
            if st.button("Save AI Configuration"):
                st.success("AI configuration saved successfully!")
        
        with col2:
            st.markdown("**Performance Thresholds**")
            
            success_threshold = st.slider("Success Rate Threshold (%)", 50, 90, 70)
            response_time = st.slider("Max Response Time (seconds)", 5, 30, 15)
            quality_score = st.slider("Min Quality Score", 1, 10, 7)
            
            st.markdown("**Current System Status**")
            system_status = {
                'AI Engine': '🟢 Online',
                'Speech Recognition': '🟢 Active',
                'Natural Language Processing': '🟢 Optimal',
                'Call Routing': '🟢 Stable',
                'Data Pipeline': '🟢 Healthy'
            }
            
            for component, status in system_status.items():
                st.text(f"{component}: {status}")

def multichannel_dashboard(user_data, user_role):
    """Multi-channel Communication Tracking Dashboard"""
    st.header("📱 Multi-Channel Communication Hub")
    
    # Multi-channel KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("SMS Sent", "1,247", delta="156")
    with col2:
        st.metric("WhatsApp Messages", "892", delta="67")
    with col3:
        st.metric("Email Sequences", "2,341", delta="234")
    with col4:
        st.metric("Call Follow-ups", "445", delta="23")
    with col5:
        st.metric("Response Rate", "42.3%", delta="3.7%")
    
    # Multi-channel tabs
    channel_tabs = st.tabs([
        "📱 SMS/WhatsApp", 
        "📧 Email Sequences", 
        "📞 Call Follow-up", 
        "📝 Template Management",
        "📊 Channel Performance"
    ])
    
    with channel_tabs[0]:
        st.subheader("📱 SMS & WhatsApp Campaigns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Active Campaigns**")
            sms_campaigns = pd.DataFrame({
                'Campaign Name': ['Welcome Series', 'Follow-up Reminder', 'Product Demo Invite'],
                'Channel': ['SMS', 'WhatsApp', 'SMS'],
                'Status': ['Active', 'Active', 'Scheduled'],
                'Sent': [234, 156, 0],
                'Delivered': [228, 152, 0],
                'Replied': [45, 23, 0]
            })
            st.dataframe(sms_campaigns)
            
            if st.button("📱 Create New SMS Campaign"):
                st.success("New SMS campaign wizard opened!")
        
        with col2:
            # SMS/WhatsApp performance
            channel_performance = pd.DataFrame({
                'Channel': ['SMS', 'WhatsApp'],
                'Sent': [890, 456],
                'Delivered': [867, 445],
                'Read': [623, 389],
                'Replied': [89, 67]
            })
            
            fig_channels = px.bar(channel_performance, x='Channel', y=['Sent', 'Delivered', 'Read', 'Replied'],
                                title="SMS vs WhatsApp Performance")
            st.plotly_chart(fig_channels, use_container_width=True)
    
    with channel_tabs[1]:
        st.subheader("📧 Email Sequence Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Email Sequences**")
            email_sequences = pd.DataFrame({
                'Sequence Name': ['Onboarding Flow', 'Nurture Campaign', 'Re-engagement'],
                'Emails': [5, 8, 3],
                'Active Leads': [234, 456, 123],
                'Open Rate': ['34.5%', '28.7%', '22.1%'],
                'Click Rate': ['8.9%', '12.3%', '15.6%']
            })
            st.dataframe(email_sequences)
            
            if st.button("📧 Create Email Sequence"):
                st.success("Email sequence builder opened!")
        
        with col2:
            # Email performance over time
            days = pd.date_range('2025-09-01', '2025-09-10')
            email_performance = pd.DataFrame({
                'Date': days,
                'Sent': np.random.randint(200, 400, len(days)),
                'Opened': np.random.randint(50, 150, len(days)),
                'Clicked': np.random.randint(10, 50, len(days))
            })
            
            fig_email = px.line(email_performance, x='Date', y=['Sent', 'Opened', 'Clicked'],
                              title="Email Performance Trend")
            st.plotly_chart(fig_email, use_container_width=True)
    
    with channel_tabs[2]:
        st.subheader("📞 Call Follow-up Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Scheduled Follow-ups**")
            followups = pd.DataFrame({
                'Lead Name': ['Sarah Ahmed', 'Mike Johnson', 'John Smith'],
                'Last Call': ['2025-09-08', '2025-09-07', '2025-09-09'],
                'Follow-up Date': ['2025-09-11', '2025-09-10', '2025-09-12'],
                'Priority': ['High', 'Medium', 'High'],
                'Agent': ['AI-001', 'Agent-5', 'AI-002']
            })
            st.dataframe(followups)
        
        with col2:
            st.markdown("**Follow-up Performance**")
            followup_metrics = {
                'Scheduled Today': 45,
                'Completed': 32,
                'Pending': 13,
                'Success Rate': '71.1%',
                'Avg Days Between Calls': 2.3
            }
            
            for metric, value in followup_metrics.items():
                st.metric(metric, value)
    
    with channel_tabs[3]:
        st.subheader("📝 Template Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Message Templates**")
            templates = pd.DataFrame({
                'Template Name': ['Welcome SMS', 'Follow-up WhatsApp', 'Demo Invite Email'],
                'Type': ['SMS', 'WhatsApp', 'Email'],
                'Usage Count': [234, 156, 445],
                'Success Rate': ['67.8%', '72.3%', '34.5%'],
                'Last Modified': ['2025-09-08', '2025-09-05', '2025-09-10']
            })
            st.dataframe(templates)
            
            if st.button("➕ Create New Template"):
                st.success("Template editor opened!")
        
        with col2:
            st.markdown("**Template Performance**")
            template_performance = pd.DataFrame({
                'Template': ['Welcome SMS', 'Follow-up WhatsApp', 'Demo Invite'],
                'Response Rate': [67.8, 72.3, 34.5]
            })
            
            fig_templates = px.bar(template_performance, x='Template', y='Response Rate',
                                 title="Template Response Rates")
            st.plotly_chart(fig_templates, use_container_width=True)
    
    with channel_tabs[4]:
        st.subheader("📊 Channel Performance Analytics")
        
        # Cross-channel performance comparison
        col1, col2 = st.columns(2)
        
        with col1:
            channel_comparison = pd.DataFrame({
                'Channel': ['SMS', 'WhatsApp', 'Email', 'Voice Call'],
                'Cost per Contact': ['$0.05', '$0.03', '$0.02', '$0.25'],
                'Response Rate': [23.4, 34.7, 12.8, 67.2],
                'Conversion Rate': [8.9, 12.3, 4.5, 23.7]
            })
            st.dataframe(channel_comparison)
        
        with col2:
            fig_response = px.bar(channel_comparison, x='Channel', y='Response Rate',
                                title="Response Rate by Channel")
            st.plotly_chart(fig_response, use_container_width=True)

def admin_dashboard(user_data, user_role):
    """System Administration Panel"""
    st.header("🔧 System Administration Panel")
    
    # System health indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("System Health", "98.7%", delta="0.3%")
    with col2:
        st.metric("Database Load", "23%", delta="-5%")
    with col3:
        st.metric("API Response", "145ms", delta="-12ms")
    with col4:
        st.metric("Active Users", "47", delta="8")
    
    # Admin tabs
    admin_tabs = st.tabs([
        "⚙️ System Config",
        "👥 User Management", 
        "🗄️ Database Admin",
        "📊 Performance Monitor",
        "🔒 Security Center"
    ])
    
    with admin_tabs[0]:
        st.subheader("⚙️ System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Lead Scoring Configuration**")
            
            hot_range = st.slider("HOT Score Range", 15, 20, (16, 20))
            warm_range = st.slider("WARM Score Range", 10, 16, (12, 16))
            cold_range = st.slider("COLD Score Range", 4, 12, (5, 11))
            
            st.markdown("**Scoring Factors**")
            email_weight = st.slider("Email Quality Weight", 0, 100, 25)
            phone_weight = st.slider("Phone Quality Weight", 0, 100, 30)
            company_weight = st.slider("Company Size Weight", 0, 100, 20)
            source_weight = st.slider("Lead Source Weight", 0, 100, 25)
            
            if st.button("Save Scoring Config"):
                st.success("Lead scoring configuration updated!")
        
        with col2:
            st.markdown("**Agent Queue Settings**")
            
            max_leads_per_agent = st.number_input("Max Leads per Agent", 1, 100, 25)
            queue_priority_system = st.selectbox("Queue Priority", 
                                               ["FIFO", "Score-based", "Time-weighted"])
            
            auto_assignment = st.checkbox("Auto-assignment Enabled", True)
            round_robin = st.checkbox("Round Robin Assignment", False)
            
            st.markdown("**Performance Thresholds**")
            min_call_success = st.slider("Min Call Success Rate (%)", 50, 90, 65)
            max_response_time = st.slider("Max Response Time (hours)", 1, 48, 24)
            
            if st.button("Update Queue Settings"):
                st.success("Queue configuration updated!")
    
    with admin_tabs[1]:
        st.subheader("👥 User Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Active Users**")
            users = pd.DataFrame({
                'Username': ['admin', 'manager1', 'teamlead1', 'agent1', 'agent2'],
                'Role': ['Admin', 'Manager', 'Team Lead', 'Agent', 'Agent'],
                'Status': ['Online', 'Online', 'Away', 'Online', 'Offline'],
                'Last Login': ['16:45', '16:30', '15:22', '16:48', '14:15'],
                'Permissions': ['Full', 'View All', 'Team Only', 'Personal', 'Personal']
            })
            st.dataframe(users)
            
            if st.button("➕ Add New User"):
                st.success("User creation form opened!")
        
        with col2:
            st.markdown("**Role Permissions Matrix**")
            permissions = pd.DataFrame({
                'Permission': ['View All Data', 'Modify Leads', 'System Config', 'User Management', 'Export Data'],
                'Admin': ['✅', '✅', '✅', '✅', '✅'],
                'Manager': ['✅', '✅', '❌', '❌', '✅'],
                'Team Lead': ['🔶', '✅', '❌', '❌', '🔶'],
                'Agent': ['❌', '🔶', '❌', '❌', '❌']
            })
            st.dataframe(permissions)
    
    with admin_tabs[2]:
        st.subheader("🗄️ Database Administration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Database Statistics**")
            db_stats = {
                'Total Leads': '15,847',
                'Total Calls': '45,923',
                'Total Tasks': '8,234',
                'Database Size': '2.34 GB',
                'Last Backup': '2025-09-10 03:00'
            }
            
            for stat, value in db_stats.items():
                st.metric(stat, value)
            
            if st.button("🗄️ Backup Database"):
                st.success("Database backup initiated!")
            
            if st.button("🔄 Sync External Data"):
                st.info("External data sync in progress...")
        
        with col2:
            st.markdown("**Table Sizes**")
            table_sizes = pd.DataFrame({
                'Table': ['Lead', 'LeadCallRecord', 'LeadSchedule', 'LeadTransaction'],
                'Records': ['15,847', '45,923', '8,234', '23,567'],
                'Size (MB)': ['145.7', '892.3', '67.2', '234.5'],
                'Growth Rate': ['+12%', '+23%', '+8%', '+15%']
            })
            st.dataframe(table_sizes)
    
    with admin_tabs[3]:
        st.subheader("📊 Performance Monitor")
        
        # System performance metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # CPU and Memory usage over time
            hours = [f"{i:02d}:00" for i in range(9, 18)]
            cpu_usage = np.random.uniform(20, 80, len(hours))
            memory_usage = np.random.uniform(30, 90, len(hours))
            
            performance_df = pd.DataFrame({
                'Time': hours,
                'CPU Usage': cpu_usage,
                'Memory Usage': memory_usage
            })
            
            fig_perf = px.line(performance_df, x='Time', y=['CPU Usage', 'Memory Usage'],
                             title="System Resource Usage")
            st.plotly_chart(fig_perf, use_container_width=True)
        
        with col2:
            st.markdown("**Current System Load**")
            current_metrics = {
                'CPU Usage': '34.5%',
                'Memory Usage': '67.8%',
                'Disk I/O': '12.3%',
                'Network Usage': '23.4%',
                'Active Connections': '156'
            }
            
            for metric, value in current_metrics.items():
                st.metric(metric, value)
    
    with admin_tabs[4]:
        st.subheader("🔒 Security Center")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Security Alerts**")
            security_alerts = pd.DataFrame({
                'Timestamp': ['16:45:23', '15:32:11', '14:28:45'],
                'Type': ['Login Attempt', 'Data Export', 'Config Change'],
                'User': ['admin', 'manager1', 'admin'],
                'Status': ['✅ Success', '⚠️ Review', '✅ Authorized'],
                'IP Address': ['192.168.1.10', '10.0.0.25', '192.168.1.10']
            })
            st.dataframe(security_alerts)
        
        with col2:
            st.markdown("**Access Control**")
            access_settings = {
                'Failed Login Threshold': 3,
                'Session Timeout (minutes)': 120,
                'Password Expiry (days)': 90,
                'Two-Factor Authentication': 'Enabled',
                'IP Whitelist': 'Active'
            }
            
            for setting, value in access_settings.items():
                st.text(f"{setting}: {value}")

def realtime_monitoring_dashboard(user_data, user_role):
    """Real-time System Monitoring Dashboard"""
    st.header("📡 Real-time System Monitoring")
    
    # Real-time indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Live Calls", "12", delta="2")
    with col2:
        st.metric("Queue Length", "234", delta="-15")
    with col3:
        st.metric("System Load", "67%", delta="-3%")
    with col4:
        st.metric("Response Time", "1.2s", delta="-0.3s")
    
    # Real-time monitoring tabs
    monitor_tabs = st.tabs([
        "🔴 Live Operations",
        "📈 Real-time Analytics", 
        "⚠️ System Alerts",
        "🎯 Performance KPIs"
    ])
    
    with monitor_tabs[0]:
        st.subheader("🔴 Live Operations Monitor")
        
        # Auto-refresh functionality
        auto_refresh = st.checkbox("🔄 Auto-refresh (5 seconds)")
        
        if auto_refresh:
            placeholder = st.empty()
            
            # Simulate real-time data updates
            for i in range(12):  # 1 minute of updates
                with placeholder.container():
                    current_time = datetime.now()
                    
                    # Live call status
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**🔴 Live Calls in Progress**")
                        live_calls = pd.DataFrame({
                            'AI Agent': [f'AI-{j:03d}' for j in range(1, 8)],
                            'Lead Name': [f'Lead-{2340+j}' for j in range(7)],
                            'Duration': [f'00:0{np.random.randint(1,9)}:{np.random.randint(10,59)}' for _ in range(7)],
                            'Status': np.random.choice(['Connecting', 'In Progress', 'Wrapping Up'], 7),
                            'Sentiment': np.random.choice(['Positive', 'Neutral', 'Interested'], 7)
                        })
                        st.dataframe(live_calls)
                    
                    with col2:
                        st.markdown("**📊 Live Metrics**")
                        live_metrics = {
                            'Calls This Hour': np.random.randint(45, 65),
                            'Success Rate': f"{np.random.uniform(70, 85):.1f}%",
                            'Avg Call Duration': f"{np.random.uniform(2.5, 4.0):.1f} min",
                            'Queue Wait Time': f"{np.random.randint(2, 8)} min"
                        }
                        
                        for metric, value in live_metrics.items():
                            st.metric(metric, value)
                
                time.sleep(5)  # 5-second refresh
        else:
            # Static view when auto-refresh is off
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Current Active Operations**")
                operations = pd.DataFrame({
                    'Operation': ['AI Calling', 'Lead Import', 'Email Campaign', 'Data Sync'],
                    'Status': ['🟢 Active', '🟡 Processing', '🟢 Running', '🔵 Scheduled'],
                    'Progress': ['67%', '23%', '89%', '0%'],
                    'ETA': ['45 min', '12 min', '15 min', '2 hours']
                })
                st.dataframe(operations)
            
            with col2:
                # System resource usage
                resource_usage = pd.DataFrame({
                    'Resource': ['CPU', 'Memory', 'Disk', 'Network'],
                    'Current Usage': [34, 67, 23, 45],
                    'Peak Today': [78, 89, 56, 67]
                })
                
                fig_resources = px.bar(resource_usage, x='Resource', y=['Current Usage', 'Peak Today'],
                                     title="System Resource Usage")
                st.plotly_chart(fig_resources, use_container_width=True)
    
    with monitor_tabs[1]:
        st.subheader("📈 Real-time Analytics")
        
        # Real-time performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Simulated real-time call volume
            minutes = pd.date_range(start=datetime.now().replace(second=0, microsecond=0) - timedelta(minutes=30), 
                                  periods=30, freq='1min')
            call_volume = np.random.poisson(3, 30)  # Poisson distribution for call arrivals
            
            realtime_df = pd.DataFrame({
                'Time': minutes,
                'Calls': call_volume
            })
            
            fig_realtime = px.line(realtime_df, x='Time', y='Calls',
                                 title="Call Volume - Last 30 Minutes")
            st.plotly_chart(fig_realtime, use_container_width=True)
        
        with col2:
            # Success rate trend
            success_rates = np.random.uniform(65, 85, 30)
            success_df = pd.DataFrame({
                'Time': minutes,
                'Success Rate': success_rates
            })
            
            fig_success = px.line(success_df, x='Time', y='Success Rate',
                                title="Success Rate Trend")
            st.plotly_chart(fig_success, use_container_width=True)
    
    with monitor_tabs[2]:
        st.subheader("⚠️ System Alerts & Notifications")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Recent Alerts**")
            alerts = pd.DataFrame({
                'Time': ['17:02:34', '16:58:12', '16:45:23', '16:32:11'],
                'Level': ['⚠️ Warning', '✅ Info', '🔴 Critical', '✅ Info'],
                'Component': ['AI Engine', 'Database', 'Call Router', 'User Auth'],
                'Message': ['High queue load detected', 'Backup completed', 'Connection timeout', 'New user login'],
                'Status': ['Active', 'Resolved', 'Investigating', 'Resolved']
            })
            st.dataframe(alerts)
        
        with col2:
            st.markdown("**Alert Statistics**")
            alert_stats = {
                'Critical Alerts Today': 2,
                'Warnings Today': 8,
                'Info Messages': 45,
                'Avg Resolution Time': '12 min',
                'Open Issues': 1
            }
            
            for stat, value in alert_stats.items():
                st.metric(stat, value)
    
    with monitor_tabs[3]:
        st.subheader("🎯 Performance KPIs Dashboard")
        
        # KPI grid
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.metric("System Availability", "99.87%", delta="0.02%")
            st.metric("API Response Time", "145ms", delta="-12ms")
        
        with kpi_col2:
            st.metric("Database Performance", "94.2%", delta="1.3%")
            st.metric("Queue Processing Rate", "85 leads/hour", delta="12")
        
        with kpi_col3:
            st.metric("AI Model Accuracy", "87.3%", delta="0.8%")
            st.metric("User Satisfaction", "4.6/5", delta="0.1")
        
        with kpi_col4:
            st.metric("Data Sync Success", "98.9%", delta="0.2%")
            st.metric("Security Score", "96/100", delta="2")
        
        # Performance trend chart
        performance_trend = pd.DataFrame({
            'Date': pd.date_range('2025-09-01', '2025-09-10'),
            'System Health': np.random.uniform(95, 99.5, 10),
            'User Satisfaction': np.random.uniform(4.2, 4.8, 10),
            'Processing Efficiency': np.random.uniform(85, 95, 10)
        })
        
        fig_trend = px.line(performance_trend, x='Date', 
                          y=['System Health', 'User Satisfaction', 'Processing Efficiency'],
                          title="Key Performance Trends")
        st.plotly_chart(fig_trend, use_container_width=True)

# Keep existing agent_dashboard, team_lead_dashboard, manager_dashboard functions
# [Previous dashboard functions remain unchanged]
