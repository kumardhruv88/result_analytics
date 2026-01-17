"""
Advanced Analytics Page
3D visualizations and advanced statistical analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules.data_loader import load_result_data
from modules.analytics import calculate_overall_statistics, get_cgpa_distribution
from modules.visualizations import create_3d_performance_scatter

st.set_page_config(page_title="Advanced Analytics", page_icon="📈", layout="wide")

st.title("📈 Advanced Analytics")
st.markdown("### Interactive 3D Visualizations & Statistical Insights")
st.markdown("---")

# Load data
df = load_result_data()

if df.empty:
    st.error("⚠️ No data available.")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🎨 3D Visualizations",
    "📊 Statistical Analysis",
    "🔍 Correlation Analysis",
    "🎯 Performance Clustering"
])

with tab1:
    st.markdown("### 🎨 Interactive 3D Performance Visualization")
    
    st.info("💡 **Interactive Controls:** Use your mouse to rotate, zoom, and pan. Hover over points for details!")
    
    # 3D Scatter Plot
    fig_3d = create_3d_performance_scatter(df)
    st.plotly_chart(fig_3d, use_container_width=True)
    
    with st.expander("📖 How to interpret this visualization"):
        st.markdown("""
        **Axes:**
        - **X-axis (CGPA)**: Student's CGPA (0-10 scale)
        - **Y-axis (Branches)**: Different engineering branches (numerically encoded)
        - **Z-axis (Credits)**: Total credits earned
        
        **Colors:**
        - **Green**: Students who passed
        - **Red**: Students who failed
        - **Yellow/Orange**: Intermediate status
        
        **Insights you can gather:**
        1. **Clusters**: Groups of similar-performing students
        2. **Outliers**: Exceptionally high or low performers
        3. **Branch patterns**: Which branches have better concentration of high CGPAs
        4. **Pass/Fail distribution**: Visual representation of success rates
        """)
    
    st.markdown("---")
    
    # 3D Bar Chart - Branch vs Grade
    if 'Branch' in df.columns and 'Letter_Grade' in df.columns:
        st.markdown("### 📊 3D Grade Distribution Across Branches")
        
        # Create pivot for 3D visualization
        grade_pivot = pd.crosstab(df['Branch'], df['Letter_Grade'])
        
        # Create 3D bar chart
        branches = grade_pivot.index.tolist()
        grades = grade_pivot.columns.tolist()
        
        fig_3d_bar = go.Figure()
        
        for i, branch in enumerate(branches):
            for j, grade in enumerate(grades):
                count = grade_pivot.loc[branch, grade]
                
                fig_3d_bar.add_trace(go.Mesh3d(
                    x=[i-0.4, i+0.4, i+0.4, i-0.4, i-0.4, i+0.4, i+0.4, i-0.4],
                    y=[j-0.4, j-0.4, j+0.4, j+0.4, j-0.4, j-0.4, j+0.4, j+0.4],
                    z=[0, 0, 0, 0, count, count, count, count],
                    alphahull=0,
                    opacity=0.8,
                    color='rgb' + str(tuple(int(255*x) for x in __import__('colorsys').hsv_to_rgb((j/len(grades)), 0.8, 0.9))),
                    hovertemplate=f'<b>Branch: {branch}</b><br>Grade: {grade}<br>Count: {count}<extra></extra>',
                    showlegend=False
                ))
        
        fig_3d_bar.update_layout(
            title='3D View: Grades Across Branches',
            scene=dict(
                xaxis=dict(title='Branch', ticktext=branches, tickvals=list(range(len(branches)))),
                yaxis=dict(title='Grade', ticktext=grades, tickvals=list(range(len(grades)))),
                zaxis=dict(title='Number of Students'),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
            ),
            height=700,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_3d_bar, use_container_width=True)

with tab2:
    st.markdown("### 📊 Statistical Deep Dive")
    
    stats = calculate_overall_statistics(df)
    
    # Detailed statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Central Tendency")
        
        stats_df = pd.DataFrame({
            'Metric': ['Mean CGPA', 'Median CGPA', 'Mode CGPA', 'Range'],
            'Value': [
                f"{stats['avg_cgpa']:.3f}",
                f"{stats['median_cgpa']:.3f}",
                f"{df['CGPA'].mode()[0]:.3f}" if 'CGPA' in df.columns and len(df['CGPA'].mode()) > 0 else 'N/A',
                f"{stats['max_cgpa'] - stats['min_cgpa']:.3f}"
            ]
        })
        
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 📊 Dispersion")
        
        if 'CGPA' in df.columns:
            from scipy import stats as scipy_stats
            
            q1 = df['CGPA'].quantile(0.25)
            q3 = df['CGPA'].quantile(0.75)
            iqr = q3 - q1
            
            dispersion_df = pd.DataFrame({
                'Metric': ['Standard Deviation', 'Variance', 'IQR', 'Coefficient of Variation'],
                'Value': [
                    f"{stats['std_cgpa']:.3f}",
                    f"{stats['std_cgpa']**2:.3f}",
                    f"{iqr:.3f}",
                    f"{(stats['std_cgpa']/stats['avg_cgpa']*100):.2f}%"
                ]
            })
            
            st.dataframe(dispersion_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Percentile Analysis
    st.markdown("#### 📊 Percentile Distribution")
    
    if 'CGPA' in df.columns:
        percentiles = [10, 25, 50, 75, 90, 95, 99]
        percentile_values = [df['CGPA'].quantile(p/100) for p in percentiles]
        
        import plotly.express as px
        
        percentile_df = pd.DataFrame({
            'Percentile': [f"{p}th" for p in percentiles],
            'CGPA': percentile_values
        })
        
        fig_percentiles = px.bar(
            percentile_df,
            x='Percentile',
            y='CGPA',
            title='CGPA at Different Percentiles',
            text='CGPA',
            color='CGPA',
            color_continuous_scale='Viridis'
        )
        
        fig_percentiles.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_percentiles.update_layout(
            template='plotly_white',
            height=400,
            yaxis_range=[0, 10],
            showlegend=False
        )
        
        st.plotly_chart(fig_percentiles, use_container_width=True)
        
        st.info("""
        **Percentile Interpretation:**
        - **50th percentile (median)**: Half the students scored below this CGPA
        - **90th percentile**: Only 10% of students scored higher than this
        - **10th percentile**: 10% of students scored below this (at-risk students)
        """)
    
    st.markdown("---")
    
    # Normality test
    st.markdown("#### 📊 Distribution Analysis")
    
    if 'CGPA' in df.columns:
        from scipy.stats import normaltest, skew, kurtosis
        
        cgpa_data = df['CGPA'].dropna()
        
        # Skewness and Kurtosis
        skewness = skew(cgpa_data)
        kurt = kurtosis(cgpa_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Skewness", f"{skewness:.3f}")
            if abs(skewness) < 0.5:
                st.success("Nearly symmetric")
            elif skewness < 0:
                st.info("Left-skewed (more high performers)")
            else:
                st.warning("Right-skewed (more low performers)")
        
        with col2:
            st.metric("Kurtosis", f"{kurt:.3f}")
            if abs(kurt) < 0.5:
                st.success("Normal distribution")
            elif kurt > 0:
                st.info("Heavy-tailed (more outliers)")
            else:
                st.warning("Light-tailed (fewer outliers)")
        
        with col3:
            # Normality test
            stat, p_value = normaltest(cgpa_data)
            st.metric("Normality p-value", f"{p_value:.4f}")
            if p_value > 0.05:
                st.success("Likely normal distribution")
            else:
                st.warning("Not normal distribution")

with tab3:
    st.markdown("### 🔍 Correlation Analysis")
    
    # Check available numerical columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if len(numeric_cols) >= 2:
        st.markdown("#### 📊 Correlation Matrix")
        
        # Select columns for correlation
        corr_cols = st.multiselect(
            "Select columns to analyze correlations",
            options=numeric_cols,
            default=numeric_cols[:min(5, len(numeric_cols))]
        )
        
        if len(corr_cols) >= 2:
            # Calculate correlation
            corr_matrix = df[corr_cols].corr()
            
            # Create heatmap
            import plotly.express as px
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto='.2f',
                aspect='auto',
                color_continuous_scale='RdBu_r',
                zmin=-1,
                zmax=1,
                title='Correlation Heatmap'
            )
            
            fig_corr.update_layout(
                template='plotly_white',
                height=max(400, len(corr_cols) * 60)
            )
            
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Interpretation
            st.info("""
            **Correlation Interpretation:**
            - **+1.0**: Perfect positive correlation
            - **0.0**: No correlation
            - **-1.0**: Perfect negative correlation
            
            **Colors:**
            - **Red**: Negative correlation
            - **Blue**: Positive correlation
            - **White**: No correlation
            """)
            
            # Find strong correlations
            st.markdown("#### 🔍 Strong Correlations Found")
            
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.5:
                        strong_corr.append({
                            'Variable 1': corr_matrix.columns[i],
                            'Variable 2': corr_matrix.columns[j],
                            'Correlation': corr_val,
                            'Strength': 'Strong Positive' if corr_val > 0.7 else 'Moderate Positive' if corr_val > 0.5 else 'Strong Negative' if corr_val < -0.7 else 'Moderate Negative'
                        })
            
            if strong_corr:
                strong_corr_df = pd.DataFrame(strong_corr)
                strong_corr_df = strong_corr_df.sort_values('Correlation', key=abs, ascending=False)
                st.dataframe(strong_corr_df, use_container_width=True, hide_index=True)
            else:
                st.info("No strong correlations (>0.5) found between selected variables.")
    else:
        st.warning("Not enough numerical columns for correlation analysis.")

# Sidebar
with st.sidebar:
    st.markdown("### 🎨 Visualization Tips")
    
    st.markdown("""
    **3D Charts:**
    - Click and drag to rotate
    - Scroll to zoom
    - Hover for details
    
    **Best Practices:**
    - Look for clusters
    - Identify outliers
    - Compare distributions
    """)
    
    st.markdown("---")
    
    if not df.empty:
        st.markdown("### 📊 Quick Stats")
        stats = calculate_overall_statistics(df)
        st.metric("Total Records", len(df))
        st.metric("Average CGPA", f"{stats['avg_cgpa']:.2f}")
        st.metric("Std Deviation", f"{stats['std_cgpa']:.2f}")

with tab4:
    st.markdown("### 🎯 Performance Clustering Analysis")
    
    st.info("""
    **K-Means Clustering** groups students into 3 categories based on their performance metrics:
    - 🟢 **High Performers**: Consistently strong academic performance
    - 🟠 **Average Performers**: Moderate performance with room for improvement  
    - 🔴 **At-Risk Students**: May need additional academic support
    """)
    
    try:
        from modules.additional_viz import create_performance_clustering
        
        fig_clustering = create_performance_clustering(df)
        st.plotly_chart(fig_clustering, use_container_width=True)
        
        # Cluster statistics
        st.markdown("#### 📊 Cluster Statistics")
        
        # Manual clustering based on CGPA for statistics
        if 'CGPA' in df.columns:
            high = df[df['CGPA'] >= 8.0]
            medium = df[(df['CGPA'] >= 6.0) & (df['CGPA'] < 8.0)]
            low = df[df['CGPA'] < 6.0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.success(f"**🟢 High Performers**")
                st.metric("Count", len(high))
                st.metric("Avg CGPA", f"{high['CGPA'].mean():.2f}" if len(high) > 0 else "N/A")
                st.metric("Percentage", f"{len(high)/len(df)*100:.1f}%")
            
            with col2:
                st.warning(f"**🟠 Average Performers**")
                st.metric("Count", len(medium))
                st.metric("Avg CGPA", f"{medium['CGPA'].mean():.2f}" if len(medium) > 0 else "N/A")
                st.metric("Percentage", f"{len(medium)/len(df)*100:.1f}%")
            
            with col3:
                st.error(f"**🔴 At-Risk Students**")
                st.metric("Count", len(low))
                st.metric("Avg CGPA", f"{low['CGPA'].mean():.2f}" if len(low) > 0 else "N/A")
                st.metric("Percentage", f"{len(low)/len(df)*100:.1f}%")
            
            # Recommendations
            st.markdown("---")
            st.markdown("#### 💡 Recommendations")
            
            if len(low) > 0:
                st.warning(f"""
                **For At-Risk Students ({len(low)} students):**
                - Consider implementing mentorship programs
                - Provide additional tutoring sessions
                - Monitor attendance and engagement closely
                """)
            
            if len(high) > 0:
                st.success(f"""
                **For High Performers ({len(high)} students):**
                - Offer advanced placement opportunities
                - Encourage participation in research projects
                - Provide leadership development opportunities
                """)
    
    except Exception as e:
        st.error(f"Clustering visualization unavailable: {str(e)}")
        st.info("Install scikit-learn for advanced clustering: `pip install scikit-learn`")
