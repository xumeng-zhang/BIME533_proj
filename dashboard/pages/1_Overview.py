"""
Overview Page - Key Findings
"""

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Key Findings", page_icon="📊", layout="wide")

st.title("📊 Key Findings: Oral Health Disparities in the United States")

st.markdown("""
Based on analysis of NHANES 2009-2010 data, we identified significant oral health
disparities across racial/ethnic, socioeconomic, and educational lines.
""")

# Load key findings
findings_path = Path(__file__).parents[2] / 'results' / 'key_findings.txt'
if findings_path.exists():
    with open(findings_path, 'r') as f:
        findings_text = f.read()

    # Display findings in expandable sections
    st.markdown("## 🔍 Major Findings")

    findings_list = findings_text.split('\n\n')[1:-1]  # Skip header and empty lines

    for i, finding in enumerate(findings_list, 1):
        if finding.strip():
            # Extract title and content
            parts = finding.split(':', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                content = parts[1].strip()
                with st.expander(title, expanded=(i <= 2)):
                    st.markdown(f"**{content}**")

# Display figures
st.markdown("---")
st.markdown("## 📈 Visual Summary of Disparities")

# Create tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs([
    "Race/Ethnicity",
    "Education",
    "Poverty",
    "Age"
])

# Correct path to figures directory
figures_dir = Path(__file__).parents[2] / 'results' / 'figures'

with tab1:
    st.markdown("### Untreated Tooth Decay by Race/Ethnicity")
    img_path = figures_dir / 'decay_by_race.png'
    if img_path.exists():
        st.image(str(img_path), use_column_width=True)
        st.markdown("""
        **Key Insight:** Mexican Americans and Non-Hispanic Blacks show nearly double the
        prevalence of untreated tooth decay compared to other racial/ethnic groups. Error
        bars represent 95% confidence intervals accounting for survey design.
        """)
    else:
        st.warning("Figure not found. Run generate_analysis.py first.")

with tab2:
    st.markdown("### Average Teeth Present by Education Level")
    img_path = figures_dir / 'teeth_by_education.png'
    if img_path.exists():
        st.image(str(img_path), use_column_width=True)
        st.markdown("""
        **Key Insight:** A clear education gradient exists - college graduates have an average
        of 23.3 teeth while those with less than high school education have only 16.1 teeth.
        This represents a loss of 7 teeth (25% of full dentition). The dashed line shows full
        dentition (28 permanent teeth, excluding wisdom teeth).
        """)
    else:
        st.warning("Figure not found. Run generate_analysis.py first.")

with tab3:
    st.markdown("### Complete Tooth Loss by Poverty Level")
    img_path = figures_dir / 'edentulism_by_poverty.png'
    if img_path.exists():
        st.image(str(img_path), use_column_width=True)
        st.markdown("""
        **Key Insight:** Those living below the poverty line have 26% prevalence of complete
        tooth loss (edentulism) compared to 18% for those above poverty. This 1.4x difference
        highlights the strong relationship between economic status and oral health outcomes.
        """)
    else:
        st.warning("Figure not found. Run generate_analysis.py first.")

with tab4:
    st.markdown("### Untreated Tooth Decay by Age Group")
    img_path = figures_dir / 'decay_by_age.png'
    if img_path.exists():
        st.image(str(img_path), use_column_width=True)
        st.markdown("""
        **Key Insight:** Dental decay patterns vary across age groups, with important
        implications for targeted intervention programs.
        """)
    else:
        st.warning("Figure not found. Run generate_analysis.py first.")

# Implications section
st.markdown("---")
st.markdown("## 💡 Implications for Public Health Practice")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Targeted Interventions Needed

    These disparities suggest the need for:

    - **Culturally-tailored** oral health programs for high-risk racial/ethnic groups
    - **School-based** dental sealant programs in low-income areas
    - **Community health worker** outreach to populations with limited dental access
    - **Medicaid expansion** for adult dental coverage
    """)

with col2:
    st.markdown("""
    ### Priority Populations

    Programs should prioritize:

    - **Mexican American** and **Non-Hispanic Black** communities (highest decay prevalence)
    - **Low-income** populations (highest tooth loss rates)
    - Adults with **less than high school** education (poorest outcomes)
    - **Older adults** below poverty line (compounding effects)
    """)

# Data quality note
st.info("""
### Note on Data Quality

All estimates shown are **survey-weighted** to represent the U.S. population and account for
NHANES's complex sampling design. Confidence intervals reflect both sampling variability and
design effects. Sample sizes vary by outcome due to different examination protocols.
""")

# Next steps
st.markdown("---")
st.markdown("""
### 🔍 Want to Explore Further?

Navigate to **🔍 Explore Data** in the sidebar to interactively investigate these
disparities and create your own comparisons across different demographic variables.
""")
