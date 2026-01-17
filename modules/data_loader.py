"""
Data Loader Module
Handles loading and caching of result data
"""

import pandas as pd
import streamlit as st
from typing import Optional
import os

@st.cache_data(ttl=3600)
def load_result_data(filepath: str = 'data/results_data.csv') -> pd.DataFrame:
    """
    Load and cache result data with proper type conversions
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        DataFrame with result data
    """
    try:
        # Check if file exists
        if not os.path.exists(filepath):
            st.error(f"⚠️ Data file not found: {filepath}")
            st.info("Please ensure the PDF extraction script has been run and data file is in the correct location.")
            return pd.DataFrame()
        
        # Load data
        df = pd.read_csv(filepath)
        
        # Clean column names (remove extra spaces)
        df.columns = df.columns.str.strip()
        
        # Standardize column names - handle both old and new formats
        column_mapping = {
            'Student_Name': 'Name',  # Map new format to old format for compatibility
            'Total_Credits': 'Credits',  # Standardize Credits column
        }
        
        # Apply column mapping
        for new_col, old_col in column_mapping.items():
            if new_col in df.columns and old_col not in df.columns:
                df[old_col] = df[new_col]
        
        # Data type conversions
        if 'Roll_Number' in df.columns:
            df['Roll_Number'] = df['Roll_Number'].astype(str)
        
        # Convert numeric columns
        numeric_cols = ['CGPA', 'SGPA', 'Total_Marks', 'Internal_Marks', 'External_Marks', 'Grade_Point', 'Credits', 'Backlogs', 'Total_Credits']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Extract branch specialization from roll numbers
        df = _add_branch_specialization(df)
        
        return df
    
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame()

def _add_branch_specialization(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract branch code and specialization from roll numbers
    Roll number format: 2023UCB6036 where UCB = CSE - Big Data Analytics
    """
    import re
    
    # Branch code to specialization mapping
    BRANCH_SPECIALIZATIONS = {
        'UBT': ('BIO-TECH', 'Bio Technology'),
        'UCE': ('CE', 'Civil Engineering'),
        'UCS': ('CSE', 'Computer Science Engineering'),
        'UCA': ('CSE', 'Artificial Intelligence (CSAI)'),
        'UCD': ('CSE', 'Data Science (CSDS)'),
        'UCM': ('MAC', 'Mathematics and Computing'),
        'UCB': ('CSE', 'Big Data Analytics (CSDA)'),
        'UCI': ('CSE', 'IoT (CIOT)'),
        'UEE': ('EE', 'Electrical Engineering'),
        'UEC': ('ECE', 'Electronics & Communication'),
        'UEI': ('ECE', 'ECE - IoT (EIOT)'),
        'UEA': ('ECE', 'ECE - AI (ECAM)'),
        'UCG': ('GI', 'Geoinformatics'),
        'UIT': ('IT', 'Information Technology'),
        'UIN': ('IT', 'IT - Network Security (ITNS)'),
        'UIC': ('ICE', 'Instrumentation & Control'),
        'UME': ('ME', 'Mechanical Engineering'),
        'UMV': ('ME', 'Mechanical Engineering (MEEV)'),
    }
    
    def extract_branch_info(roll_number):
        """Extract branch code from roll number"""
        if pd.isna(roll_number) or not isinstance(roll_number, str):
            return None, None, None
        
        # Extract 3-letter code (e.g., UCB from 2023UCB6036)
        match = re.search(r'\d{4}([A-Z]{3})', str(roll_number))
        if match:
            code = match.group(1)
            if code in BRANCH_SPECIALIZATIONS:
                parent, full_name = BRANCH_SPECIALIZATIONS[code]
                return code, parent, full_name
        return None, None, None
    
    # Extract branch information
    if 'Roll_Number' in df.columns:
        branch_info = df['Roll_Number'].apply(extract_branch_info)
        df['Branch_Code'] = branch_info.apply(lambda x: x[0])
        df['Parent_Branch'] = branch_info.apply(lambda x: x[1])
        df['Branch_Specialization'] = branch_info.apply(lambda x: x[2])
        
        # Fill in missing values with original branch
        df['Parent_Branch'] = df['Parent_Branch'].fillna(df['Branch'])
        df['Branch_Specialization'] = df['Branch_Specialization'].fillna(df['Branch'])
    
    return df

def filter_data(df: pd.DataFrame, 
                branch: Optional[str] = None,
                section: Optional[str] = None,
                min_cgpa: float = 0.0,
                max_cgpa: float = 10.0,
                result_status: Optional[str] = None) -> pd.DataFrame:
    """
    Filter dataframe based on multiple criteria
    
    Args:
        df: Input dataframe
        branch: Branch code (e.g., 'CSE')
        section: Section (e.g., 'A')
        min_cgpa: Minimum CGPA filter
        max_cgpa: Maximum CGPA filter
        result_status: Pass/Fail filter
        
    Returns:
        Filtered dataframe
    """
    filtered = df.copy()
    
    if branch and branch != 'All':
        filtered = filtered[filtered['Branch'] == branch]
    
    if section and section != 'All':
        filtered = filtered[filtered['Section'] == section]
    
    if 'CGPA' in filtered.columns:
        filtered = filtered[(filtered['CGPA'] >= min_cgpa) & (filtered['CGPA'] <= max_cgpa)]
    
    if result_status and result_status != 'All':
        filtered = filtered[filtered['Result_Status'] == result_status]
    
    return filtered

def get_unique_values(df: pd.DataFrame, column: str) -> list:
    """Get sorted unique values from a column"""
    if column in df.columns:
        return sorted(df[column].dropna().unique().tolist())
    return []

def search_student(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """
    Search for students by roll number or name
    
    Args:
        df: Result dataframe
        search_term: Roll number or name to search
        
    Returns:
        Filtered dataframe with matching students
    """
    search_term = search_term.strip().upper()
    
    if not search_term:
        return pd.DataFrame()
    
    # Search in roll number and name columns
    mask = (
        df['Roll_Number'].str.upper().str.contains(search_term, na=False) |
        df['Name'].str.upper().str.contains(search_term, na=False)
    )
    
    return df[mask]
