"""
Reports & Export Page
Generate and download custom reports
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from modules.data_loader import load_result_data, filter_data, get_unique_values
from modules.analytics import (
    calculate_overall_statistics,
    get_branch_wise_statistics,
    calculate_subject_statistics,
    get_top_performers
)

st.set_page_config(page_title="Reports & Export", page_icon="📥", layout="wide")

st.title("📥 Reports & Export")
st.markdown("### Generate Custom Reports and Export Data")
st.markdown("---")

# Load data
df = load_result_data()

if df.empty:
    st.error("⚠️ No data available.")
    st.stop()

# Report types
tab1, tab2, tab3 = st.tabs([
    "📊 Quick Exports",
    "📋 Custom Report Builder",
    "📈 Analytics Summary"
])

with tab1:
    st.markdown("### 📊 Quick Export Options")
    
    st.info("Download pre-configured reports with a single click!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📁 Complete Dataset")
        st.write("Download the entire result dataset")
        
        csv_complete = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Complete Data (CSV)",
            data=csv_complete,
            file_name=f"complete_results_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Excel format
        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Results', index=False)
        
        st.download_button(
            label="📥 Download Complete Data (Excel)",
            data=buffer.getvalue(),
            file_name=f"complete_results_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        st.markdown("#### 📊 Statistics Summary")
        st.write("Download comprehensive statistics")
        
        # Generate statistics
        stats = calculate_overall_statistics(df)
        branch_stats = get_branch_wise_statistics(df)
        
        if not branch_stats.empty:
            csv_stats = branch_stats.to_csv(index=False)
            st.download_button(
                label="📥 Download Branch Statistics (CSV)",
                data=csv_stats,
                file_name=f"branch_statistics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Subject statistics
        if 'Subject_Name' in df.columns:
            subject_stats = calculate_subject_statistics(df)
            if not subject_stats.empty:
                csv_subject = subject_stats.to_csv(index=False)
                st.download_button(
                    label="📥 Download Subject Statistics (CSV)",
                    data=csv_subject,
                    file_name=f"subject_statistics_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    st.markdown("---")
    
    # Toppers list
    st.markdown("#### 🏆 Toppers Report")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        top_n = st.number_input("Number of toppers", min_value=5, max_value=100, value=10, step=5)
    
    toppers = get_top_performers(df, n=top_n, by='overall')
    
    if not toppers.empty:
        st.dataframe(toppers, use_container_width=True, hide_index=True)
        
        csv_toppers = toppers.to_csv(index=False)
        st.download_button(
            label=f"📥 Download Top {top_n} Students (CSV)",
            data=csv_toppers,
            file_name=f"top_{top_n}_students_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with tab2:
    st.markdown("### 📋 Custom Report Builder")
    
    st.info("Build your own custom report by selecting filters and columns")
    
    # Filters section
    st.markdown("#### 🔍 Apply Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        branches = get_unique_values(df, 'Branch') if 'Branch' in df.columns else []
        selected_branches = st.multiselect(
            "Select Branches",
            options=branches,
            default=[]
        )
    
    with col2:
        sections = get_unique_values(df, 'Section') if 'Section' in df.columns else []
        selected_sections = st.multiselect(
            "Select Sections",
            options=sections,
            default=[]
        )
    
    with col3:
        min_cgpa = st.number_input("Min CGPA", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
    
    with col4:
        max_cgpa = st.number_input("Max CGPA", min_value=0.0, max_value=10.0, value=10.0, step=0.1)
    
    # Result status filter
    result_filter = st.selectbox(
        "Result Status",
        options=['All', 'Pass', 'Fail']
    )
    
    # Column selection
    st.markdown("#### 📊 Select Columns to Include")
    
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect(
        "Columns",
        options=all_columns,
        default=all_columns[:min(8, len(all_columns))]
    )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_branches:
        filtered_df = filtered_df[filtered_df['Branch'].isin(selected_branches)]
    
    if selected_sections:
        filtered_df = filtered_df[filtered_df['Section'].isin(selected_sections)]
    
    if 'CGPA' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['CGPA'] >= min_cgpa) & (filtered_df['CGPA'] <= max_cgpa)]
    
    if result_filter != 'All' and 'Result_Status' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Result_Status'].str.upper() == result_filter.upper()]
    
    # Select columns
    if selected_columns:
        available_cols = [col for col in selected_columns if col in filtered_df.columns]
        filtered_df = filtered_df[available_cols]
    
    # Preview
    st.markdown("#### 👁️ Preview")
    st.info(f"Filtered dataset contains **{len(filtered_df)}** records")
    st.dataframe(filtered_df.head(20), use_container_width=True)
    
    # Export options
    st.markdown("#### 📥 Export Filtered Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_filtered = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv_filtered,
            file_name=f"custom_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Excel with multiple sheets
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, sheet_name='Filtered Data', index=False)
            
            # Add statistics sheet
            if len(filtered_df) > 0:
                stats_df = pd.DataFrame({
                    'Metric': ['Total Records', 'Average CGPA', 'Median CGPA', 'Max CGPA', 'Min CGPA'],
                    'Value': [
                        len(filtered_df),
                        filtered_df['CGPA'].mean() if 'CGPA' in filtered_df.columns else 'N/A',
                        filtered_df['CGPA'].median() if 'CGPA' in filtered_df.columns else 'N/A',
                        filtered_df['CGPA'].max() if 'CGPA' in filtered_df.columns else 'N/A',
                        filtered_df['CGPA'].min() if 'CGPA' in filtered_df.columns else 'N/A',
                    ]
                })
                stats_df.to_excel(writer, sheet_name='Statistics', index=False)
        
        st.download_button(
            label="📥 Download as Excel",
            data=buffer.getvalue(),
            file_name=f"custom_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col3:
        # JSON format
        json_filtered = filtered_df.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_filtered,
            file_name=f"custom_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

with tab3:
    st.markdown("### 📈 Analytics Summary Report")
    
    st.info("Comprehensive statistical summary for administrative use")
    
    # Generate full report
    stats = calculate_overall_statistics(df)
    branch_stats = get_branch_wise_statistics(df)
    
    # Create summary report
    st.markdown("#### 📊 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", stats['total_students'])
    
    with col2:
        st.metric("Pass Percentage", f"{stats['pass_percentage']:.1f}%")
    
    with col3:
        st.metric("Average CGPA", f"{stats['avg_cgpa']:.2f}")
    
    with col4:
        st.metric("Total Backlogs", int(stats['total_backlogs']))
    
    # Branch wise summary
    if not branch_stats.empty:
        st.markdown("#### 🏆 Branch-wise Performance")
        st.dataframe(branch_stats, use_container_width=True)
    
    # Generate comprehensive report
    st.markdown("#### 📥 Download Complete Analytics Report")
    
    # Create Excel with multiple sheets
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Sheet 1: Executive Summary
        exec_summary = pd.DataFrame({
            'Metric': [
                'Total Students',
                'Students Passed',
                'Students Failed',
                'Pass Percentage',
                'Average CGPA',
                'Median CGPA',
                'Highest CGPA',
                'Lowest CGPA',
                'Standard Deviation',
                'Total Backlogs'
            ],
            'Value': [
                stats['total_students'],
                stats['pass_count'],
                stats['fail_count'],
                f"{stats['pass_percentage']:.2f}%",
                f"{stats['avg_cgpa']:.2f}",
                f"{stats['median_cgpa']:.2f}",
                f"{stats['max_cgpa']:.2f}",
                f"{stats['min_cgpa']:.2f}",
                f"{stats['std_cgpa']:.2f}",
                int(stats['total_backlogs'])
            ]
        })
        exec_summary.to_excel(writer, sheet_name='Executive Summary', index=False)
        
        # Sheet 2: Branch Statistics
        if not branch_stats.empty:
            branch_stats.to_excel(writer, sheet_name='Branch Statistics', index=False)
        
        # Sheet 3: Subject Statistics (if available)
        if 'Subject_Name' in df.columns:
            subject_stats = calculate_subject_statistics(df)
            if not subject_stats.empty:
                subject_stats.to_excel(writer, sheet_name='Subject Statistics', index=False)
        
        # Sheet 4: Top 20 Students
        toppers = get_top_performers(df, n=20, by='overall')
        if not toppers.empty:
            toppers.to_excel(writer, sheet_name='Top 20 Students', index=False)
        
        # Sheet 5: Raw Data (sampled if too large)
        sample_size = min(1000, len(df))
        df.head(sample_size).to_excel(writer, sheet_name='Raw Data Sample', index=False)
    
    st.download_button(
        label="📥 Download Complete Analytics Report (Excel)",
        data=buffer.getvalue(),
        file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    
    st.success("✅ Report includes: Executive Summary, Branch Stats, Subject Stats, Top Students, and Raw Data Sample")

# Sidebar
with st.sidebar:
    st.markdown("### 📥 Export Formats")
    
    st.markdown("""
    **Available Formats:**
    - **CSV**: Simple spreadsheet format
    - **Excel**: Multi-sheet workbooks
    - **JSON**: Structured data format
    
    **Use Cases:**
    - **CSV**: Quick analysis in Excel/Google Sheets
    - **Excel**: Professional reports with multiple tabs
    - **JSON**: Integration with other systems
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips")
    st.info("""
    - Use filters to create targeted reports
    - Excel format includes multiple sheets
    - Custom reports can be shared with stakeholders
    """)
