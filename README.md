# NHANES Oral Health Disparities Dashboard

An interactive public health informatics dashboard visualizing oral health disparities across demographic and socioeconomic groups using NHANES 2009-2010 data.

**BIME 533 Final Project** | University of Washington | March 2026

## Project Overview

This project presents an interactive dashboard that helps public health program coordinators explore disparities in oral health outcomes across different population groups in the United States. Using data from the National Health and Nutrition Examination Survey (NHANES) 2009-2010, the dashboard reveals significant differences in oral health by race/ethnicity, education level, income, and age.

### Key Findings

- **1.9x** higher prevalence of untreated tooth decay among Mexican Americans compared to other racial groups
- **7.2 fewer teeth** on average for those with less than high school education vs. college graduates
- **1.4x** higher rate of complete tooth loss for those below poverty line
- **17.4%** of the population has untreated tooth decay; **23.1%** have lost all their teeth

## Dashboard Features

- **Interactive Visualizations**: Explore disparities by different demographic variables
- **Survey-Weighted Analysis**: All estimates account for NHANES's complex sampling design
- **Confidence Intervals**: Uncertainty shown for all estimates
- **Multiple Outcomes**: Untreated decay, tooth loss, average teeth present, restorations
- **Downloadable Data**: Export results for reports and presentations
- **Trustworthy Design**: Transparent methods, clear data sources, appropriate use guidance

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/BIME533_Proj.git
   cd BIME533_Proj
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run data processing** (if not already done)
   ```bash
   python src/data_processing.py
   python generate_analysis.py
   ```

5. **Launch dashboard**
   ```bash
   streamlit run dashboard/app.py
   ```

The dashboard will open in your default web browser at `http://localhost:8501`

## Project Structure

```
BIME533_Proj/
├── data/
│   ├── raw/                      # NHANES .XPT files (not in repo - download separately)
│   │   ├── DEMO_F.XPT
│   │   └── OHXDEN_F.XPT
│   └── processed/
│       └── nhanes_merged.csv     # Analysis-ready dataset
├── src/
│   ├── data_processing.py        # Data loading, merging, cleaning
│   └── survey_analysis.py        # Survey-weighted statistics
├── dashboard/
│   ├── app.py                    # Main landing page
│   └── pages/
│       ├── 1_Overview.py         # Key findings summary
│       ├── 2_Explore_Data.py     # Interactive exploration
│       └── 3_Methodology.py      # Methods and trustworthiness
├── results/
│   ├── figures/                  # Publication-quality plots
│   └── key_findings.txt          # Summary of main results
├── docs/
│   └── final_report.md           # Written report (3-5 pages)
├── requirements.txt              # Python dependencies
├── generate_analysis.py          # Generate figures and findings
└── README.md                     # This file
```

## Data Sources

**National Health and Nutrition Examination Survey (NHANES) 2009-2010**

- **Demographics**: [DEMO_F](https://wwwn.cdc.gov/Nchs/Nhanes/2009-2010/DEMO_F.htm)
- **Oral Health**: [OHXDEN_F](https://wwwn.cdc.gov/Nchs/Nhanes/2009-2010/OHXDEN_F.htm)
- **Overview**: [NHANES 2009-2010](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/overview.aspx?BeginYear=2009)

### Downloading Data Files

Data files are not included in this repository due to size. Download them automatically:

```bash
python download_data.py
```

Or manually:
1. Visit [NHANES 2009-2010 Data Page](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Demographics&CycleBeginYear=2009)
2. Download DEMO_F.xpt and OHXDEN_F.xpt
3. Place in `data/raw/` directory (rename with .XPT extension if needed)

## Methods

### Survey-Weighted Analysis

All analyses account for NHANES's complex survey design:
- **Sample weights** (WTMEC2YR for examination data)
- **Stratification** and **clustering** effects
- **Design-adjusted confidence intervals**

### Statistical Software

- **Python 3.11**
- **pandas** 2.1.4 - data manipulation
- **pyreadstat** 1.2.5 - reading SAS transport files
- **statsmodels** 0.14.1 - survey-weighted statistics
- **matplotlib** 3.8.2 - static visualizations
- **plotly** 5.18.0 - interactive charts
- **streamlit** 1.29.0 - dashboard framework

### Reproducibility

All analysis code is included. To reproduce results:

```bash
# Process data
python src/data_processing.py

# Generate analysis and figures
python generate_analysis.py

# Launch dashboard
streamlit run dashboard/app.py
```

## Documentation

### For Users

- **Dashboard Overview**: See `dashboard/app.py` and visit the deployed dashboard
- **Methodology**: Detailed explanation in dashboard's Methodology page
- **Key Findings**: See `results/key_findings.txt`

### For Developers

- **Data Processing**: Documented in `src/data_processing.py`
- **Analysis Functions**: Documented in `src/survey_analysis.py`
- **Dashboard Components**: Each page in `dashboard/pages/` is self-documented

## 👥 Target Audience

This dashboard is designed for **public health program coordinators** at state and local health departments who:
- Need to identify disparities for program planning
- Support grant applications with evidence
- Prioritize intervention programs
- Have intermediate quantitative literacy (comfortable with percentages, bar charts, confidence intervals)

## Limitations

- **Data Age**: NHANES 2009-2010 (over 15 years old)
- **Cross-Sectional**: Cannot establish causation
- **Missing Data**: Not all participants had full dental examinations
- **Generalizability**: U.S. civilian, non-institutionalized population only

See the dashboard's Methodology page for detailed limitations.


---

**Disclaimer**: This dashboard uses data from 2009-2010 and is intended for educational purposes. Current oral health statistics may differ. Always consult recent data sources for current estimates.
