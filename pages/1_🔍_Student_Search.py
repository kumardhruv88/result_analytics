"""
Student Search Page
Find and view individual student results
"""

import streamlit as st
import pandas as pd
from modules.data_loader import load_result_data, search_student
from modules.analytics import calculate_student_rank

st.set_page_config(page_title="Student Search", page_icon="🔍", layout="wide")

# Custom CSS
st.markdown("""
<style>
.student-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 15px;
    color: white;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    margin: 20px 0;
}

.rank-badge {
    background: #ffd700;
    color: #1e3a8a;
    padding: 10px 20px;
    border-radius: 25px;
    font-weight: bold;
    font-size: 1.2em;
    display: inline-block;
    margin: 10px 0;
}

.result-pass {
    background: #10b981;
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: bold;
}

.result-fail {
    background: #ef4444;
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🔍 Student Search")
st.markdown("### Find Individual Student Results")
st.markdown("---")

# Load data
df = load_result_data()

if df.empty:
    st.error("⚠️ No data available. Please check the data file.")
    st.stop()

# Search interface
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    search_term = st.text_input(
        "🔍 Search by Roll Number or Name",
        placeholder="Enter roll number or student name...",
        help="Type the roll number or name to search"
    )

with col2:
    branch_filter = st.selectbox(
        "Branch",
        options=['All'] + sorted(df['Branch'].unique().tolist()) if 'Branch' in df.columns else ['All']
    )

with col3:
    section_filter = st.selectbox(
        "Section",
        options=['All'] + sorted(df['Section'].unique().tolist()) if 'Section' in df.columns else ['All']
    )

# Apply filters
filtered_df = df.copy()
if branch_filter != 'All' and 'Branch' in df.columns:
    filtered_df = filtered_df[filtered_df['Branch'] == branch_filter]
if section_filter != 'All' and 'Section' in df.columns:
    filtered_df = filtered_df[filtered_df['Section'] == section_filter]

# Search logic
if search_term:
    results = search_student(filtered_df, search_term)
    
    if results.empty:
        st.warning(f"No results found for '{search_term}'")
    else:
        st.success(f"Found {len(results)} matching student(s)")
        
        # Display each student's result
        for idx, student in results.iterrows():
            with st.container():
                # Student Card Header
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="student-card">
                        <h2>🎓 {student.get('Name', 'N/A')}</h2>
                        <p style="font-size: 1.1em;">
                            <b>Roll Number:</b> {student.get('Roll_Number', 'N/A')}<br>
                            <b>Branch:</b> {student.get('Branch', 'N/A')} | 
                            <b>Section:</b> {student.get('Section', 'N/A')} |
                            <b>Semester:</b> {student.get('Semester', 5)}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Result status badge
                    status = student.get('Result_Status', 'Unknown').upper()
                    if status == 'PASS':
                        st.markdown('<div class="result-pass">✅ PASSED</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="result-fail">❌ FAILED</div>', unsafe_allow_html=True)
                
                # Performance Metrics
                st.markdown("### 📊 Performance Metrics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("SGPA", f"{student.get('SGPA', 0):.2f}")
                
                with col2:
                    st.metric("CGPA", f"{student.get('CGPA', 0):.2f}")
                
                with col3:
                    st.metric("Backlogs", int(student.get('Backlogs', 0)))
                
                with col4:
                    st.metric("Credits", int(student.get('Credits', 0)))
                
                student_data = student # student is already a Series from iterrows()
                
                # --- PROFESSIONAL PROFILE HEADER ---
                st.markdown("### 👤 Student Profile")
                
                # Create a card-like layout using columns with borders
                p1, p2, p3 = st.columns([1, 2, 1])
                
                with p1:
                    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
                
                with p2:
                    st.subheader(student_data['Name'])
                    st.caption(f"**Roll Number:** {student_data['Roll_Number']}")
                    
                    # Branch display
                    branch_col = 'Branch_Specialization' if 'Branch_Specialization' in df.columns else 'Branch'
                    st.caption(f"**Department:** {student_data.get(branch_col, 'Unknown')}")

                with p3:
                     # Key Stat Box
                    st.metric("Cumulative GPA", f"{student_data.get('CGPA', 0):.2f}", delta="SGPA: " + str(student_data.get('SGPA', 0)))

                st.markdown("---")

                # --- ACADEMIC TRANSCRIPT ---
                st.subheader("📚 Academic Transcript & Analytics")

                subject_data = [] # Re-implementing extraction logic cleanly
                for i in range(1, 8):
                    code = student_data.get(f'Subject_{i}_Code')
                    if pd.notna(code):
                        subject_data.append({
                            'Subject Code': code,
                            'Grade': student_data.get(f'Subject_{i}_Grade'),
                            'Credits': student_data.get(f'Subject_{i}_Credits'),
                            'Grade Point': student_data.get(f'Subject_{i}_GradePoint'),
                            'Credit Points': student_data.get(f'Subject_{i}_CreditPoints')
                        })
                
                if subject_data:
                    sub_df = pd.DataFrame(subject_data)
                    
                    # Compare Logic (Recalculated)
                    branch_col = 'Branch_Specialization' if 'Branch_Specialization' in df.columns else 'Branch'
                    branch_val = student_data.get(branch_col)
                    peers = df[df[branch_col] == branch_val]
                    
                    avgs = []
                    maxs = []
                    
                    for c in sub_df['Subject Code']:
                        # simplistic lookup across all subject cols for peers
                        peer_vals = []
                        for k in range(1, 8):
                            mask = peers[f'Subject_{k}_Code'] == c
                            if mask.any():
                                peer_vals.extend(pd.to_numeric(peers.loc[mask, f'Subject_{k}_GradePoint'], errors='coerce').dropna().tolist())
                        
                        if peer_vals:
                            avgs.append(sum(peer_vals)/len(peer_vals))
                            maxs.append(max(peer_vals))
                        else:
                            avgs.append(0)
                            maxs.append(0)
                    
                    sub_df['Class Avg'] = avgs
                    sub_df['Top Score'] = maxs

                    # Layout: Charts vs Table
                    c_viz, c_table = st.columns([1, 1])

                    with c_viz:
                        st.markdown("#### 📈 Performance Radar")
                        # Radar Chart for Subjects
                        import plotly.express as px
                        categories = sub_df['Subject Code'].tolist()
                        values = pd.to_numeric(sub_df['Grade Point'], errors='coerce').fillna(0).tolist()
                        class_avg = sub_df['Class Avg'].tolist()
                        
                        fig_radar = px.line_polar(r=values, theta=categories, line_close=True, title="You vs Class Avg")
                        fig_radar.add_scatterpolar(r=class_avg, theta=categories, fill='toself', name='Class Avg', line_color='gray', opacity=0.4)
                        fig_radar.add_scatterpolar(r=values, theta=categories, fill='toself', name='Student', line_color='#6C5CE7')
                        
                        st.plotly_chart(fig_radar, use_container_width=True)

                    with c_table:
                         st.markdown("#### 📋 Detailed Grades")
                         styled = sub_df.style.background_gradient(subset=['Grade Point'], cmap='Purples').format("{:.1f}", subset=['Class Avg', 'Grade Point'])
                         st.dataframe(styled, use_container_width=True, hide_index=True)

                    # Distribution of grades for this student
                    try:
                        import plotly.express as px
                        grade_counts = sub_df['Grade'].value_counts()
                        fig = px.pie(
                            values=grade_counts.values,
                            names=grade_counts.index,
                            title=f"Grade Distribution for {student.get('Name', 'Student')}",
                            hole=0.4,
                            color_discrete_sequence=px.colors.qualitative.Pastel
                        )
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        fig.update_layout(showlegend=False, margin=dict(t=30, b=0, l=0, r=0), height=250)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.info("Chart unavailable")
                else:
                    st.info("No detailed subject data available for this student.")
                
                # Ranking information
                rank_info = calculate_student_rank(df, student.get('Roll_Number', ''))
                
                if rank_info:
                    st.markdown("### 🏆 Rankings")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.info(f"**Overall Rank**: {rank_info['overall_rank']} / {rank_info['total_students']}")
                    
                    with col2:
                        st.info(f"**Branch Rank**: {rank_info['branch_rank']} / {rank_info['branch_total']}")
                    
                    with col3:
                        st.info(f"**Percentile**: {rank_info['percentile']:.1f}%")
                
                # Rankings already displayed above

                
                # Export button
                st.markdown("---")
                if st.button(f"📥 Download {student.get('Name', 'Student')}'s Report", key=f"download_{idx}"):
                    # Create downloadable dataframe
                    student_data = student.to_frame().T
                    csv = student_data.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"result_{student.get('Roll_Number', 'student')}.csv",
                        mime="text/csv"
                    )
                
                st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
else:
    # No search term - show instructions
    st.info("""
    ### 📝 How to Search:
    
    1. **By Roll Number**: Enter the full or partial roll number (e.g., 2021BTCS001)
    2. **By Name**: Enter the student's name (partial names work too)
    3. **Use Filters**: Select specific branch or section to narrow down results
    
    **Tip**: The search is case-insensitive and supports partial matches!
    """)
    
    # Show sample data
    st.markdown("### 📊 Sample Students")
    sample_size = min(10, len(df))
    sample_df = df.head(sample_size)[['Roll_Number', 'Name', 'Branch', 'CGPA', 'SGPA', 'Result_Status']]
    st.dataframe(sample_df, use_container_width=True)

# Statistics sidebar
with st.sidebar:
    st.markdown("### 📊 Search Statistics")
    st.metric("Total Students", len(df['Roll_Number'].unique()) if 'Roll_Number' in df.columns else len(df))
    
    if 'Branch' in df.columns:
        st.metric("Branches", df['Branch'].nunique())
    
    if 'Section' in df.columns:
        st.metric("Sections", df['Section'].nunique())
    
    st.markdown("---")
    st.caption("💡 Tip: Use Ctrl+F to quickly search on this page!")
