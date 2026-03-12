"""
Data Processing Module for NHANES Oral Health Dashboard
Load, merge, and clean NHANES 2009-2010 data
"""

import pandas as pd
import numpy as np
from pyreadstat import read_xport
from pathlib import Path


def load_nhanes_data(data_dir='data/raw'):
    """
    Load NHANES 2009-2010 demographic and oral health examination data

    Parameters:
    -----------
    data_dir : str
        Directory containing the raw NHANES .XPT files

    Returns:
    --------
    tuple : (demo_df, oral_df, merge_info)
        DataFrames for demographics and oral health, plus merge statistics
    """
    data_path = Path(data_dir)

    print("Loading NHANES 2009-2010 data...")

    # Load Demographics Data (DEMO_F)
    demo_path = data_path / 'DEMO_F.XPT'
    print(f"  Loading demographics: {demo_path}")
    demo_df, demo_meta = read_xport(str(demo_path))
    print(f"    Loaded {len(demo_df):,} participants with {len(demo_df.columns)} variables")

    # Load Oral Health Examination Data (OHXDEN_F)
    oral_path = data_path / 'OHXDEN_F.XPT'
    print(f"  Loading oral health examinations: {oral_path}")
    oral_df, oral_meta = read_xport(str(oral_path))
    print(f"    Loaded {len(oral_df):,} participants with {len(oral_df.columns)} variables")

    merge_info = {
        'demo_count': len(demo_df),
        'oral_count': len(oral_df),
        'demo_vars': list(demo_df.columns),
        'oral_vars': list(oral_df.columns)
    }

    return demo_df, oral_df, merge_info


def merge_datasets(demo_df, oral_df):
    """
    Merge demographics and oral health datasets on SEQN identifier

    Parameters:
    -----------
    demo_df : DataFrame
        Demographics data
    oral_df : DataFrame
        Oral health examination data

    Returns:
    --------
    DataFrame : merged dataset with _merge indicator
    """
    print("\nMerging datasets...")

    # Merge on SEQN (respondent sequence number)
    merged = demo_df.merge(oral_df, on='SEQN', how='left', indicator=True)

    # Print merge statistics
    merge_counts = merged['_merge'].value_counts()
    print(f"  Both datasets: {merge_counts.get('both', 0):,} participants")
    print(f"  Demo only: {merge_counts.get('left_only', 0):,} participants")
    print(f"  Oral only: {merge_counts.get('right_only', 0):,} participants (should be 0)")

    return merged


def calculate_oral_health_outcomes(df):
    """
    Calculate derived oral health outcome variables

    Parameters:
    -----------
    df : DataFrame
        Merged NHANES data

    Returns:
    --------
    DataFrame : data with new oral health outcome columns
    """
    print("\nCalculating oral health outcomes...")

    df = df.copy()

    # Tooth count variables: OHX##TC where ## is tooth number (01-32)
    # TC status codes: 1=Primary, 2=Permanent, 3=Dental Implant, 4=Not present, 5=Permanent root fragment
    tooth_count_cols = [f'OHX{str(i).zfill(2)}TC' for i in range(1, 33)]

    # Calculate total teeth present (count teeth with TC = 2 (permanent) or 3 (implant))
    def count_teeth(row):
        count = 0
        for col in tooth_count_cols:
            if col in row and row[col] in [2.0, 3.0]:
                count += 1
        return count

    df['total_teeth'] = df.apply(count_teeth, axis=1)

    # Use NHANES summary variables for dental caries
    # OHXDECAY: Decayed teeth (1=Yes, 2=No, 9=Cannot assess)
    if 'OHXDECAY' in df.columns:
        df['has_untreated_decay'] = df['OHXDECAY'].apply(
            lambda x: 1 if x == 1.0 else (0 if x == 2.0 else np.nan)
        )
    else:
        df['has_untreated_decay'] = np.nan

    # OHXREST: Restorations (1=Yes, 2=No, 9=Cannot assess)
    if 'OHXREST' in df.columns:
        df['has_restorations'] = df['OHXREST'].apply(
            lambda x: 1 if x == 1.0 else (0 if x == 2.0 else np.nan)
        )

    # OHXSEAL: Dental sealants (1=Yes, 2=No, 9=Cannot assess)
    if 'OHXSEAL' in df.columns:
        df['has_sealants'] = df['OHXSEAL'].apply(
            lambda x: 1 if x == 1.0 else (0 if x == 2.0 else np.nan)
        )

    # Edentulism (complete tooth loss)
    df['edentulous'] = (df['total_teeth'] == 0).astype(int)

    # Create a combined oral disease indicator
    # Has ANY oral health issue: decay OR edentulism
    df['any_oral_disease'] = ((df['has_untreated_decay'] == 1) | (df['edentulous'] == 1)).astype(int)

    # Count non-missing values for reporting
    decay_n = df['has_untreated_decay'].notna().sum()
    decay_yes = (df['has_untreated_decay'] == 1).sum()

    print(f"  Created oral health outcomes:")
    print(f"    - total_teeth: mean = {df['total_teeth'].mean():.1f}, median = {df['total_teeth'].median():.0f}")
    print(f"    - edentulous: {df['edentulous'].sum():,} participants ({df['edentulous'].mean()*100:.1f}%)")
    print(f"    - has_untreated_decay: {decay_yes:,} of {decay_n:,} assessed ({decay_yes/decay_n*100 if decay_n > 0 else 0:.1f}%)")
    if 'has_restorations' in df.columns:
        rest_n = df['has_restorations'].notna().sum()
        rest_yes = (df['has_restorations'] == 1).sum()
        print(f"    - has_restorations: {rest_yes:,} of {rest_n:,} assessed ({rest_yes/rest_n*100 if rest_n > 0 else 0:.1f}%)")

    return df


def create_demographic_categories(df):
    """
    Create categorized demographic variables for analysis

    Parameters:
    -----------
    df : DataFrame
        Merged NHANES data with demographic variables

    Returns:
    --------
    DataFrame : data with new categorical variables
    """
    print("\nCreating demographic categories...")

    df = df.copy()

    # Age groups
    df['age_group'] = pd.cut(
        df['RIDAGEYR'],
        bins=[0, 20, 35, 50, 65, 150],
        labels=['Under 20', '20-34', '35-49', '50-64', '65+'],
        right=False
    )

    # Gender (RIAGENDR: 1=Male, 2=Female)
    df['gender'] = df['RIAGENDR'].map({1: 'Male', 2: 'Female'})

    # Race/Ethnicity (RIDRETH1)
    # 1 = Mexican American, 2 = Other Hispanic, 3 = Non-Hispanic White,
    # 4 = Non-Hispanic Black, 5 = Other Race
    race_map = {
        1: 'Mexican American',
        2: 'Other Hispanic',
        3: 'Non-Hispanic White',
        4: 'Non-Hispanic Black',
        5: 'Other Race'
    }
    df['race_ethnicity'] = df['RIDRETH1'].map(race_map)

    # Education level (DMDEDUC2 - for adults 20+)
    # 1 = Less than 9th grade, 2 = 9-11th grade, 3 = High school/GED,
    # 4 = Some college, 5 = College graduate
    edu_map = {
        1: 'Less than HS',
        2: 'Less than HS',  # Combine < 9th and 9-11th
        3: 'High school/GED',
        4: 'Some college',
        5: 'College graduate'
    }
    df['education'] = df['DMDEDUC2'].map(edu_map)

    # Poverty level (INDFMPIR - Income-to-poverty ratio)
    # <1.0 = Below poverty, 1.0-1.99 = Near poverty, 2.0+ = Above poverty
    df['poverty_category'] = pd.cut(
        df['INDFMPIR'],
        bins=[0, 1, 2, float('inf')],
        labels=['Below poverty', 'Near poverty', 'Above poverty'],
        right=False
    )

    print(f"  Created demographic categories:")
    print(f"    - age_group: {df['age_group'].value_counts().to_dict()}")
    print(f"    - gender: {df['gender'].value_counts().to_dict()}")
    print(f"    - race_ethnicity: {df['race_ethnicity'].value_counts().to_dict()}")
    print(f"    - education: {df['education'].value_counts().to_dict()}")
    print(f"    - poverty_category: {df['poverty_category'].value_counts().to_dict()}")

    return df


def create_analysis_dataset(data_dir='data/raw', output_path='data/processed/nhanes_merged.csv'):
    """
    Main function to create analysis-ready dataset

    Parameters:
    -----------
    data_dir : str
        Directory containing raw NHANES files
    output_path : str
        Path to save the merged dataset

    Returns:
    --------
    DataFrame : analysis-ready dataset
    """
    # Load data
    demo_df, oral_df, merge_info = load_nhanes_data(data_dir)

    # Merge datasets
    merged = merge_datasets(demo_df, oral_df)

    # Keep only participants with oral health exam data
    analysis_data = merged[merged['_merge'] == 'both'].copy()
    print(f"\nFinal analysis dataset: {len(analysis_data):,} participants")

    # Calculate oral health outcomes
    analysis_data = calculate_oral_health_outcomes(analysis_data)

    # Create demographic categories
    analysis_data = create_demographic_categories(analysis_data)

    # Save to CSV
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    analysis_data.to_csv(output_path, index=False)
    print(f"\nSaved analysis dataset to: {output_path}")
    print(f"  Shape: {analysis_data.shape}")

    return analysis_data


if __name__ == '__main__':
    # Run the data processing pipeline
    print("="*60)
    print("NHANES 2009-2010 Oral Health Data Processing")
    print("="*60)

    analysis_df = create_analysis_dataset()

    print("\n" + "="*60)
    print("Data processing complete!")
    print("="*60)
