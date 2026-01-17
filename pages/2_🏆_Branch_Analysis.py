"""
Branch-wise Analysis Page
Comprehensive branch performance comparison and detailed student lists
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_loader import load_result_data
from modules.visualizations import create_branch_comparison_chart, create_box_plot

st.set_page_config(page_title="Branch Analysis", page_icon="🏆", layout="wide")

st.title("🏆 Branch-wise Analysis")
st.markdown("### 🏛️ Detailed Branch Report & Student Lists")
st.markdown("---")

# Load data
df = load_result_data()

if df.empty:
    st.error("⚠️ No data available.")
    st.stop()

# --- Helpers ---
def get_student_best_worst_subject(row):
    """Find best and worst subject for a student row"""
    subjects = []
    for i in range(1, 8):
        code = row.get(f'Subject_{i}_Code')
        gp = row.get(f'Subject_{i}_GradePoint')
        if pd.notna(code) and pd.notna(gp):
            try:
                subjects.append((code, float(gp)))
            except:
                pass
    
    if not subjects:
        return "N/A", "N/A"
    
    # Sort by grade point
    subjects.sort(key=lambda x: x[1], reverse=True)
    
    best_sub = f"{subjects[0][0]} ({int(subjects[0][1])})"
    worst_sub = f"{subjects[-1][0]} ({int(subjects[-1][1])})"
    
    return best_sub, worst_sub

# --- Sidebar / Top Filters ---
col_filter1, col_filter2 = st.columns([3, 1])

with col_filter1:
    # Toggle logic restored if user wants to switch context
    branch_column = 'Branch_Specialization' if 'Branch_Specialization' in df.columns else 'Branch'
    
    # Main Branch Selector
    all_branches = sorted(df[branch_column].unique().tolist())
    selected_branch = st.selectbox("👉 Select Branch to Analyze", all_branches)

# Filter Data
branch_data = df[df[branch_column] == selected_branch].copy()

# --- TABS FOR ORGANIZED VIEW ---
tab1, tab2, tab3 = st.tabs(["📋 Student Records", "📊 Analytics & Charts", "📈 Global Comparison"])

# === TAB 1: NEW DETAILS (The Table View) ===
with tab1:
    st.markdown(f"### 📋 Student Performance List: {selected_branch}")
    
    if not branch_data.empty:
        # Metrics summary on top of table
        c1, c2, c3, c4 = st.columns(4)
        avg_cgpa = branch_data['CGPA'].mean()
        max_cgpa = branch_data['CGPA'].max()
        min_cgpa = branch_data['CGPA'].min()
        
        c1.metric("Total Students", len(branch_data))
        c2.metric("Average CGPA", f"{avg_cgpa:.2f}")
        c3.metric("Highest CGPA", f"{max_cgpa:.2f}")
        c4.metric("Lowest CGPA", f"{min_cgpa:.2f}")
        
        st.markdown("---")

        # Prepare data for table
        table_data = []
        
        for idx, row in branch_data.iterrows():
            best, worst = get_student_best_worst_subject(row)
            table_data.append({
                'Roll Number': row.get('Roll_Number'),
                'Name': row.get('Name'),
                'CGPA': row.get('CGPA', 0),
                'SGPA': row.get('SGPA', 0),
                'Best Subject': best,
                'Lowest Subject': worst
            })
        
        student_df = pd.DataFrame(table_data)
        
        # Sort by CGPA desc
        student_df = student_df.sort_values('CGPA', ascending=False).reset_index(drop=True)
        student_df.index += 1  # Start rank at 1
        student_df.index.name = 'Rank'
        
        # Display table
        st.dataframe(
            student_df.style
            .background_gradient(subset=['CGPA'], cmap='RdYlGn', vmin=5, vmax=10)
            .format({'CGPA': '{:.2f}', 'SGPA': '{:.2f}'}),
            use_container_width=True,
            height=600  # Taller table
        )
        
        # Download Button
        csv = student_df.to_csv()
        st.download_button(
            "📥 Download Student List (CSV)",
            csv,
            f"{selected_branch}_students.csv",
            "text/csv",
            key='download-csv'
        )

# === TAB 2: ANALYTICS (The Charts & Stats) ===
with tab2:
    st.markdown(f"### 📊 Deep Dive: {selected_branch}")
    
    # Row 1: Distribution & Scatter
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("#### 🥧 CGPA Distribution")
        # Binning CGPA data
        bins = [0, 4, 5, 6, 7, 8, 9, 10]
        labels = ['Failed (<4)', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']
        branch_data['CGPA_Band'] = pd.cut(branch_data['CGPA'], bins=bins, labels=labels, right=True)
        
        dist_counts = branch_data['CGPA_Band'].value_counts().reset_index()
        dist_counts.columns = ['CGPA Range', 'Count']
        
        fig = px.pie(
            dist_counts, 
            values='Count', 
            names='CGPA Range',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Teal
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### 📉 Performance Curve (Rank vs CGPA)")
        # Sort data for rank
        scatter_data = branch_data.sort_values('CGPA', ascending=False).reset_index(drop=True)
        scatter_data['Rank'] = scatter_data.index + 1
        
        fig_scatter = px.scatter(
            scatter_data, 
            x='Rank', 
            y='CGPA',
            hover_data=['Name', 'Roll_Number'],
            color='CGPA',
            color_continuous_scale='Viridis',
            title="Student Performance Decay Curve"
        )
        fig_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # Row 2: Top Performers
    st.markdown("#### 🏆 Hall of Fame")
    top_3 = branch_data.nlargest(3, 'CGPA')
    
    t1, t2, t3 = st.columns(3)
    
    for i, (_, student) in enumerate(top_3.iterrows()):
        rank = i + 1
        with [t1, t2, t3][i]:
            color = "#FFD700" if rank == 1 else "#C0C0C0" if rank == 2 else "#CD7F32"
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #1e1e24, #25252b); border-top: 3px solid {color}; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 5px 5px 15px rgba(0,0,0,0.5);">
                <div style="font-size: 2em; margin-bottom: 10px;">{'🥇' if rank==1 else '🥈' if rank==2 else '🥉'}</div>
                <h3 style="margin:0; color: white; font-size: 1.1em;">{student.get('Name')}</h3>
                <p style="color: #bbb; font-size: 0.9em;">{student.get('Roll_Number')}</p>
                <h2 style="color: {color}; margin: 5px 0;">{student.get('CGPA'):.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

# === TAB 3: RESTORED COMPARISON (The Global View) ===
with tab3:
    st.markdown("### 📈 How does this branch compare?")
    
    # Calculate global branch stats
    branch_stats = df.groupby(branch_column).agg({
        'CGPA': 'mean',
        'Roll_Number': 'count'
    }).reset_index()
    branch_stats.columns = ['Branch', 'Avg_CGPA', 'Students']
    
    # Bar Chart
    fig_comp = px.bar(
        branch_stats, 
        x='Branch', 
        y='Avg_CGPA',
        color='Avg_CGPA',
        color_continuous_scale='Viridis',
        title="Average CGPA across all Branches"
    )
    # Highlight current branch
    colors = ['lightslategray'] * len(branch_stats)
    # Find index of current branch to highlight ? (Plotly handles via color scale, but we can update layout)
    
    st.plotly_chart(fig_comp, use_container_width=True)
    
    # Box Plot
    st.markdown("### 📦 Distribution Comparison")
    fig_box = px.box(df, x=branch_column, y="CGPA", title="CGPA Variability by Branch")
    st.plotly_chart(fig_box, use_container_width=True)

# Sidebar info
with st.sidebar:
    st.markdown("### 📊 Quick Stats")
    if not branch_stats.empty:
        best_branch = branch_stats.loc[branch_stats['Avg_CGPA'].idxmax()]
        st.success(f"**Top Branch:**\n{best_branch['Branch']}\nAvg: {best_branch['Avg_CGPA']:.2f}")


