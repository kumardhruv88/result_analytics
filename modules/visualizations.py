"""
Visualizations Module
Plotly-based interactive and 3D visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Optional

# Color schemes
GRADE_COLORS = {
    'O': '#10b981',   # Excellent - Green
    'A+': '#34d399',  # Very Good - Light Green
    'A': '#60a5fa',   # Good - Blue
    'B+': '#93c5fd',  # Above Average - Light Blue
    'B': '#fbbf24',   # Average - Yellow
    'C': '#fb923c',   # Below Average - Orange
    'P': '#f87171',   # Pass - Light Red
    'F': '#ef4444'    # Fail - Red
}

THEME = {
    'primary': '#1e3a8a',
    'secondary': '#3b82f6',
    'success': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b',
}

def create_3d_performance_scatter(df: pd.DataFrame) -> go.Figure:
    """
    Creates interactive 3D scatter plot of student performance
    X: CGPA, Y: Branch (encoded), Z: Total Credits
    """
    if df.empty or 'CGPA' not in df.columns:
        return go.Figure()
    
    # Encode branches numerically
    if 'Branch' in df.columns:
        branches = df['Branch'].unique()
        branch_mapping = {branch: i for i, branch in enumerate(branches)}
        df_plot = df.copy()
        df_plot['Branch_Code'] = df_plot['Branch'].map(branch_mapping)
    else:
        df_plot = df.copy()
        df_plot['Branch_Code'] = 0
        branches = ['All']
    
    # Color based on result status
    color_map = {'PASS': 1, 'FAIL': 0}
    colors = df_plot['Result_Status'].str.upper().map(color_map).fillna(0.5) if 'Result_Status' in df_plot.columns else [0.5] * len(df_plot)
    
    # Hover text
    hover_text = []
    for idx, row in df_plot.iterrows():
        text = f"<b>{row.get('Name', 'N/A')}</b><br>"
        text += f"Roll: {row.get('Roll_Number', 'N/A')}<br>"
        text += f"CGPA: {row.get('CGPA', 0):.2f}<br>"
        text += f"Branch: {row.get('Branch', 'N/A')}<br>"
        text += f"Status: {row.get('Result_Status', 'N/A')}"
        hover_text.append(text)
    
    fig = go.Figure(data=[go.Scatter3d(
        x=df_plot['CGPA'],
        y=df_plot['Branch_Code'],
        z=df_plot.get('Credits', [2] * len(df_plot)),  # Default to 2 if no credits column
        mode='markers',
        marker=dict(
            size=6,
            color=colors,
            colorscale='RdYlGn',
            showscale=True,
            opacity=0.8,
            line=dict(color='white', width=0.5),
            colorbar=dict(title="Status", tickvals=[0, 1], ticktext=['Fail', 'Pass'])
        ),
        text=hover_text,
        hoverinfo='text'
    )])
    
    fig.update_layout(
        title='3D Student Performance Visualization',
        scene=dict(
            xaxis_title='CGPA',
            yaxis=dict(
                title='Branch',
                ticktext=list(branches),
                tickvals=list(range(len(branches)))
            ),
            zaxis_title='Credits',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
        ),
        width=900,
        height=700,
        template='plotly_white',
        showlegend=False
    )
    
    return fig

def create_branch_comparison_chart(branch_stats: pd.DataFrame) -> go.Figure:
    """Create interactive bar chart for branch-wise CGPA comparison"""
    
    if branch_stats.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    # Add average CGPA bars
    fig.add_trace(go.Bar(
        x=branch_stats['Branch'],
        y=branch_stats['Avg_CGPA'],
        name='Average CGPA',
        marker_color=THEME['primary'],
        text=branch_stats['Avg_CGPA'].round(2),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Avg CGPA: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Branch-wise Average CGPA Comparison',
        xaxis_title='Branch',
        yaxis_title='Average CGPA',
        yaxis_range=[0, 10],
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    return fig

def create_grade_distribution_chart(df: pd.DataFrame, groupby: Optional[str] = None) -> go.Figure:
    """Create stacked bar chart for grade distribution"""
    
    if df.empty or 'Letter_Grade' not in df.columns:
        return go.Figure()
    
    if groupby and groupby in df.columns:
        # Crosstab for grouped distribution
        dist = pd.crosstab(df[groupby], df['Letter_Grade'])
        
        fig = go.Figure()
        
        # Add trace for each grade
        for grade in dist.columns:
            color = GRADE_COLORS.get(grade, '#gray')
            fig.add_trace(go.Bar(
                name=grade,
                x=dist.index,
                y=dist[grade],
                marker_color=color,
                hovertemplate='<b>%{x}</b><br>Grade ' + grade + ': %{y}<extra></extra>'
            ))
        
        fig.update_layout(
            title=f'Grade Distribution by {groupby}',
            xaxis_title=groupby,
            yaxis_title='Number of Students',
            barmode='stack',
            template='plotly_white',
            height=500
        )
    else:
        # Overall grade distribution
        dist = df['Letter_Grade'].value_counts().sort_index()
        colors = [GRADE_COLORS.get(grade, '#gray') for grade in dist.index]
        
        fig = go.Figure(data=[go.Bar(
            x=dist.index,
            y=dist.values,
            marker_color=colors,
            text=dist.values,
            textposition='outside',
            hovertemplate='<b>Grade %{x}</b><br>Count: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            title='Overall Grade Distribution',
            xaxis_title='Letter Grade',
            yaxis_title='Number of Students',
            template='plotly_white',
            height=500,
            showlegend=False
        )
    
    return fig

def create_cgpa_distribution_histogram(df: pd.DataFrame) -> go.Figure:
    """Create histogram for CGPA distribution"""
    
    if df.empty or 'CGPA' not in df.columns:
        return go.Figure()
    
    fig = px.histogram(
        df,
        x='CGPA',
        nbins=20,
        title='CGPA Distribution',
        labels={'CGPA': 'CGPA', 'count': 'Number of Students'},
        color_discrete_sequence=[THEME['secondary']]
    )
    
    fig.update_layout(
        template='plotly_white',
        height=500,
        xaxis_range=[0, 10],
        showlegend=False
    )
    
    # Add mean line
    mean_cgpa = df['CGPA'].mean()
    fig.add_vline(
        x=mean_cgpa,
        line_dash="dash",
        line_color=THEME['danger'],
        annotation_text=f"Mean: {mean_cgpa:.2f}",
        annotation_position="top"
    )
    
    return fig

def create_box_plot(df: pd.DataFrame, groupby: str = 'Branch') -> go.Figure:
    """Create box plot for CGPA distribution by group"""
    
    if df.empty or 'CGPA' not in df.columns or groupby not in df.columns:
        return go.Figure()
    
    fig = px.box(
        df,
        x=groupby,
        y='CGPA',
        title=f'CGPA Distribution by {groupby}',
        color=groupby,
        points='outliers'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=500,
        showlegend=False,
        yaxis_range=[0, 10]
    )
    
    return fig

def create_subject_difficulty_chart(subject_stats: pd.DataFrame) -> go.Figure:
    """Create horizontal bar chart for subject difficulty"""
    
    if subject_stats.empty:
        return go.Figure()
    
    # Sort by difficulty index
    subject_stats_sorted = subject_stats.sort_values('Difficulty_Index', ascending=True)
    
    # Color gradient based on difficulty
    colors = px.colors.sample_colorscale(
        'RdYlGn_r',
        subject_stats_sorted['Difficulty_Index'].values
    )
    
    fig = go.Figure(data=[go.Bar(
        y=subject_stats_sorted['Subject_Name'],
        x=subject_stats_sorted['Difficulty_Index'],
        orientation='h',
        marker_color=colors,
        text=subject_stats_sorted['Difficulty_Index'].round(3),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Difficulty Index: %{x:.3f}<br>Avg Marks: ' + 
                     subject_stats_sorted['Avg_Marks'].round(2).astype(str) + '<extra></extra>'
    )])
    
    fig.update_layout(
        title='Subject Difficulty Index (Higher = More Difficult)',
        xaxis_title='Difficulty Index',
        yaxis_title='Subject',
        template='plotly_white',
        height=max(400, len(subject_stats_sorted) * 30),
        showlegend=False
    )
    
    return fig

def create_pass_percentage_heatmap(df: pd.DataFrame) -> go.Figure:
    """Create heatmap of pass percentage: Subjects vs Branches"""
    
    if df.empty or 'Subject_Name' not in df.columns or 'Branch' not in df.columns:
        return go.Figure()
    
    # Calculate pass percentage
    pivot = df.pivot_table(
        values='Result_Status',
        index='Subject_Name',
        columns='Branch',
        aggfunc=lambda x: (x.str.upper() == 'PASS').sum() / len(x) * 100
    )
    
    fig = px.imshow(
        pivot,
        labels=dict(x="Branch", y="Subject", color="Pass %"),
        x=pivot.columns,
        y=pivot.index,
        color_continuous_scale='RdYlGn',
        aspect='auto',
        title='Pass Percentage Heatmap: Subjects vs Branches'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=max(400, len(pivot) * 30),
        xaxis_title='Branch',
        yaxis_title='Subject'
    )
    
    return fig

def create_topper_cards_data(df: pd.DataFrame, n: int = 3) -> list:
    """Prepare data for topper showcase cards"""
    
    if df.empty or 'CGPA' not in df.columns:
        return []
    
    toppers = df.nlargest(n, 'CGPA')
    
    cards = []
    for idx, row in toppers.iterrows():
        card = {
            'rank': idx + 1,
            'name': row.get('Name', 'N/A'),
            'roll': row.get('Roll_Number', 'N/A'),
            'cgpa': row.get('CGPA', 0),
            'sgpa': row.get('SGPA', 0),
            'branch': row.get('Branch', 'N/A'),
        }
        cards.append(card)
    
    return cards

def create_pie_chart(df: pd.DataFrame, column: str, title: str) -> go.Figure:
    """Create pie chart for categorical data"""
    
    if df.empty or column not in df.columns:
        return go.Figure()
    
    dist = df[column].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=dist.index,
        values=dist.values,
        hole=0.4,  # Donut chart
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=title,
        template='plotly_white',
        height=400
    )
    
    return fig
