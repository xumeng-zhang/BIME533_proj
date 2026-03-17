"""
NHANES Oral Health Disparities Dashboard
Main Landing Page
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="NHANES Oral Health Dashboard",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and introduction
st.title("🦷 NHANES Oral Health Disparities Dashboard")
st.markdown("### Exploring Oral Health Inequities Across Demographic and Socioeconomic Groups")

# Introduction
st.markdown("""
Welcome to the NHANES Oral Health Disparities Dashboard. This interactive tool visualizes
oral health outcomes across different population groups using data from the National Health
and Nutrition Examination Survey (NHANES) 2009-2010.
""")

# Target audience callout
st.info("""
### Who is this dashboard for?

This dashboard is designed for **public health program coordinators** at state and local
health departments who need to:
- Identify which demographic groups have the worst oral health outcomes
- Support grant applications with disparity evidence
- Prioritize intervention programs
- Compare outcomes across socioeconomic factors

**Skills assumed:** Intermediate quantitative literacy (comfortable interpreting percentages,
bar charts, and confidence intervals)
""")

# Key statistics overview
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Sample Size",
        value="8,189",
        help="Participants with dental examination data"
    )

with col2:
    st.metric(
        label="🦷 Avg Teeth Present",
        value="17.5",
        help="Mean number of permanent teeth (out of 28)"
    )

with col3:
    st.metric(
        label="⚠️ Untreated Decay",
        value="17.4%",
        help="Prevalence of untreated tooth decay"
    )

with col4:
    st.metric(
        label="❌ Complete Tooth Loss",
        value="23.1%",
        help="Prevalence of edentulism (no teeth remaining)"
    )

# Highlight key disparities
st.markdown("---")
st.markdown("## 🎯 Key Disparities Identified")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### Race/Ethnicity Disparities
    - **Mexican Americans** have **1.9x higher** prevalence of untreated decay (21.4%)
      compared to other racial groups
    - Significant differences persist after accounting for survey design
    """)

    st.markdown("""
    #### Education Gradient
    - **College graduates** have **7.2 more teeth** on average than those with less than
      high school education
    - Clear dose-response relationship between education and oral health
    """)

with col2:
    st.markdown("""
    #### Poverty Impact
    - Those **below poverty** have **1.4x higher** rate of complete tooth loss (26.0%)
      compared to those above poverty line
    - Economic disparities compound with age
    """)

    st.markdown("""
    #### Age-Related Burden
    - Oral health deteriorates with age across all demographic groups
    - Disparities widen in older age groups
    """)

# Navigation guide
st.markdown("---")
st.markdown("## 📍 How to Use This Dashboard")

st.markdown("""
Use the **sidebar navigation** (← left side) to explore different sections:

1. **📊 Overview** - Summary of key findings (this page)
2. **🔍 Explore Data** - Interactive visualizations to investigate disparities by different demographic variables
3. **📖 Methodology** - Learn about data sources, methods, and key concepts

Each page includes:
- Interactive charts you can explore
- Confidence intervals showing statistical uncertainty
- Download options for data and figures
- Plain language explanations of findings
""")

# Data source citation
st.markdown("---")
st.markdown("## 📚 Data Source")

st.markdown("""
**National Health and Nutrition Examination Survey (NHANES) 2009-2010**

- **Survey Design:** Nationally representative cross-sectional survey of the U.S. civilian,
  non-institutionalized population
- **Data Collection:** January 2009 - December 2010
- **Sample Size:** 10,537 participants surveyed; 8,189 with dental examination data
- **Conducted by:** Centers for Disease Control and Prevention (CDC), National Center for
  Health Statistics (NCHS)
- **Documentation:** [NHANES 2009-2010 Overview](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/overview.aspx?BeginYear=2009)
""")

# Footer
st.markdown("---")
st.caption("""
**BIME 533 Final Project** | University of Washington | March 2026
Dashboard created with [Streamlit](https://streamlit.io) | Data from [CDC NHANES](https://www.cdc.gov/nchs/nhanes/)

⚠️ Data is from 2009-2010 and should be interpreted with appropriate temporal context
""")

# Sidebar information
with st.sidebar:
    st.markdown("## About This Dashboard")
    st.markdown("""
                
    This dashboard presents **survey-weighted** analyses of oral health disparities
    using NHANES 2009-2010 data.
    """)

    st.markdown("---")
    st.markdown("""
    ### Need Help?

    Hover over charts and metrics for explanations.
    Visit the Methodology page for detailed information about methods and limitations.
    """)
