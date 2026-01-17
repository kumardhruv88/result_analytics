"""
Additional Visualizations Module
Radar charts and other specialized visuals
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_radar_chart(student_subjects: pd.DataFrame, student_name: str = "Student") -> go.Figure:
    """
    Create radar chart for subject-wise grade points
    
    Args:
        student_subjects: DataFrame with subject-wise data for one student
        student_name: Name of the student for title
        
    Returns:
        Plotly figure object
    """
    if student_subjects.empty or 'Subject_Name' not in student_subjects.columns:
        return go.Figure()
    
    # Prepare data
    subjects = student_subjects['Subject_Name'].tolist()
    grade_points = student_subjects['Grade_Point'].tolist() if 'Grade_Point' in student_subjects.columns else [0] * len(subjects)
    
    # Close the radar chart by appending first value
    subjects_closed = subjects + [subjects[0]]
    grade_points_closed = grade_points + [grade_points[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=grade_points_closed,
        theta=subjects_closed,
        fill='toself',
        name=student_name,
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.4)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickmode='linear',
                tick0=0,
                dtick=2
            )
        ),
        title=f'Subject-wise Performance - {student_name}',
        showlegend=False,
        template='plotly_white',
        height=500
    )
    
    return fig


def create_performance_clustering(df: pd.DataFrame) -> go.Figure:
    """
    Create 3D scatter with K-Means clustering
    
    Args:
        df: Result dataframe with CGPA data
        
    Returns:
        Plotly figure with clustered data
    """
    if df.empty or 'CGPA' not in df.columns:
        return go.Figure()
    
    try:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        # Prepare features for clustering
        features = []
        feature_names = []
        
        if 'CGPA' in df.columns:
            features.append(df['CGPA'].fillna(0).values)
            feature_names.append('CGPA')
        
        if 'Total_Marks' in df.columns:
            features.append(df['Total_Marks'].fillna(0).values)
            feature_names.append('Total_Marks')
        else:
            features.append(df['CGPA'].fillna(0).values * 10)  # Approximate
            feature_names.append('Approx_Marks')
        
        if 'Backlogs' in df.columns:
            features.append(df['Backlogs'].fillna(0).values)
            feature_names.append('Backlogs')
        else:
            features.append(np.zeros(len(df)))
            feature_names.append('Backlogs')
        
        X = np.column_stack(features)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Apply K-Means clustering (3 clusters)
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Define cluster labels
        cluster_labels = ['High Performers', 'Average Performers', 'At-Risk Students']
        cluster_colors = ['#10b981', '#f59e0b', '#ef4444']  # Green, Orange, Red
        
        # Sort clusters by average CGPA
        cluster_avg_cgpa = []
        for i in range(3):
            mask = clusters == i
            if mask.any():
                cluster_avg_cgpa.append(df.loc[mask, 'CGPA'].mean())
            else:
                cluster_avg_cgpa.append(0)
        
        # Reorder clusters
        cluster_order = np.argsort(cluster_avg_cgpa)[::-1]  # Descending order
        cluster_mapping = {old: new for new, old in enumerate(cluster_order)}
        clusters = np.array([cluster_mapping[c] for c in clusters])
        
        # Create 3D scatter plot
        fig = go.Figure()
        
        for i in range(3):
            mask = clusters == i
            cluster_df = df[mask]
            
            fig.add_trace(go.Scatter3d(
                x=cluster_df['CGPA'] if 'CGPA' in cluster_df.columns else [0],
                y=cluster_df.get('Total_Marks', cluster_df.get('CGPA', 0) * 10),
                z=cluster_df.get('Backlogs', [0] * len(cluster_df)),
                mode='markers',
                name=cluster_labels[i],
                marker=dict(
                    size=6,
                    color=cluster_colors[i],
                    opacity=0.7,
                    line=dict(color='white', width=0.5)
                ),
                hovertemplate='<b>%{text}</b><br>CGPA: %{x:.2f}<br>Marks: %{y:.1f}<br>Backlogs: %{z}<extra></extra>',
                text=cluster_df.get('Name', ['Student'] * len(cluster_df))
            ))
        
        fig.update_layout(
            title='Student Performance Clustering (K-Means)',
            scene=dict(
                xaxis_title='CGPA',
                yaxis_title='Total Marks',
                zaxis_title='Backlogs',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
            ),
            height=700,
            template='plotly_white',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig
        
    except ImportError:
        # Scikit-learn not available, create simple visualization
        fig = go.Figure()
        
        # Simple manual clustering based on CGPA
        high = df[df['CGPA'] >= 8.0] if 'CGPA' in df.columns else pd.DataFrame()
        medium = df[(df['CGPA'] >= 6.0) & (df['CGPA'] < 8.0)] if 'CGPA' in df.columns else pd.DataFrame()
        low = df[df['CGPA'] < 6.0] if 'CGPA' in df.columns else pd.DataFrame()
        
        for cluster_df, name, color in [
            (high, 'High Performers (CGPA ≥ 8.0)', '#10b981'),
            (medium, 'Average Performers (6.0 ≤ CGPA < 8.0)', '#f59e0b'),
            (low, 'At-Risk Students (CGPA < 6.0)', '#ef4444')
        ]:
            if not cluster_df.empty:
                fig.add_trace(go.Scatter3d(
                    x=cluster_df['CGPA'],
                    y=cluster_df.get('Total_Marks', cluster_df['CGPA'] * 10),
                    z=cluster_df.get('Backlogs', [0] * len(cluster_df)),
                    mode='markers',
                    name=name,
                    marker=dict(size=6, color=color, opacity=0.7)
                ))
        
        fig.update_layout(
            title='Student Performance Clustering',
            scene=dict(xaxis_title='CGPA', yaxis_title='Marks', zaxis_title='Backlogs'),
            height=700,
            template='plotly_white'
        )
        
        return fig
