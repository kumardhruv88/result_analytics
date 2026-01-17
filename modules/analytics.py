"""
Analytics Module
Core analytics functions for result analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def calculate_overall_statistics(df: pd.DataFrame) -> Dict:
    """Calculate dashboard-wide statistics"""
    
    if df.empty:
        return {}
    
    stats = {
        'total_students': len(df['Roll_Number'].unique()) if 'Roll_Number' in df.columns else len(df),
        'total_records': len(df),
        'avg_cgpa': df['CGPA'].mean() if 'CGPA' in df.columns else 0,
        'median_cgpa': df['CGPA'].median() if 'CGPA' in df.columns else 0,
        'std_cgpa': df['CGPA'].std() if 'CGPA' in df.columns else 0,
        'max_cgpa': df['CGPA'].max() if 'CGPA' in df.columns else 0,
        'min_cgpa': df['CGPA'].min() if 'CGPA' in df.columns else 0,
    }
    
    # Calculate pass/fail statistics
    if 'Result_Status' in df.columns:
        pass_count = len(df[df['Result_Status'].str.upper() == 'PASS'])
        fail_count = len(df[df['Result_Status'].str.upper() == 'FAIL'])
        stats['pass_count'] = pass_count
        stats['fail_count'] = fail_count
        stats['pass_percentage'] = (pass_count / len(df) * 100) if len(df) > 0 else 0
    else:
        stats['pass_count'] = 0
        stats['fail_count'] = 0
        stats['pass_percentage'] = 0
    
    # Calculate backlog statistics
    if 'Backlogs' in df.columns:
        stats['total_backlogs'] = df['Backlogs'].sum()
        stats['students_with_backlogs'] = len(df[df['Backlogs'] > 0])
    else:
        stats['total_backlogs'] = 0
        stats['students_with_backlogs'] = 0
    
    return stats

def get_branch_wise_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate statistics for each branch"""
    
    if df.empty or 'Branch' not in df.columns:
        return pd.DataFrame()
    
    # Group by branch and calculate aggregates
    branch_stats = df.groupby('Branch').agg({
        'Roll_Number': 'count',
        'CGPA': ['mean', 'median', 'std', 'min', 'max'] if 'CGPA' in df.columns else 'count',
    }).round(2)
    
    # Flatten column names
    branch_stats.columns = ['Total_Students', 'Avg_CGPA', 'Median_CGPA', 'Std_CGPA', 'Min_CGPA', 'Max_CGPA']
    
    # Calculate pass percentage per branch
    if 'Result_Status' in df.columns:
        pass_pct = df.groupby('Branch').apply(
            lambda x: (x['Result_Status'].str.upper() == 'PASS').sum() / len(x) * 100
        ).round(2)
        branch_stats['Pass_Percentage'] = pass_pct
    
    # Calculate total backlogs per branch
    if 'Backlogs' in df.columns:
        total_backlogs = df.groupby('Branch')['Backlogs'].sum()
        branch_stats['Total_Backlogs'] = total_backlogs
    
    return branch_stats.reset_index()

def get_top_performers(df: pd.DataFrame, n: int = 10, by: str = 'overall', branch: str = None) -> pd.DataFrame:
    """
    Get top N performers
    
    Args:
        df: Result dataframe
        n: Number of top performers
        by: 'overall' or 'branch'
        branch: Specific branch name if by='branch'
        
    Returns:
        DataFrame with top performers
    """
    if df.empty or 'CGPA' not in df.columns:
        return pd.DataFrame()
    
    # Get unique students (in case of multiple rows per student)
    df_unique = df.sort_values('CGPA', ascending=False).drop_duplicates(subset='Roll_Number', keep='first')
    
    if by == 'overall':
        return df_unique.nlargest(n, 'CGPA')[['Roll_Number', 'Name', 'Branch', 'CGPA', 'SGPA']]
    elif by == 'branch' and branch:
        branch_df = df_unique[df_unique['Branch'] == branch]
        return branch_df.nlargest(n, 'CGPA')[['Roll_Number', 'Name', 'CGPA', 'SGPA']]
    else:
        # Top 3 from each branch
        return df_unique.groupby('Branch').apply(
            lambda x: x.nlargest(3, 'CGPA')[['Roll_Number', 'Name', 'CGPA']]
        ).reset_index(drop=True)

def calculate_subject_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate subject-wise analysis"""
    
    if df.empty or 'Subject_Name' not in df.columns:
        return pd.DataFrame()
    
    subject_stats = df.groupby('Subject_Name').agg({
        'Total_Marks': ['mean', 'median', 'std', 'min', 'max'],
        'Grade_Point': 'mean',
    }).round(2)
    
    subject_stats.columns = ['Avg_Marks', 'Median_Marks', 'Std_Marks', 'Min_Marks', 'Max_Marks', 'Avg_Grade_Point']
    
    # Calculate pass percentage per subject
    if 'Result_Status' in df.columns:
        pass_pct = df.groupby('Subject_Name').apply(
            lambda x: (x['Result_Status'].str.upper() == 'PASS').sum() / len(x) * 100
        ).round(2)
        subject_stats['Pass_Percentage'] = pass_pct
    
    # Calculate difficulty index (1 - normalized average)
    subject_stats['Difficulty_Index'] = (1 - (subject_stats['Avg_Marks'] / 100)).round(3)
    
    return subject_stats.reset_index().sort_values('Difficulty_Index', ascending=False)

def get_grade_distribution(df: pd.DataFrame, groupby: str = None) -> pd.DataFrame:
    """
    Calculate grade distribution
    
    Args:
        df: Result dataframe
        groupby: Optional column to group by (e.g., 'Branch', 'Subject_Name')
        
    Returns:
        Grade distribution dataframe
    """
    if df.empty or 'Letter_Grade' not in df.columns:
        return pd.DataFrame()
    
    if groupby and groupby in df.columns:
        dist = pd.crosstab(df[groupby], df['Letter_Grade'], normalize='index') * 100
    else:
        dist = df['Letter_Grade'].value_counts(normalize=True) * 100
    
    return dist.round(2)

def calculate_student_rank(df: pd.DataFrame, roll_number: str) -> Dict:
    """Calculate student's rank overall and within branch"""
    
    if df.empty or 'Roll_Number' not in df.columns:
        return {}
    
    student_data = df[df['Roll_Number'] == roll_number]
    
    if student_data.empty:
        return {}
    
    student = student_data.iloc[0]
    
    # Get unique students for ranking
    df_unique = df.drop_duplicates(subset='Roll_Number', keep='first')
    
    overall_rank = (df_unique['CGPA'] > student['CGPA']).sum() + 1
    
    if 'Branch' in df.columns:
        branch_df = df_unique[df_unique['Branch'] == student['Branch']]
        branch_rank = (branch_df['CGPA'] > student['CGPA']).sum() + 1
        branch_total = len(branch_df)
    else:
        branch_rank = overall_rank
        branch_total = len(df_unique)
    
    percentile = ((len(df_unique) - overall_rank) / len(df_unique) * 100) if len(df_unique) > 0 else 0
    
    return {
        'overall_rank': overall_rank,
        'total_students': len(df_unique),
        'branch_rank': branch_rank,
        'branch_total': branch_total,
        'percentile': round(percentile, 2)
    }

def get_cgpa_distribution(df: pd.DataFrame, bins: int = 10) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get CGPA distribution for histogram
    
    Returns:
        Tuple of (counts, bin_edges)
    """
    if df.empty or 'CGPA' not in df.columns:
        return np.array([]), np.array([])
    
    counts, bin_edges = np.histogram(df['CGPA'].dropna(), bins=bins, range=(0, 10))
    
    return counts, bin_edges
