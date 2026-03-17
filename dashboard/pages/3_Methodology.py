"""
Methodology - Understanding the Data and Analysis
"""

import streamlit as st

st.set_page_config(page_title="Methodology", page_icon="📖", layout="wide")

st.title("📖 Methodology")

st.markdown("""
This page explains the data source, key concepts, and limitations you need to understand
when interpreting the results.
""")

# =============================================================================
# DATA SOURCE
# =============================================================================
st.markdown("## 📊 Data Source: NHANES 2009-2010")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    **National Health and Nutrition Examination Survey (NHANES)** is a nationally
    representative survey of the U.S. population conducted by the CDC.

    **Key Details:**
    - **Population:** U.S. civilian, non-institutionalized population
    - **Survey Period:** 2009-2010
    - **Total Participants:** 10,537 surveyed; 8,189 had dental examinations
    - **Design:** Complex, multi-stage probability sample with oversampling of certain groups

    **Data Files Used:**
    - [Demographics (DEMO_F)] - Age, race, education, income
    - [Oral Health (OHXDEN_F)] - Tooth counts, decay, restorations

    **Integration:** Files merged using participant ID (SEQN). Only participants with
    both demographic and dental exam data are included (n=8,189).
    """)

with col2:
    st.info("""
    **NOTE: This dashborad is only using 2009-2010 for now.**

    
    It's designed to showcase the use of informatics tools that can improve understanding the **patterns of disparities**,
    which tend to be stable over time even if absolute rates change.
    """)

# =============================================================================
# SURVEY WEIGHTING
# =============================================================================
st.markdown("---")
st.markdown("## ⚖️ Survey Weighting Explained")

st.markdown("""
NHANES doesn't survey everyone equally. They intentionally oversample certain groups
(e.g., minorities, elderly) to get enough data for analysis. **Without accounting for this,
estimates would be biased.**
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### What We Do

    All estimates use **survey weights** (WTMEC2YR) that adjust for:
    - Unequal probability of selection
    - Survey non-response
    - Post-stratification to U.S. population totals

    **Result:** Our estimates represent the entire U.S. population, not just survey participants.
    """)

with col2:
    st.markdown("""
    ### What This Means for You

    - Percentages are **population estimates**, not raw survey percentages
    - Confidence intervals are wider than simple samples (accounts for survey design)
    - Sample sizes shown are actual participants, but estimates are weighted
    """)

# =============================================================================
# STATISTICAL NOTES
# =============================================================================
st.markdown("---")
st.markdown("## 🔢 Statistical Methods")

with st.expander("How we calculate prevalence (for binary outcomes like decay)"):
    st.markdown("""
    **For yes/no outcomes:**

    1. Calculate weighted proportion: (sum of weights for "yes") / (total weights)
    2. Calculate standard error accounting for survey design
    3. Compute 95% CI: estimate ± 1.96 × standard error

    """)

with st.expander("How we calculate means (for continuous outcomes like tooth count)"):
    st.markdown("""
    **For continuous outcomes:**

    1. Calculate weighted mean: (sum of [weight × value]) / (sum of weights)
    2. Calculate weighted variance
    3. Compute design-adjusted standard error
    4. Compute 95% CI: mean ± 1.96 × standard error

    The weighted mean represents the population average, not just the survey sample average.
    """)


# =============================================================================
# UNDERSTANDING CONFIDENCE INTERVALS
# =============================================================================
st.markdown("---")
st.markdown("## 📊 Understanding Confidence Intervals")

st.markdown("""
All charts show **95% confidence intervals** (error bars). Here's what they mean:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### What is a CI?

    If we repeated the survey many times, the true population value would fall within
    this range **95% of the time**.

    It's our uncertainty about the population estimate, not variability in people.
    """)

with col2:
    st.markdown("""
    ### What Affects Width?

    - **Sample size:** Smaller groups = wider intervals
    - **Variability:** More variation = wider intervals
    - **Survey design:** Complex designs = wider intervals
    """)


# =============================================================================
# LIMITATIONS
# =============================================================================
st.markdown("---")
st.markdown("## ⚠️ Important Limitations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Data Limitations

    **Age of Data**
    - Data is from 2009-2010 (15+ years old)
    - Use for understanding **disparity patterns**, not current rates

    **Cross-Sectional Design**
    - One-time snapshot, not longitudinal
    - **Cannot determine causation** - only associations
    - Example: Education correlates with oral health, but we can't prove it causes better outcomes

    **Missing Data**
    - Only 77.7% of participants had dental exams
    - Some analyses have smaller sample sizes
    - Could introduce bias if missingness is related to outcomes
    """)

with col2:
    st.markdown("""
    ### What You Can/Cannot Do

    **✅ Good Uses:**
    - Identify which groups have worse outcomes
    - Understand magnitude of disparities
    - Prioritize populations for intervention
    - Support grant applications

    **❌ Don't Use For:**
    - Predicting individual outcomes
    - Making causal claims
    - Estimating current (2026) prevalence
    - Local or state-level estimates
    - Clinical decision-making
    """)


# Footer
st.markdown("---")
st.markdown("""
### 📚 Learn More

- [NHANES 2009-2010 Overview](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/overview.aspx?BeginYear=2009)
- [NHANES Analytic Guidelines](https://wwwn.cdc.gov/nchs/nhanes/analyticguidelines.aspx)
- [CDC Oral Health Disparities](https://www.cdc.gov/oral-health/health-equity/index.html)
""")
