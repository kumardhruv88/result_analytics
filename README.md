# 🎓 Result Analytics Dashboard

A professional web-based dashboard for analyzing B.Tech semester results with interactive visualizations and comprehensive statistical insights.

## ✨ Features

### 📊 **Executive Overview**
- Real-time KPIs: Total students, pass rates, average CGPA, top performers
- CGPA distribution histogram with quartile analysis
- Department performance rankings
- Statistical correlation matrix for subject-grade relationships

### 🔍 **Student Search**
- Search by roll number or name
- Individual performance profiles with radar charts
- Subject-wise grade comparison vs. class average
- Class rank and percentile tracking

### 🏆 **Branch Analysis**
- CGPA distribution by specialization  
- Performance decay curve (rank vs. CGPA scatter plot)
- Top 3 Hall of Fame with medal badges
- Detailed student records table with download option

### 📚 **Subject Analysis**
- Subject difficulty matrix (average grade points, pass rates)
- Top 5 performers per subject with names
- Grade distribution pie charts
- Branch-wise subject performance grouping

### 📈 **Advanced Analytics**
- Interactive 3D performance visualizations
- Box plots for CGPA distribution
- Statistical summaries (mean, median, std deviation)

### 📥 **Reports & Export**
- CSV/Excel export for all data views
- Custom report generation
- Multi-format download support

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Statistics**: SciPy

## 📁 Project Structure

```
result-dashboard/
├── Homepage.py              # Main application
├── requirements.txt         # Dependencies
├── data/
│   └── results_data.csv    # Result data
├── modules/
│   ├── analytics.py        # Statistical functions
│   ├── data_loader.py      # Data management
│   └── visualizations.py   # Chart generators
└── pages/
    ├── 1_🔍_Student_Search.py
    ├── 2_🏆_Branch_Analysis.py
    ├── 3_📚_Subject_Analysis.py
    ├── 4_📈_Advanced_Analytics.py
    └── 5_📥_Reports.py
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run Homepage.py
```

The app will open at `http://localhost:8501`

## 📊 Data Format

Your CSV should include:
- `Roll_Number`, `Name`, `Branch`, `CGPA`, `SGPA`  
- `Result_Status` (PASS/FAIL)
- Subject columns: `Subject_X_Code`, `Subject_X_Grade`, `Subject_X_GradePoint`

---

**Built with ❤️ for academic excellence**
