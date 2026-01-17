# 🎓 B.Tech Result Analysis Dashboard

A comprehensive, interactive web-based dashboard for analyzing B.Tech 5th Semester results using Streamlit and Plotly.

## 📊 Features

### Key Features

*   **📊 Interactive Dashboard**: Built with Streamlit for seamless interaction.
*   **🌙 Dark Mode UI**: Sleek, modern dark-themed interface with glassmorphism elements.
*   **🎯 Advanced Branch Analysis**: 
    *   Specific breakdown of branches (e.g., CSE - Big Data Analytics vs CSE - AI).
    *   Accurate groupings for improved comparison.
*   **📚 Deep Subject Analysis**: 
    *   Group subjects by branch to see specific performance metrics.
    *   Detailed grade distribution charts and top performer lists per subject.
*   **🔍 Student Search**: Comprehensive individual reports with subject-wise credit & grade details.
*   **📈 Visualizations**: Interactive charts powered by Plotly.vidual students by roll number or name with rankings
- **🏆 Branch Analysis**: Comprehensive branch-wise performance comparison
- **📚 Subject Analysis**: Subject difficulty analysis and performance metrics
- **📈 Advanced Analytics**: Interactive 3D visualizations and statistical deep dive
- **📥 Reports & Export**: Generate custom reports in CSV, Excel, and JSON formats

### Visualizations
- 📊 **Interactive Charts**: Plotly-based charts with zoom, hover, and pan features
- 🎨 **3D Visualizations**: Rotate-able 3D scatter plots and bar charts
- 📈 **Statistical Plots**: Box plots, histograms, heatmaps, and correlation matrices
- 📋 **Data Tables**: Styled dataframes with gradient backgrounds

## 🛠️ Tech Stack

- **Frontend Framework**: Streamlit 1.30.0
- **Visualization**: Plotly 5.18.0, Matplotlib, Seaborn
- **Data Processing**: Pandas 2.1.4, NumPy 1.26.3
- **Statistical Analysis**: SciPy 1.11.4
- **PDF Processing**: pdfplumber 0.10.3
- **Export**: openpyxl 3.1.2, fpdf2 2.7.6

## 📁 Project Structure

```
result-dashboard/
├── app.py                          # Main Streamlit app (Home page)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── data/
│   └── results_data.csv            # Result dataset (CSV format)
│
├── modules/
│   ├── __init__.py
│   ├── data_loader.py              # Data loading and caching
│   ├── analytics.py                # Statistical analysis functions
│   └── visualizations.py           # Plotly chart generators
│
└── pages/                          # Multi-page app pages
    ├── 1_🔍_Student_Search.py
    ├── 2_🏆_Branch_Analysis.py
    ├── 3_📚_Subject_Analysis.py
    ├── 4_📈_Advanced_Analytics.py
    └── 5_📥_Reports.py
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download

```bash
cd result-dashboard
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Prepare Data

1. Extract data from PDF using the extraction script:
```bash
cd ..
python extract_pdf_data.py
```

2. Move the generated `results_data.csv` to the `data/` folder:
```bash
# Windows
move results_data.csv result-dashboard\data\

# Mac/Linux
mv results_data.csv result-dashboard/data/
```

Alternatively, place your CSV file directly in the `data/` folder with the following required columns:
- `Roll_Number`, `Name`, `Branch`, `Section`, `CGPA`, `SGPA`, `Result_Status`, etc.

### Step 5: Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### Navigating the Dashboard

1. **Sidebar Navigation**: Use the sidebar to switch between different pages
2. **Interactive Charts**: Hover over charts for details, click and drag to pan, scroll to zoom
3. **3D Visualizations**: Click and drag to rotate 3D charts
4. **Filters**: Use dropdowns and sliders to filter data dynamically
5. **Export**: Download reports in various formats from the Reports page

### Expected Data Format

**CSV Column Structure:**
```csv
Roll_Number,Name,Branch,Section,Semester,CGPA,SGPA,Result_Status,Backlogs,...
2021BTCS001,Student Name,CSE,A,5,8.75,8.80,Pass,0
```

**Required Columns:**
- `Roll_Number` (string)
- `Name` (string)
- `Branch` (string)
- `CGPA` (float)
- `Result_Status` (string: "Pass" or "Fail")

**Optional Columns:**
- `Section`, `Semester`, `SGPA`, `Backlogs`, `Credits`
- Subject-specific: `Subject_Name`, `Subject_Code`, `Total_Marks`, `Letter_Grade`, `Grade_Point`

## 🎨 Features Breakdown

### Home Page
- Overall KPI metrics (Total Students, Pass %, Average CGPA, Highest CGPA)
- 4 interactive tabs: Overview, Branch Analysis, CGPA Distribution, 3D Visualization
- Branch and result status distribution pie charts
- Grade distribution charts

### Student Search
- Search by roll number or name (supports partial matches)
- Filter by branch and section
- Display individual student cards with:
  - Performance metrics (SGPA, CGPA, Backlogs, Credits)
  - Overall and branch rankings
  - Percentile calculation
  - Subject-wise breakdown table
- Download individual student reports

### Branch Analysis
- Branch comparison bar charts
- Box plots showing CGPA distribution
- Top 3 students from each branch (with medal badges)
- Grade distribution by branch
- Detailed branch statistics table
- Section-wise breakdown

### Subject Analysis
- Subject difficulty index ranking
- Performance metrics per subject
- Pass/fail percentage heatmaps (Subjects vs Branches)
- Grade distribution per subject
- Marks distribution histograms
- Statistical insights (most varied, most consistent subjects)

### Advanced Analytics
- Interactive 3D scatter plot (CGPA vs Branch vs Credits)
- 3D bar chart (Grade distribution across branches)
- Statistical deep dive (mean, median, mode, variance, IQR, etc.)
- Percentile distribution analysis
- Normality testing (skewness, kurtosis)
- Correlation heatmap
- Strong correlation identification

### Reports & Export
- Quick exports (Complete data, Branch stats, Subject stats, Toppers)
- Custom report builder with filters and column selection
- Multiple format support (CSV, Excel, JSON)
- Multi-sheet Excel workbooks
- Analytics summary report with executive summary

## ⚙️ Configuration

### Custom Styling
Edit the CSS in `app.py` to change colors, fonts, and layout.

### Data Path
By default, data is loaded from `data/results_data.csv`. To change:
```python
# In modules/data_loader.py
df = load_result_data('path/to/your/file.csv')
```

### Caching
Streamlit caches data for 1 hour by default. To change:
```python
@st.cache_data(ttl=7200)  # Cache for 2 hours
def load_result_data(filepath):
    ...
```

## 🐛 Troubleshooting

### Dashboard won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### No data displayed
- Verify `results_data.csv` exists in the `data/` folder
- Check CSV format matches expected structure
- Review browser console for errors

### Charts not rendering
- Clear Streamlit cache: Click "C" in the running dashboard
- Try different browser (Chrome recommended)
- Update Plotly: `pip install --upgrade plotly`

### Module import errors
- Ensure you're in the correct directory: `cd result-dashboard`
- Check virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub account
4. Select repository and `app.py` as main file
5. Deploy!

### Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Deploy with Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t result-dashboard .
docker run -p 8501:8501 result-dashboard
```

## 📝 License

This project is created for educational and institutional use.

## 👨‍💻 Author

**Senior Data Analyst**  
Data Analytics Department

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Plotly](https://plotly.com/python/)
- Data analysis with [Pandas](https://pandas.pydata.org/)

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the Usage Guide
3. Contact the development team

---

**Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Production Ready ✅
