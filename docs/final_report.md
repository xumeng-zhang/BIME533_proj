# NHANES Oral Health Disparities Dashboard: An Interactive Tool for Exploring Health Inequities

**Xumeng Zhang**
BIME 533 - Public Health Informatics
University of Washington
March 2026

---

## Abstract

Oral health disparities persist across demographic and socioeconomic groups in the United States, but traditional static reports make it difficult for public health practitioners to explore these differences and inform intervention planning. This project developed an interactive dashboard using NHANES 2009-2010 data (N=8,189 with dental examinations) to visualize oral health outcomes across population groups. Survey-weighted analyses revealed significant disparities: Mexican Americans had 1.9 times higher prevalence of untreated tooth decay (21.4%) compared to other racial groups (11.1%); college graduates had 7.2 more teeth (23.3) on average than those with less than high school education (16.1); and individuals below the poverty line had 1.4 times higher rates of complete tooth loss (26.0%) than those above the poverty line (18.1%). The dashboard was designed specifically for public health program coordinators and policy makers with intermediate quantitative skills, and deployed on Streamlit Community Cloud <https://bime533proj-qeaztkfnzapl6urxnuyvbt.streamlit.app/> for easy access without software installation.

---

## 1. Introduction

Oral diseases are among the most common chronic conditions in the United States, profoundly affecting quality of life, nutrition, and overall health. These burdens fall disproportionately on populations with lower income, limited access to dental care, and from certain racial and ethnic minority groups (CDC, 2023). While national surveillance data from the National Health and Nutrition Examination Survey (NHANES) provides comprehensive information on oral health across demographic groups, these data are typically presented in static reports that are difficult for policymakers and public health practitioners to use for program planning and priority setting.

Public health informatics offers an opportunity to address this gap by transforming complex survey data into interactive, accessible visualizations. However, effective dashboards must be carefully designed with specific user needs in mind and built on principles of trustworthiness and transparency.

**Target Users:** This dashboard was designed specifically for **public health program coordinators and policy makers** who need to identify oral health disparities to prioritize interventions, support grant applications, and allocate resources. These users typically have intermediate quantitative skills and need actionable insights rather than raw statistical tables.

**Project Aim:** To develop an interactive dashboard that enables public health practitioners to explore associations between oral health outcomes (untreated tooth decay, tooth loss, dental restorations) and demographic/socioeconomic characteristics (race/ethnicity, education, poverty level, age) using NHANES 2009-2010 data.

---

## 2. Data and Methods

### 2.1 Data Sources and Integration

**NHANES 2009-2010 Overview:**
NHANES is a continuous, nationally representative, cross-sectional survey of the civilian, non-institutionalized U.S. population conducted by the Centers for Disease Control and Prevention (CDC) (NCHS, 2012). The 2009-2010 cycle surveyed 10,537 participants using a complex, multistage probability sampling design with oversampling of certain demographic groups to ensure adequate representation (CDC/NCHS, 2009-2010).

**Data Integration Process:**
This analysis integrated two datasets from the National Health and Nutrition Examination Survey (NHANES). Demographic information (n = 10,537) was obtained from <https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2009/DataFiles/DEMO_F.xpt>, which includes variables such as age, gender, race/ethnicity, education level, income-to-poverty ratio, survey weights (WTMEC2YR, WTINT2YR), and survey design variables (SDMVSTRA, SDMVPSU). Oral health information (n = 8,189) was obtained from <https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2009/DataFiles/OHXDEN_F.xpt> , which contains tooth-level measures including tooth counts, untreated decay, restorations, and sealants. The two datasets were merged using the participant identifier SEQN, resulting in a final analytic dataset of 8,189 participants with both demographic and oral health data.

**Missing Data:** 
Not all participants received full dental assessments; the untreated decay variable (OHXDECAY) was available for 3,058 participants (37% of those examined), primarily adults

**Demographic Variables:**
- Age groups: <20, 20-34, 35-49, 50-64, 65+
- race/ethnicity: NH White, NH Black, Mexican American, Other Hispanic, Other 
- education level: Less than HS, HS/GED, Some college, College graduate
- poverty categories: Below poverty <1.0 PIR, Near poverty 1.0-1.99, Above poverty ≥2.0
  
**Oral health outcomes:** 
- Total teeth present: count of permanent teeth 
- has untreated decay: binary (OHXDECAY=1)
- edentulous: binary (total_teeth=0)
- has restorations: binary (OHXREST=1)

### 2.2 Statistical Analysis

**Survey-Weighted Methods:**
All analyses used survey weights to account for NHANES's complex sampling design. Standard unweighted analyses would produce biased estimates due to oversampling of certain demographic groups. We applied:

- **Sample Weights:** WTMEC2YR (MEC examination weight) for all oral health outcomes, as these require examination data
- **Prevalence Estimation:** For binary outcomes (e.g., has untreated decay), weighted prevalence = Σ(weight × outcome) / Σ(weight)
- **Mean Estimation:** For continuous outcomes (e.g., number of teeth), weighted mean = Σ(weight × value) / Σ(weight)
<!-- - **Confidence Intervals:** Calculated using design-adjusted standard errors accounting for stratification and clustering (simplified Taylor linearization approximation with effective sample size correction) -->

**Software:** 
- Python 3.11
- pandas (data manipulation)
- pyreadstat (reading SAS transport files)
- statsmodels (survey-weighted statistics)
- matplotlib and seaborn (static figures)
- plotly (interactive charts)
- streamlit (dashboard framework).

---

## 3. Results

### 3.1 Sample Characteristics

The final analysis dataset included 8,189 participants with dental examination data. The sample was 50% female, 43% Non-Hispanic White, 21% Mexican American, and 19% Non-Hispanic Black. Age distribution ranged from children to elderly, with 39% under age 20. Education levels (adults 20+) ranged from less than high school (29%) to college graduates (21%). Approximately 26% of participants lived below or near the poverty line.

Overall oral health burden was substantial: 17.4% had untreated tooth decay (among the 3,058 assessed for decay), 23.1% had lost all their teeth (edentulous), and the average number of teeth present was 17.5 (out of 28 permanent teeth, excluding wisdom teeth).

### 3.2 Racial/Ethnic Disparities in Untreated Tooth Decay

**Figure 1** shows significant racial/ethnic disparities in untreated tooth decay. Mexican Americans had the highest prevalence at 21.4% (95% CI: 18.6%-24.3%), followed by Non-Hispanic Blacks at 21.0% (95% CI: 17.7%-24.2%). In contrast, Non-Hispanic Whites had 11.6% prevalence (95% CI: 9.4%-13.7%), and Other Hispanic and Other Race groups had similar rates around 11%. This represents a **1.9-fold disparity** between the highest and lowest prevalence groups, translating to an absolute difference of 10.3 percentage points.

These differences were statistically significant, as evidenced by non-overlapping 95% confidence intervals. From a public health perspective, this means that among Mexican Americans who received a dental assessment, more than 1 in 5 had untreated tooth decay—nearly double the rate of other groups.

### 3.3 Education Gradient in Oral Health

**Figure 2** demonstrates a clear education gradient in average number of teeth present. College graduates had a mean of 23.3 teeth (95% CI: 22.6-24.0), compared to 16.1 teeth (95% CI: 15.3-16.9) among those with less than high school education—a difference of **7.2 teeth**, or 25% of full dentition. High school graduates and those with some college fell between these extremes at 17.7 and 19.8 teeth, respectively, showing a dose-response relationship.

This finding highlights the strong association between educational attainment and oral health outcomes. Those with the least education have lost, on average, 12 of their 28 permanent teeth, compared to only 5 teeth lost among college graduates.

### 3.4 Poverty and Complete Tooth Loss

**Figure 3** reveals the relationship between poverty and edentulism (complete tooth loss). Individuals living below the poverty line had a 26.0% prevalence of edentulism (95% CI: 23.6%-28.3%), compared to 18.1% (95% CI: 16.6%-19.7%) among those above the poverty line—a **1.4-fold disparity**. Those near poverty (1.0-1.99 PIR) had an intermediate prevalence of 25.4%.

Complete tooth loss represents the most severe oral health outcome, affecting nutrition, speech, appearance, and quality of life. The finding that more than one quarter of those living in poverty have lost all their teeth underscores the substantial burden in this population.

### 3.5 Age Patterns

**Figure 4** shows that untreated decay prevalence varies by age group. Among those under 20, prevalence was 14.3% (95% CI: 12.8%-15.8%). Age-specific patterns (not shown due to space) revealed that disparities by race/ethnicity and socioeconomic status widened with age, suggesting cumulative disadvantage over the life course.

---

## 4. Discussion

### 4.1 Principal Findings

This project identified substantial and persistent oral health disparities across multiple dimensions of social stratification. Mexican Americans and Non-Hispanic Blacks face nearly twice the burden of untreated tooth decay compared to other groups. Educational attainment shows a strong dose-response relationship with oral health, with each additional level of education associated with better outcomes. Economic disadvantage compounds these disparities, with those in poverty experiencing significantly higher rates of complete tooth loss.

### 4.2 Dashboard Design for Trustworthiness

The dashboard was built with transparency and rigorous uncertainty communication as core design principles.

**Methodological Transparency:**
The dashboard includes a comprehensive Methodology page explaining survey weighting, data integration, confidence interval calculation, and statistical assumptions. We use plain language to explain why survey weights matter and how they affect estimates, making methods accessible to users with intermediate quantitative skills.

**Uncertainty Communication:**
All estimates include 95% confidence intervals displayed as error bars on charts. We provide explanations of what confidence intervals mean (uncertainty about population values, not individual variation) and how to interpret overlapping vs. non-overlapping intervals. Sample sizes are shown to help users gauge precision.


### 4.3 Limitations

**Cross-Sectional Design:** We cannot establish causation. While education is associated with better oral health, this could reflect unmeasured confounding by income, health literacy, access to care, or other factors. Further analysis such as longitudinal study might be needed to disentangle causal pathways.

**Missing Data:** Not all participants received full dental examinations (77.7% did), and the decay assessment (OHXDECAY) was only available for 37% of examined participants. If missingness is related to oral health status, this could introduce bias.

### 4.4 Implications for Public Health Practice

These findings have several actionable implications:

**Targeted Interventions:** Programs should prioritize Mexican American and Non-Hispanic Black communities with culturally tailored outreach, potentially including community health workers, Spanish-language materials, and partnerships with community organizations.

**School-Based Programs:** The education gradient suggests early intervention is critical. Expanding school-based dental sealant programs in low-income schools could reduce disparities before they compound.

**Medicaid Expansion:** High rates of edentulism among those in poverty highlight the need for comprehensive adult dental coverage under Medicaid. Many states provide limited adult dental benefits.

**Life Course Approach:** Widening disparities with age suggest that prevention programs need to reach young adults and middle-aged populations, not just children and seniors.

---

## 5. Conclusion

Oral health disparities in the United States are substantial, patterned by race/ethnicity, education, and economic status. This project demonstrates that public health informatics tools—specifically, well-designed, trustworthy interactive dashboards—can make complex surveillance data more accessible and actionable for public health practitioners. By implementing principles of transparency, appropriate design for target users, and rigorous survey-weighted methods, the NHANES Oral Health Disparities Dashboard provides a model for translating data into practice to advance health equity.

The dashboard is deployed at <https://bime533proj-qeaztkfnzapl6urxnuyvbt.streamlit.app/>.

---

## References

Centers for Disease Control and Prevention (CDC). (2023). Oral Health. <https://www.cdc.gov/oral-health/>

Centers for Disease Control and Prevention, National Center for Health Statistics (CDC/NCHS). (2009-2010). National Health and Nutrition Examination Survey Data. Hyattsville, MD: U.S. Department of Health and Human Services. <https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2009>


---

## AI Use Statement

This project was developed through extensive iterative collaboration with Claude Code, which was used throughout the project to support multiple stages of development. Claude Code assisted with:

- Developing the data processing pipeline, including Python scripts for loading, cleaning, and merging NHANES datasets

- Writing statistical analysis code, such as survey-weighted prevalence and mean calculations

- Implementing the dashboard, including the Streamlit application structure and interactive visualizations

- Supporting report editing, and improving clarity and organization of the written analysis

The development process involved many rounds of interaction with the model, during which generated code and text were carefully reviewed, tested, revised, and refined by Xumeng. All conceptual and analytical decisions, including the idea proposal, dashboard design, analytic approaches, and result interpretation, were made by myself.
---
