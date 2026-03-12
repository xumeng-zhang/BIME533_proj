"""
Methodology and Trust Page - Addressing Trustworthiness and Transparency
"""

import streamlit as st

st.set_page_config(page_title="Methodology", page_icon="📖", layout="wide")

st.title("📖 Methodology & Trustworthiness")

st.markdown("""
This page explains the data sources, methods, and design principles that make this
dashboard trustworthy and reliable for public health decision-making.
""")

# =============================================================================
# WHAT MAKES THIS DASHBOARD TRUSTWORTHY?
# =============================================================================
st.markdown("---")
st.markdown("## ✅ What Makes This Dashboard Trustworthy?")

st.markdown("""
We designed this dashboard with six key principles of trustworthiness in mind:
""")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Data Provenance",
    "Methodological Transparency",
    "Uncertainty Communication",
    "Professional Design",
    "Reproducibility",
    "Appropriate Use"
])

with tab1:
    st.markdown("### 1. Clear Data Provenance")
    st.markdown("""
    **Why this matters:** Knowing where data comes from helps you judge its quality and relevance.

    **What we do:**
    - Use data from a **gold-standard source**: CDC's National Health and Nutrition Examination
      Survey (NHANES), the most comprehensive health survey in the United States
    - Provide **direct links** to original data files and documentation
    - Clearly state **data collection period** (2009-2010)
    - Acknowledge **survey design** (nationally representative, probability sample)

    **Data Sources:**
    - 📊 [DEMO_F: Demographics Data](https://wwwn.cdc.gov/Nchs/Nhanes/2009-2010/DEMO_F.htm)
    - 🦷 [OHXDEN_F: Oral Health Examination Data](https://wwwn.cdc.gov/Nchs/Nhanes/2009-2010/OHXDEN_F.htm)
    - 📖 [NHANES 2009-2010 Overview](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/overview.aspx?BeginYear=2009)
    """)

with tab2:
    st.markdown("### 2. Methodological Transparency")
    st.markdown("""
    **Why this matters:** Understanding the methods helps you know what the numbers actually mean
    and what limitations to consider.

    **What we do:**
    - Explain **how we calculated estimates** (survey-weighted analysis)
    - Document **data integration process** (see section below)
    - State **statistical assumptions** clearly
    - Disclose **limitations** (e.g., cross-sectional design, data age)
    - Provide access to **all analysis code** (see Reproducibility tab)
    """)

    st.info("""
    **Survey Weighting Explained:**

    NHANES doesn't survey everyone equally - they oversample certain groups (e.g., minorities,
    elderly) to ensure adequate representation. Without weights, our estimates would be biased.

    **What we do:** Use MEC examination weights (WTMEC2YR) that account for:
    - Unequal probability of selection
    - Non-response
    - Post-stratification to population totals

    **Result:** Our estimates represent the entire U.S. population, not just survey participants.
    """)

with tab3:
    st.markdown("### 3. Uncertainty Communication")
    st.markdown("""
    **Why this matters:** All survey estimates have uncertainty. Honest communication of uncertainty
    helps prevent over-confidence in specific numbers.

    **What we do:**
    - Show **95% confidence intervals** on all estimates (error bars on charts)
    - Use **plain language** to explain what uncertainty means
    - Flag estimates with **small sample sizes** (less reliable)
    - Explain **sources of uncertainty** (sampling variability, design effects)

    **How to interpret confidence intervals:**
    - The "true" population value likely falls within this range 95% of the time
    - Wider intervals = more uncertainty (smaller sample or more variability)
    - Non-overlapping intervals suggest meaningful differences
    """)

with tab4:
    st.markdown("### 4. Professional Design")
    st.markdown("""
    **Why this matters:** Good design helps communicate information clearly and reduces
    misinterpretation.

    **What we do:**
    - Use **colorblind-friendly** color palettes (accessible to all users)
    - Provide **consistent formatting** across all visualizations
    - Include **clear labels** and **units** on all axes
    - Add **contextual help** (hover tooltips, expandable info boxes)
    - Use **appropriate chart types** for each data type
    """)

with tab5:
    st.markdown("### 5. Reproducibility")
    st.markdown("""
    **Why this matters:** If others can reproduce your results, it builds confidence that the
    findings are real and not errors.

    **What we do:**
    - Provide **all analysis code** on GitHub
    - Document **software versions** (Python 3.11, specific package versions)
    - Use **publicly available data** (anyone can download and verify)
    - Include **step-by-step instructions** for data processing

    **GitHub Repository:**
    - 📂 [BIME533_Proj](https://github.com/yourusername/BIME533_Proj) *(will be public after deployment)*
    - Includes: data processing scripts, analysis code, dashboard source, and report

    **Software Used:**
    - Python 3.11
    - pandas 2.1.4 (data manipulation)
    - pyreadstat 1.2.5 (reading NHANES .XPT files)
    - statsmodels 0.14.1 (survey-weighted analysis)
    - streamlit 1.29.0 (dashboard)
    - plotly 5.18.0 (interactive visualizations)
    """)

with tab6:
    st.markdown("### 6. Appropriate Use Guidance")
    st.markdown("""
    **Why this matters:** Data can be misused or misinterpreted. Clear guidance helps users
    apply findings appropriately.

    **What we do:**
    - State **intended audience** clearly (public health program coordinators)
    - Provide **limitations** of the data (see section below)
    - Warn against **causal interpretations** (cross-sectional data)
    - Specify **appropriate use cases** (identifying disparities, priority setting)
    - Note **inappropriate uses** (individual-level predictions, causal inference)
    """)

# =============================================================================
# DATA INTEGRATION
# =============================================================================
st.markdown("---")
st.markdown("## 🔗 Data Integration Process")

st.markdown("""
**Question from Professor:** "How will you integrate these two data sources (oral health outcome
data and demographic/socioeconomic data) in the dashboard?"

**Answer:**
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    ### Integration Method

    1. **Common Identifier:**
       - Both datasets share a unique participant ID: **SEQN** (Respondent Sequence Number)
       - This allows us to link demographic information to oral health outcomes

    2. **Merge Type:**
       - **Left join** with demographics as the base
       - Keep only participants who completed dental examinations
       - Reason: Oral health analyses require exam data

    3. **Sample Sizes:**
       - Demographics file: **10,537 participants**
       - Oral health exam file: **8,189 participants** (77.7% of total)
       - Final merged dataset: **8,189 participants** with both demographic and oral health data

    4. **Missing Data:**
       - Not all participants had dental exams (mobile exam center participation)
       - Some variables have additional missingness (e.g., decay assessment requires full exam)
       - We handle missing data through **complete-case analysis** for each outcome
    """)

with col2:
    st.markdown("""
    ### Data Flow Diagram

    ```
    ┌─────────────────────────────┐
    │  DEMO_F.XPT                 │
    │  Demographics Data          │
    │  n = 10,537 participants    │
    │                             │
    │  Variables:                 │
    │  - SEQN (ID)                │
    │  - Age, Gender, Race        │
    │  - Education, Income        │
    │  - Survey Weights           │
    │  - Strata, PSUs             │
    └──────────┬──────────────────┘
               │
               │  Merge on SEQN
               │  (Left Join)
               ▼
    ┌─────────────────────────────┐
    │  OHXDEN_F.XPT               │
    │  Oral Health Exam Data      │
    │  n = 8,189 participants     │
    │                             │
    │  Variables:                 │
    │  - SEQN (ID)                │
    │  - Tooth counts (OHXxxTC)   │
    │  - Decay (OHXDECAY)         │
    │  - Restorations (OHXREST)   │
    └──────────┬──────────────────┘
               │
               ▼
    ┌─────────────────────────────┐
    │  Merged Analysis Dataset    │
    │  n = 8,189 participants     │
    │                             │
    │  Derived Variables:         │
    │  - total_teeth              │
    │  - has_untreated_decay      │
    │  - edentulous               │
    │  - Age groups, categories   │
    └─────────────────────────────┘
    ```
    """)

st.markdown("""
### Survey Weight Selection

**Important:** Different analyses require different survey weights:

- **Oral health outcomes:** Use **WTMEC2YR** (MEC exam weight)
  - Reason: Only participants who attended the Mobile Examination Center have oral health data
  - This weight accounts for non-response to the MEC exam
- **Demographics only:** Would use **WTINT2YR** (interview weight)
  - Not used in this dashboard since all outcomes require exam data

**Why this matters:** Using incorrect weights would produce biased estimates. We carefully
select the appropriate weight for each analysis.
""")

# =============================================================================
# ABOUT NHANES
# =============================================================================
st.markdown("---")
st.markdown("## 📊 About NHANES")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Survey Design

    **NHANES (National Health and Nutrition Examination Survey)** is a continuous,
    nationally representative survey conducted by the CDC.

    **Key features:**
    - **Population:** Civilian, non-institutionalized U.S. population
    - **Design:** Complex, multi-stage probability sample
    - **Components:**
      - Household interview (demographics, health history)
      - Physical examination (health measurements, specimens)
      - Dental examination (oral health assessment)
    - **Sample size (2009-2010):** 10,537 participants surveyed; 8,189 examined
    """)

    st.markdown("""
    ### Why NHANES?

    NHANES is considered the "gold standard" for national health surveillance because:
    - ✅ **Nationally representative** (generalizable to U.S. population)
    - ✅ **Rigorous methods** (standardized protocols, quality control)
    - ✅ **Comprehensive data** (extensive demographic, health, and examination data)
    - ✅ **Public access** (free, open data for research and public health)
    - ✅ **Long history** (enables trend analysis across decades)
    """)

with col2:
    st.markdown("""
    ### Oral Health Examination

    **What was measured:**
    - **Tooth count:** Number of permanent teeth present
    - **Dental caries:** Presence of untreated tooth decay
    - **Restorations:** Fillings, crowns, and other dental work
    - **Periodontal disease:** Gum health (not included in this dashboard)

    **Who was examined:**
    - All participants aged 2 years and older
    - Conducted in Mobile Examination Centers
    - Performed by licensed dentists
    - Standardized protocols across all sites
    """)

    st.markdown("""
    ### Sample Characteristics (2009-2010)

    **Age distribution:**
    - Under 20: 38.5%
    - 20-34: 6.1%
    - 35-49: 19.6%
    - 50-64: 18.1%
    - 65+: 17.8%

    **Race/Ethnicity:**
    - Non-Hispanic White: 43.3%
    - Mexican American: 21.3%
    - Non-Hispanic Black: 18.8%
    - Other Hispanic: 10.7%
    - Other Race: 5.9%
    """)

# =============================================================================
# STATISTICAL METHODS
# =============================================================================
st.markdown("---")
st.markdown("## 📐 Statistical Methods")

st.markdown("""
All analyses account for NHANES's complex survey design. Here's what that means in practice:
""")

with st.expander("📊 How We Calculate Prevalence (Binary Outcomes)", expanded=False):
    st.markdown("""
    **For outcomes like "has untreated decay" (yes/no):**

    1. **Weighted prevalence** = (sum of weights for those with decay) / (sum of all weights)
       - Not just simple percentage!
       - Accounts for survey design

    2. **Confidence interval:**
       - Calculated using design-adjusted standard errors
       - Accounts for stratification and clustering
       - Wider than simple random sample CIs

    3. **Sample size:**
       - **n** = actual number of participants
       - **n_eff** = effective sample size (accounting for weights)
       - Design effect typically ranges from 1.5-3.0 for NHANES

    **Example:**
    - 532 people have untreated decay out of 3,058 assessed
    - Simple prevalence: 532/3,058 = 17.4%
    - **Weighted prevalence: 17.4%** (similar but accounts for survey design)
    - 95% CI: 15.8% - 19.0% (wider than simple binomial CI)
    """)

with st.expander("📈 How We Calculate Means (Continuous Outcomes)", expanded=False):
    st.markdown("""
    **For outcomes like "number of teeth present":**

    1. **Weighted mean** = (sum of [weight × teeth count]) / (sum of weights)
       - Gives population-representative average

    2. **Confidence interval:**
       - Based on weighted variance
       - Design-adjusted standard errors
       - Accounts for clustering and stratification

    3. **Interpretation:**
       - Represents the average for the entire U.S. population
       - Not just the average of survey participants

    **Example:**
    - College graduates: mean = 23.3 teeth (95% CI: 22.6 - 24.0)
    - Less than HS: mean = 16.1 teeth (95% CI: 15.3 - 16.9)
    - **Difference: 7.2 teeth** - this is substantial and statistically significant
    """)

with st.expander("🔍 Testing for Statistical Significance", expanded=False):
    st.markdown("""
    **How we assess if differences are "real" or just chance:**

    **Visual approach (shown in dashboard):**
    - If 95% confidence intervals **don't overlap**, likely significant difference
    - Not a formal test, but good rule of thumb

    **Formal tests (used in report):**
    - **Chi-square tests** (design-adjusted) for prevalence comparisons
    - **Kruskal-Wallis tests** for mean comparisons across multiple groups
    - **P-value < 0.05** = statistically significant

    **Important note:**
    - Statistical significance ≠ practical importance
    - Small differences can be significant with large samples
    - Large differences might not be significant with small samples
    - We focus on **magnitude of disparity**, not just p-values
    """)

# =============================================================================
# LIMITATIONS
# =============================================================================
st.markdown("---")
st.markdown("## ⚠️ Limitations & Caveats")

st.markdown("""
**Every dataset has limitations. Here's what you should know when using this dashboard:**
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Data Limitations

    **1. Data Age**
    - Data from **2009-2010** (over 15 years old)
    - Oral health patterns may have changed since then
    - Affordable Care Act (2010) expanded dental coverage for children
    - Use for **understanding disparities**, not current absolute rates

    **2. Cross-Sectional Design**
    - Data collected at one point in time
    - **Cannot determine causation**
    - Can show associations, not cause-and-effect
    - Example: Lower education associated with fewer teeth, but we can't say education
      *causes* tooth loss (could be confounded by income, access, etc.)

    **3. Missing Data**
    - Not all participants had dental exams (77.7% did)
    - Some oral health variables only assessed for subset
    - Decay assessment: 3,058 participants (37% of total)
    - Could introduce bias if missingness related to outcomes
    """)

with col2:
    st.markdown("""
    ### Methodological Limitations

    **1. Simplified Survey Design Adjustment**
    - We use survey weights but simplified variance estimation
    - Proper analysis would use Taylor linearization with full design variables
    - Our confidence intervals are conservative approximations
    - Estimates are unbiased, but CIs may be slightly wide

    **2. Multiple Comparisons**
    - Testing many groups increases chance of false positives
    - We don't adjust for multiple testing
    - Focus on consistent patterns, not isolated differences

    **3. Generalizability**
    - Represents **U.S. civilian, non-institutionalized** population
    - Excludes: military, institutionalized, homeless
    - May not apply to specific local populations
    """)

st.markdown("""
### Appropriate Use Cases

**✅ Good uses for this dashboard:**
- Identifying which demographic groups have worse oral health outcomes
- Understanding the magnitude of oral health disparities
- Supporting grant applications with evidence of disparities
- Prioritizing populations for intervention programs
- Educating stakeholders about oral health equity issues

**❌ Inappropriate uses:**
- Predicting individual oral health outcomes
- Making causal claims (e.g., "education causes better oral health")
- Estimating current (2026) prevalence rates
- Fine-grained local or state-level estimates
- Clinical decision-making for individual patients
""")

# =============================================================================
# HOW TO INTERPRET RESULTS
# =============================================================================
st.markdown("---")
st.markdown("## 📖 How to Interpret Results")

tab1, tab2, tab3 = st.tabs([
    "Reading Charts",
    "Understanding Uncertainty",
    "Assessing Disparities"
])

with tab1:
    st.markdown("""
    ### Reading Bar Charts

    **Basic elements:**
    - **Height of bar** = prevalence (for binary outcomes) or mean (for continuous outcomes)
    - **Error bars** = 95% confidence interval (range of uncertainty)
    - **Axis labels** = tell you what is being measured and the units

    **How to compare groups:**
    1. Look at bar heights - higher = worse for disease outcomes, better for teeth count
    2. Check if error bars overlap - non-overlapping suggests significant difference
    3. Calculate the difference - is it meaningful in practical terms?

    **Example interpretation:**
    - "Mexican Americans have 21.4% prevalence of untreated decay (95% CI: 18.6% - 24.3%)
      compared to Non-Hispanic Whites at 11.6% (95% CI: 9.4% - 13.7%). This 9.8 percentage
      point difference is both statistically significant (non-overlapping CIs) and
      practically important (1.8x higher prevalence)."
    """)

with tab2:
    st.markdown("""
    ### Understanding Uncertainty

    **What is a 95% confidence interval?**
    - If we repeated the survey many times, 95% of the time the true population value
      would fall within this interval
    - **NOT** the range where 95% of people fall
    - **IS** our uncertainty about the population average

    **Wide vs. narrow intervals:**
    - **Narrow CI** = more precision (larger sample size, less variability)
    - **Wide CI** = less precision (smaller sample size, more variability)

    **Using CIs for comparison:**
    - **Overlapping CIs:** Difference might not be significant
    - **Non-overlapping CIs:** Difference is likely significant (>95% confidence)
    - **Close but not overlapping:** Conduct formal statistical test

    **Why account for survey design?**
    - NHANES doesn't sample everyone equally
    - Some people represent more of the population (via weights)
    - Some observations are clustered (same clinic, same neighborhood)
    - Design-adjusted CIs are typically 1.5-3x wider than naïve CIs
    """)

with tab3:
    st.markdown("""
    ### Assessing Disparities

    **Two ways to measure disparities:**

    **1. Absolute Difference**
    - Subtract one group's rate from another
    - Example: 26.0% - 18.1% = 7.9 percentage points
    - **Best for:** Public health burden, number of people affected

    **2. Relative Ratio**
    - Divide one group's rate by another
    - Example: 26.0% / 18.1% = 1.4x higher
    - **Best for:** Comparing magnitude across different outcomes

    **Choosing a reference group:**
    - Often the most advantaged group (e.g., highest education, above poverty)
    - Or the group with best outcomes
    - Be consistent within a project

    **What's a meaningful disparity?**
    - No universal threshold
    - Consider: magnitude, statistical significance, consistency, and public health impact
    - Healthy People 2030 aims to eliminate disparities (all groups equal)
    """)

# Footer
st.markdown("---")
st.markdown("""
### 📚 Additional Resources

- [NHANES Survey Methods and Analytic Guidelines](https://wwwn.cdc.gov/nchs/nhanes/analyticguidelines.aspx)
- [Oral Health Disparities (CDC)](https://www.cdc.gov/oral-health/health-equity/index.html)
- [Healthy People 2030: Oral Conditions](https://health.gov/healthypeople/objectives-and-data/browse-objectives/oral-conditions)
- [Dashboard Design Principles](https://www.cdc.gov/surveillance-data-governance/data-stories/index.html)
""")

st.markdown("""
---
### Questions About Methods?

Contact the project team or consult the full technical report for detailed methodology.
""")
