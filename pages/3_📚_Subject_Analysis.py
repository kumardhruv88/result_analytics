"""
Subject-wise Analysis Page
Comprehensive subject performance analysis by branch
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_loader import load_result_data

st.set_page_config(page_title="Subject Analysis", page_icon="📚", layout="wide")

st.title("📚 Subject-wise Analysis")
st.markdown("### Deep Dive into Subject Performance by Branch")
st.markdown("---")

# Load data
df = load_result_data()

if df.empty:
    st.error("⚠️ No data available.")
    st.stop()

# Helper to transform wide data to long format
@st.cache_data
def get_subject_performance_data(df):
    """
    Transform wide format (Subject_1, Subject_2...) into long format
    Returns DataFrame with [Roll_Number, Branch, Subject_Code, Grade, Grade_Point, Credits]
    """
    subject_records = []
    
    # Determine branch column
    branch_col = 'Branch_Specialization' if 'Branch_Specialization' in df.columns else 'Branch'
    
    for _, row in df.iterrows():
        branch = row.get(branch_col, 'Unknown')
        roll = row.get('Roll_Number', 'Unknown')
        name = row.get('Name', 'Unknown')
        
        for i in range(1, 8):
            code_col = f'Subject_{i}_Code'
            grade_col = f'Subject_{i}_Grade'
            gp_col = f'Subject_{i}_GradePoint'
            cred_col = f'Subject_{i}_Credits'
            
            if code_col in row and pd.notna(row[code_col]):
                subject_records.append({
                    'Roll_Number': roll,
                    'Name': name,
                    'Branch': branch,
                    'Subject_Code': row[code_col],
                    'Grade': row.get(grade_col, 'N/A'),
                    'Grade_Point': pd.to_numeric(row.get(gp_col, 0), errors='coerce'),
                    'Credits': pd.to_numeric(row.get(cred_col, 0), errors='coerce')
                })
    
    return pd.DataFrame(subject_records)

# Get processed data
with st.spinner("Processing subject data..."):
    subject_df = get_subject_performance_data(df)

if subject_df.empty:
    st.warning("No subject details found in the dataset.")
    st.stop()

# --- Sidebar Controls ---
st.sidebar.header("🎯 Filter Options")

# Branch Selection
branches = sorted(subject_df['Branch'].unique().tolist())
selected_branch = st.sidebar.selectbox("Select Branch", branches)

# Filter data for selected branch
branch_data = subject_df[subject_df['Branch'] == selected_branch]

# --- Main Content ---

# 1. Overview for this Branch
st.markdown(f"## 🏛️ Analysis for: **{selected_branch}**")

# Professional Metric Row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Subjects", branch_data['Subject_Code'].nunique(), help="Unique subjects taught in this branch")
with col2:
    avg_gp = branch_data['Grade_Point'].mean()
    st.metric("Avg Grade Point", f"{avg_gp:.2f}", delta="Branch Average")
with col3:
    total_records = len(branch_data)
    st.metric("Total Enrollments", f"{total_records:,}")

st.divider()

# 2. Subject Performance Table
st.subheader("📊 Subject Performance Matrix")

# Group by Subject Code
subject_stats = branch_data.groupby('Subject_Code').agg({
    'Roll_Number': 'count',
    'Grade_Point': 'mean',
    'Grade': lambda x: (x == 'F').sum(),  # Count failures
    'Credits': 'first' # Assuming credits are same for subject
}).reset_index()

subject_stats.columns = ['Subject Code', 'Students', 'Avg Grade Point', 'Failures', 'Credits']

# Add Pass Percentage
subject_stats['Pass Percentage'] = ((subject_stats['Students'] - subject_stats['Failures']) / subject_stats['Students'] * 100).round(1)
subject_stats['Avg Grade Point'] = subject_stats['Avg Grade Point'].round(2)

# Sort by difficulty (lowest GPA first)
subject_stats = subject_stats.sort_values('Avg Grade Point')

# Diplay interactive dataframe with professional styling
st.dataframe(
    subject_stats.style.background_gradient(subset=['Avg Grade Point'], cmap='RdYlGn', vmin=4, vmax=10)
    .background_gradient(subset=['Pass Percentage'], cmap='Blues', vmin=50, vmax=100)
    .format({'Avg Grade Point': '{:.2f}', 'Pass Percentage': '{:.1f}%'}),
    use_container_width=True,
    height=400
)

# 3. Deep Dive into a specific subject
st.markdown("### 🔍 Deep Dive Analysis")

selected_subject_code = st.selectbox(
    "Select Subject to Inspect",
    subject_stats['Subject Code'].tolist()
)

if selected_subject_code:
    specific_subject_data = branch_data[branch_data['Subject_Code'] == selected_subject_code]
    
    st.markdown(f"#### 📘 Performance in: {selected_subject_code}")
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("**DISTRIBUTION**")
        grade_counts = specific_subject_data['Grade'].value_counts()
        
        fig = px.pie(
            values=grade_counts.values,
            names=grade_counts.index,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title=f"Grade Distribution"
        )
        fig.update_layout(height=350, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.markdown("**TOP PERFORMERS**")
        
        # Get top 5 students for this subject
        top_students = specific_subject_data.nlargest(5, 'Grade_Point')
        
        # Display top students with Names
        st.info(f"Top 5 scorers in {selected_subject_code}")
        
        # Format table
        top_display = top_students[['Roll_Number', 'Name', 'Grade', 'Grade_Point']].reset_index(drop=True)
        top_display.index += 1
        
        st.dataframe(
            top_display.style.background_gradient(subset=['Grade_Point'], cmap='Greens'), 
            use_container_width=True
        )

