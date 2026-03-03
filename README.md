<div align="center">

<img src="https://img.shields.io/badge/RESULT_ANALYTICS-Academic%20Intelligence-1A1A2E?style=for-the-badge&logoColor=white" alt="Result Analytics Dashboard" height="36"/>

# Result Analytics Dashboard

### B.Tech Semester Result Analysis & Visualization Platform

*From raw results to real insights.*

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## Overview

**Result Analytics Dashboard** is a web-based academic analytics tool built for B.Tech institutions. It transforms raw semester result data into interactive visualizations, statistical summaries, and exportable reports — covering everything from individual student profiles to department-wide performance trends.

---

## Features

| | Module | Description |
|---|---|---|
| 📊 | **Executive Overview** | Real-time KPIs, CGPA histograms, department rankings, and subject correlation matrix |
| 🔍 | **Student Search** | Search by roll number or name, radar charts, grade comparison vs. class average, rank & percentile |
| 🏆 | **Branch Analysis** | CGPA distribution by specialization, performance scatter plots, Hall of Fame top 3 |
| 📚 | **Subject Analysis** | Difficulty matrix, top 5 performers per subject, grade distribution pie charts |
| 📈 | **Advanced Analytics** | 3D performance visualizations, box plots, and full statistical summaries |
| 📥 | **Reports & Export** | CSV/Excel export, custom report generation, multi-format download support |

---

## Tech Stack

**Core**

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

**Data & Statistics**

![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white)

**Visualization**

![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)

---

## Project Structure

```
result-dashboard/
├── Homepage.py                         # Main application entry point
├── requirements.txt                    # Python dependencies
├── data/
│   └── results_data.csv               # Semester result data
├── modules/
│   ├── analytics.py                   # Statistical computation functions
│   ├── data_loader.py                 # Data ingestion & management
│   └── visualizations.py             # Chart & plot generators
└── pages/
    ├── 1_🔍_Student_Search.py
    ├── 2_🏆_Branch_Analysis.py
    ├── 3_📚_Subject_Analysis.py
    ├── 4_📈_Advanced_Analytics.py
    └── 5_📥_Reports.py
```

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run Homepage.py
```

The app will open at `http://localhost:8501`

---

## Data Format

The dashboard expects a CSV file at `data/results_data.csv` with the following columns:

| Column | Description |
|---|---|
| `Roll_Number` | Unique student identifier |
| `Name` | Student full name |
| `Branch` | Department / specialization |
| `CGPA` | Cumulative Grade Point Average |
| `SGPA` | Semester Grade Point Average |
| `Result_Status` | `PASS` or `FAIL` |
| `Subject_X_Code` | Subject code for subject X |
| `Subject_X_Grade` | Letter grade for subject X |
| `Subject_X_GradePoint` | Grade points for subject X |

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

*Built for academic excellence.*

</div>
