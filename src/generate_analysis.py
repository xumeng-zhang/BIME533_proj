"""
Generate key analysis results and figures for NHANES Oral Health Dashboard
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('src')
from survey_analysis import weighted_prevalence, weighted_mean, calculate_disparity_metrics

# Set plotting style
sns.set_style("whitegrid")
sns.set_context("talk")
plt.rcParams['figure.figsize'] = (12, 6)

# Load data
print("Loading data...")
data = pd.read_csv('results/nhanes_merged.csv')
print(f"Loaded {len(data):,} participants\n")

# Create figures directory
import os
os.makedirs('results/figures', exist_ok=True)

# =============================================================================
# ANALYSIS 1: Untreated Decay by Race/Ethnicity
# =============================================================================
print("="*70)
print("ANALYSIS 1: Untreated Decay Prevalence by Race/Ethnicity")
print("="*70)

decay_race = weighted_prevalence(data, 'has_untreated_decay', 'race_ethnicity')
print(decay_race)
print()

# Calculate disparities
decay_race_disp = calculate_disparity_metrics(decay_race)
print("\nDisparity Metrics:")
print(decay_race_disp)

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(decay_race))
ax.bar(x, decay_race['prevalence'], color='steelblue', alpha=0.7)
ax.errorbar(x, decay_race['prevalence'],
            yerr=[decay_race['prevalence'] - decay_race['ci_lower'],
                  decay_race['ci_upper'] - decay_race['prevalence']],
            fmt='none', color='black', capsize=5)
ax.set_xticks(x)
ax.set_xticklabels(decay_race['group'], rotation=45, ha='right')
ax.set_ylabel('Prevalence of Untreated Decay (%)')
ax.set_title('Untreated Tooth Decay by Race/Ethnicity\nNHANES 2009-2010')
ax.set_ylim(0, max(decay_race['ci_upper']) * 1.1)
plt.tight_layout()
plt.savefig('results/figures/decay_by_race.png', dpi=300, bbox_inches='tight')
print("\nSaved figure: results/figures/decay_by_race.png")
plt.close()

# =============================================================================
# ANALYSIS 2: Average Teeth Present by Education Level
# =============================================================================
print("\n" + "="*70)
print("ANALYSIS 2: Average Teeth Present by Education Level")
print("="*70)

teeth_edu = weighted_mean(data, 'total_teeth', 'education')
print(teeth_edu)

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(teeth_edu))
ax.bar(x, teeth_edu['mean'], color='forestgreen', alpha=0.7)
ax.errorbar(x, teeth_edu['mean'],
            yerr=[teeth_edu['mean'] - teeth_edu['ci_lower'],
                  teeth_edu['ci_upper'] - teeth_edu['mean']],
            fmt='none', color='black', capsize=5)
ax.set_xticks(x)
ax.set_xticklabels(teeth_edu['group'], rotation=45, ha='right')
ax.set_ylabel('Mean Number of Teeth Present')
ax.set_title('Average Teeth Present by Education Level\nNHANES 2009-2010')
ax.axhline(y=28, color='gray', linestyle='--', alpha=0.5, label='Full dentition (28 teeth)')
ax.legend()
ax.set_ylim(0, 32)
plt.tight_layout()
plt.savefig('results/figures/teeth_by_education.png', dpi=300, bbox_inches='tight')
print("\nSaved figure: results/figures/teeth_by_education.png")
plt.close()

# =============================================================================
# ANALYSIS 3: Edentulism by Poverty Level
# =============================================================================
print("\n" + "="*70)
print("ANALYSIS 3: Edentulism (Complete Tooth Loss) by Poverty Level")
print("="*70)

edent_pov = weighted_prevalence(data, 'edentulous', 'poverty_category')
print(edent_pov)

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(edent_pov))
ax.bar(x, edent_pov['prevalence'], color='coral', alpha=0.7)
ax.errorbar(x, edent_pov['prevalence'],
            yerr=[edent_pov['prevalence'] - edent_pov['ci_lower'],
                  edent_pov['ci_upper'] - edent_pov['prevalence']],
            fmt='none', color='black', capsize=5)
ax.set_xticks(x)
ax.set_xticklabels(edent_pov['group'], rotation=45, ha='right')
ax.set_ylabel('Prevalence of Edentulism (%)')
ax.set_title('Complete Tooth Loss by Poverty Level\nNHANES 2009-2010')
ax.set_ylim(0, max(edent_pov['ci_upper']) * 1.1)
plt.tight_layout()
plt.savefig('results/figures/edentulism_by_poverty.png', dpi=300, bbox_inches='tight')
print("\nSaved figure: results/figures/edentulism_by_poverty.png")
plt.close()

# =============================================================================
# ANALYSIS 4: Decay by Age Group
# =============================================================================
print("\n" + "="*70)
print("ANALYSIS 4: Untreated Decay by Age Group")
print("="*70)

decay_age = weighted_prevalence(data, 'has_untreated_decay', 'age_group')
print(decay_age)

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(decay_age))
ax.bar(x, decay_age['prevalence'], color='mediumpurple', alpha=0.7)
ax.errorbar(x, decay_age['prevalence'],
            yerr=[decay_age['prevalence'] - decay_age['ci_lower'],
                  decay_age['ci_upper'] - decay_age['prevalence']],
            fmt='none', color='black', capsize=5)
ax.set_xticks(x)
ax.set_xticklabels(decay_age['group'], rotation=45, ha='right')
ax.set_ylabel('Prevalence of Untreated Decay (%)')
ax.set_title('Untreated Tooth Decay by Age Group\nNHANES 2009-2010')
ax.set_ylim(0, max(decay_age['ci_upper']) * 1.1)
plt.tight_layout()
plt.savefig('results/figures/decay_by_age.png', dpi=300, bbox_inches='tight')
print("\nSaved figure: results/figures/decay_by_age.png")
plt.close()

# =============================================================================
# Generate Key Findings Summary
# =============================================================================
print("\n" + "="*70)
print("KEY FINDINGS SUMMARY")
print("="*70)

findings = []

# Finding 1: Racial/ethnic disparities in untreated decay
max_decay_race = decay_race.loc[decay_race['prevalence'].idxmax()]
min_decay_race = decay_race.loc[decay_race['prevalence'].idxmin()]
ratio = max_decay_race['prevalence'] / min_decay_race['prevalence']
findings.append(f"1. Racial/Ethnic Disparity in Untreated Decay: {max_decay_race['group']} has {ratio:.1f}x higher prevalence ({max_decay_race['prevalence']:.1f}%) compared to {min_decay_race['group']} ({min_decay_race['prevalence']:.1f}%)")

# Finding 2: Education gradient in teeth present
max_teeth_edu = teeth_edu.loc[teeth_edu['mean'].idxmax()]
min_teeth_edu = teeth_edu.loc[teeth_edu['mean'].idxmin()]
diff = max_teeth_edu['mean'] - min_teeth_edu['mean']
findings.append(f"2. Education Gradient in Oral Health: {max_teeth_edu['group']} have {diff:.1f} more teeth on average ({max_teeth_edu['mean']:.1f}) compared to {min_teeth_edu['group']} ({min_teeth_edu['mean']:.1f})")

# Finding 3: Poverty and edentulism
max_edent_pov = edent_pov.loc[edent_pov['prevalence'].idxmax()]
min_edent_pov = edent_pov.loc[edent_pov['prevalence'].idxmin()]
ratio_edent = max_edent_pov['prevalence'] / min_edent_pov['prevalence']
findings.append(f"3. Poverty and Complete Tooth Loss: {max_edent_pov['group']} have {ratio_edent:.1f}x higher rate of edentulism ({max_edent_pov['prevalence']:.1f}%) vs {min_edent_pov['group']} ({min_edent_pov['prevalence']:.1f}%)")

# Finding 4: Overall burden
overall_decay = weighted_prevalence(data, 'has_untreated_decay', 'gender')
overall_decay_prev = overall_decay['prevalence'].mean()
overall_edent = weighted_prevalence(data, 'edentulous', 'gender')
overall_edent_prev = overall_edent['prevalence'].mean()
findings.append(f"4. Overall Oral Health Burden: {overall_decay_prev:.1f}% have untreated tooth decay and {overall_edent_prev:.1f}% have lost all their teeth")

for finding in findings:
    print(finding)

# Save findings to file
with open('results/key_findings.txt', 'w') as f:
    f.write("KEY FINDINGS: NHANES 2009-2010 Oral Health Disparities\n")
    f.write("="*70 + "\n\n")
    for finding in findings:
        f.write(finding + "\n\n")

print("\nSaved key findings to: results/key_findings.txt")

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)
print(f"Generated 4 figures in results/figures/")
print(f"Generated key findings summary in results/key_findings.txt")
