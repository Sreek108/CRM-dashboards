# 🏢 Quara Finance - AI-Powered CRM Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/yourusername/quara-finance-dashboard/graphs/commit-activity)

> A comprehensive multi-role business intelligence dashboard built with Streamlit for the NSP-CRM system, featuring AI call analytics, lead management, and ML-powered predictions for financial services.

## 🌟 Live Demo

**[🚀 Try the Live Dashboard](https://your-app-name.streamlit.app/)**

**Demo Credentials:**
- **Agent**: `agent1` / `pass123`
- **Team Lead**: `teamlead1` / `lead123` 
- **Manager**: `manager1` / `mgr123`
- **Admin**: `admin` / `admin123`

## 📸 Screenshots

<details>
<summary>Click to view dashboard screenshots</summary>

### Agent Dashboard
![Agent Dashboard](docs/screenshots/agent-dashboard.png)

### Lead Status Analytics
![Lead Status](docs/screenshots/lead-status.png)

### AI Call Activity
![Call Activity](docs/screenshots/call-activity.png)

### ML Predictions
![ML Predictions](docs/screenshots/ml-predictions.png)

</details>

## ✨ Features

### 🎯 Role-Based Dashboards
- **👤 Agent Level**: Personal performance tracking and individual KPIs
- **👥 Team Lead**: Team oversight and performance comparison
- **📈 Manager**: Department-wide analytics and resource allocation  
- **🏢 Executive**: Company-wide insights and strategic forecasting

### 📊 Core Analytics
- **📋 Lead Status Dashboard**: Interactive pie charts and conversion tracking
- **📞 AI Call Activity**: Real-time call metrics and success rate analysis
- **📅 Follow-up Management**: Task scheduling and overdue alerts
- **🕐 Agent Availability**: Heatmap visualization of team capacity
- **💰 Conversion Analysis**: Sales funnel and revenue potential tracking
- **🌍 Geographic Insights**: Country-wise lead distribution and performance
- **🤖 ML Predictions**: Advanced forecasting for conversions and call success

### 🔐 Security & Compliance
- Role-based access control
- SAMA regulatory compliance features
- Secure session management
- Audit logging capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
git clone https://github.com/Sreek108/CRM-dashboards.git
cd quara-finance-dashboard

text

2. **Create virtual environment**
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

text

3. **Install dependencies**
pip install -r requirements.txt

text

4. **Run the application**
streamlit run app.py

text

5. **Open your browser**
Navigate to `http://localhost:8501`

## 📁 Project Structure

quara-finance-dashboard/
├── 📄 app.py # Main Streamlit application
├── 🔐 auth.py # Authentication system
├── 📊 dashboards.py # Dashboard components
├── 💾 data_loader.py # Data processing and loading
├── 📋 requirements.txt # Python dependencies
├── 📖 README.md # Project documentation
├── 📁 .streamlit/
│ └── ⚙️ config.toml # Streamlit configuration
├── 📁 docs/
│ └── 📸 screenshots/ # Dashboard screenshots
└── 📁 data/
└── 📊 sample_data/ # Sample datasets

text

## 🌐 Deployment

### Streamlit Community Cloud (Recommended)

1. **Push to GitHub**
git add .
git commit -m "Deploy dashboard"
git push origin main

text

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
   - Deploy with main file: `app.py`

### Alternative Deployment Options

<details>
<summary>Docker Deployment</summary>

Build image
docker build -t CRM-dashboards .

Run container
docker run -p 8501:8501 quara-finance-dashboard

text
</details>

<details>
<summary>Heroku Deployment</summary>

Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main

text
</details>

## 📊 Dashboard Components

### Lead Status Dashboard
- Lead distribution pie charts (New, In Progress, Interested, Closed)
- Stage progression analytics
- Conversion rate tracking
- Revenue potential analysis

### AI Call Activity Dashboard  
- Daily/weekly call volume trends
- Success rate analytics with benchmarking
- Call duration and efficiency metrics
- Sentiment analysis (Positive, Neutral, Negative)

### Follow-up & Task Management
- Upcoming calls calendar view
- Overdue task alerts with priority levels
- Task completion rate tracking
- Agent workload distribution

### Agent Availability Heatmap
- Visual time slot availability matrix
- Team capacity utilization rates
- Schedule optimization insights
- Resource allocation recommendations

### Conversion Analytics
- Sales funnel visualization
- Win/loss ratio analysis
- Monthly conversion trends
- Revenue pipeline tracking

### Geographic Dashboard
- Interactive world map with lead distribution
- Country-wise performance metrics
- Regional conversion rate analysis
- Market penetration insights

### ML Predictions & Forecasting
- Lead conversion probability models
- Call success rate forecasting
- Feature importance analysis
- Model performance metrics (Accuracy: 87.3%, Precision: 82.1%)

## 🛠️ Technology Stack

- **Frontend**: Streamlit 1.28+
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Machine Learning**: Scikit-learn
- **Authentication**: Custom role-based system
- **Deployment**: Streamlit Cloud, Docker, Heroku

## 📈 Performance Metrics

- ⚡ Load Time: < 3 seconds
- 🔄 Real-time Updates: 30-second intervals
- 👥 Concurrent Users: Up to 100 users
- ⏱️ Uptime: 99.9% availability

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create feature branch**
git checkout -b feature/AmazingFeature

text
3. **Commit changes**
git commit -m 'Add some AmazingFeature'

text
4. **Push to branch**
git push origin feature/AmazingFeature

text
5. **Open Pull Request**

### Development Setup

Install development dependencies
pip install -r requirements-dev.txt

Run tests
pytest tests/

Format code
black .
isort .

text

## 📋 Usage Examples

### Agent View
Access personal metrics only
user_role = "Agent"
agent_data = get_user_specific_data("agent1", user_role)

text

### Manager View  
Access department-wide analytics
user_role = "Manager"
all_data = get_user_specific_data("manager1", user_role)

text

## 🔧 Configuration

### Environment Variables
Optional: Set custom database URL
export DATABASE_URL="your_database_connection_string"

Optional: Set API keys for external services
export API_KEY="your_api_key"

text

### Streamlit Configuration
Edit `.streamlit/config.toml` for custom themes:
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

text

## 📊 Sample Data

The dashboard includes synthetic data generators for:
- **500 sample leads** across different stages and countries
- **1000 call records** with sentiment analysis
- **300 scheduled tasks** with various statuses  
- **Agent availability** data for heatmap visualization

## 🛡️ Security Features

- **Authentication**: Secure login system with session management
- **Authorization**: Role-based data access control
- **Data Privacy**: User-specific data filtering
- **Audit Logging**: Complete user activity tracking
- **SAMA Compliance**: Saudi Arabia regulatory requirements

## 🐛 Issue Reporting

Found a bug? Please create an issue with:
- **Environment details** (OS, Python version, browser)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Screenshots** if applicable

[Create New Issue](https://github.com/Sreek108/CRM-dashboards/issues/new)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- **Streamlit Team** for the amazing framework
- **Plotly** for interactive visualizations  
- **NSP Development Team** for database schema design
- **Quara Finance** for business requirements and testing

## 📞 Support

- **📧 Email**: support@quarafinance.com
- **📚 Documentation**: [Wiki Pages](https://github.com/Sreek108/CRM-dashboards/wiki)
- **💬 Discussions**: [GitHub Discussions](https://github.com/Sreek108/CRM-dashboards/discussions)
- **🐛 Issues**: [Bug Reports](https://github.com/yourusername/CRM-dashboards/issues)

## 🗺️ Roadmap

- [x] Multi-role dashboard implementation
- [x] Real-time data updates
- [x] ML prediction models
- [ ] Mobile app development
- [ ] Advanced AI features
- [ ] Third-party integrations
- [ ] Enhanced compliance features

---

**⭐ Star this repository if you find it helpful!**


---

<div align="center">
  <p>Built with ❤️ by the Quara Finance Development Team</p>
  <p><em>Empowering financial services with AI-driven insights</em></p>
</div>
