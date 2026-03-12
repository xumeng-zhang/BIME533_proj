"""
Interactive Data Exploration Page
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parents[2] / 'src'))
from survey_analysis import weighted_prevalence, weighted_mean

st.set_page_config(page_title="Explore Data", page_icon="🔍", layout="wide")

st.title("🔍 Interactive Data Exploration")

st.markdown("""
Use the controls below to explore oral health disparities across different demographic
groups. All estimates are survey-weighted and include 95% confidence intervals.
""")

# Load data
@st.cache_data
def load_data():
    data_path = Path(__file__).parents[2] / 'data' / 'processed' / 'nhanes_merged.csv'
    return pd.read_csv(data_path)

try:
    data = load_data()

    # Sidebar controls
    st.sidebar.header("🎯 Customize Your Analysis")

    st.sidebar.markdown("### Select Outcome")
    outcome = st.sidebar.selectbox(
        "Oral Health Outcome",
        options=[
            'has_untreated_decay',
            'edentulous',
            'total_teeth',
            'has_restorations'
        ],
        format_func=lambda x: {
            'has_untreated_decay': 'Untreated Tooth Decay',
            'edentulous': 'Complete Tooth Loss (Edentulism)',
            'total_teeth': 'Average Number of Teeth Present',
            'has_restorations': 'Dental Restorations'
        }[x],
        help="Choose which oral health outcome to analyze"
    )

    st.sidebar.markdown("### Select Demographics")
    demographic = st.sidebar.selectbox(
        "Demographic Variable",
        options=[
            'race_ethnicity',
            'age_group',
            'education',
            'poverty_category',
            'gender'
        ],
        format_func=lambda x: {
            'race_ethnicity': 'Race/Ethnicity',
            'age_group': 'Age Group',
            'education': 'Education Level',
            'poverty_category': 'Poverty Level',
            'gender': 'Gender'
        }[x],
        help="Choose which demographic variable to compare across"
    )

    st.sidebar.markdown("### Display Options")
    show_ci = st.sidebar.checkbox(
        "Show confidence intervals",
        value=True,
        help="Display 95% confidence intervals as error bars"
    )

    show_sample_sizes = st.sidebar.checkbox(
        "Show sample sizes",
        value=True,
        help="Display the number of participants in each group"
    )

    # Determine if binary or continuous outcome
    is_binary = outcome in ['has_untreated_decay', 'edentulous', 'has_restorations']

    # Calculate statistics
    with st.spinner('Calculating survey-weighted statistics...'):
        if is_binary:
            stats_df = weighted_prevalence(data, outcome, demographic)
            y_col = 'prevalence'
            y_label = 'Prevalence (%)'
        else:
            stats_df = weighted_mean(data, outcome, demographic)
            y_col = 'mean'
            y_label = 'Mean Number of Teeth'

    # Main content area
    st.markdown(f"## Results: {outcome.replace('_', ' ').title()} by {demographic.replace('_', ' ').title()}")

    # Create interactive plot
    fig = go.Figure()

    # Add bars
    fig.add_trace(go.Bar(
        x=stats_df['group'],
        y=stats_df[y_col],
        marker_color='steelblue',
        marker_line_color='darkblue',
        marker_line_width=1.5,
        text=[f"{val:.1f}" for val in stats_df[y_col]],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                      y_label + ': %{y:.1f}<br>' +
                      'Sample size: %{customdata}<br>' +
                      '<extra></extra>',
        customdata=stats_df['n']
    ))

    # Add error bars if requested
    if show_ci:
        fig.add_trace(go.Scatter(
            x=stats_df['group'],
            y=stats_df[y_col],
            error_y=dict(
                type='data',
                array=stats_df['ci_upper'] - stats_df[y_col],
                arrayminus=stats_df[y_col] - stats_df['ci_lower'],
                color='black',
                thickness=2,
                width=6
            ),
            mode='markers',
            marker=dict(size=0),
            showlegend=False,
            hoverinfo='skip'
        ))

    # Update layout
    fig.update_layout(
        xaxis_title=demographic.replace('_', ' ').title(),
        yaxis_title=y_label,
        height=500,
        hovermode='x unified',
        showlegend=False,
        template='plotly_white',
        margin=dict(t=50, b=100, l=60, r=40)
    )

    # Add reference line for full dentition if showing teeth count
    if outcome == 'total_teeth':
        fig.add_hline(
            y=28,
            line_dash="dash",
            line_color="gray",
            annotation_text="Full dentition (28 teeth)",
            annotation_position="right"
        )

    st.plotly_chart(fig, use_container_width=True)

    # Summary statistics table
    st.markdown("### 📊 Summary Statistics")

    if show_sample_sizes:
        if is_binary:
            display_df = stats_df[['group', 'prevalence', 'ci_lower', 'ci_upper', 'n']].copy()
            display_df.columns = ['Group', 'Prevalence (%)', '95% CI Lower', '95% CI Upper', 'Sample Size']
        else:
            display_df = stats_df[['group', 'mean', 'ci_lower', 'ci_upper', 'n']].copy()
            display_df.columns = ['Group', 'Mean', '95% CI Lower', '95% CI Upper', 'Sample Size']

        # Format numbers
        for col in display_df.columns[1:4]:
            display_df[col] = display_df[col].round(1)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        if is_binary:
            display_df = stats_df[['group', 'prevalence', 'ci_lower', 'ci_upper']].copy()
            display_df.columns = ['Group', 'Prevalence (%)', '95% CI Lower', '95% CI Upper']
        else:
            display_df = stats_df[['group', 'mean', 'ci_lower', 'ci_upper']].copy()
            display_df.columns = ['Group', 'Mean', '95% CI Lower', '95% CI Upper']

        for col in display_df.columns[1:]:
            display_df[col] = display_df[col].round(1)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    # Interpretation section
    st.markdown("### 💡 Interpretation")

    col1, col2 = st.columns(2)

    with col1:
        max_idx = stats_df[y_col].idxmax()
        max_group = stats_df.loc[max_idx, 'group']
        max_val = stats_df.loc[max_idx, y_col]

        if is_binary:
            st.metric(
                "Highest Prevalence",
                f"{max_group}",
                f"{max_val:.1f}%"
            )
        else:
            st.metric(
                "Highest Mean",
                f"{max_group}",
                f"{max_val:.1f} teeth"
            )

    with col2:
        min_idx = stats_df[y_col].idxmin()
        min_group = stats_df.loc[min_idx, 'group']
        min_val = stats_df.loc[min_idx, y_col]

        if is_binary:
            st.metric(
                "Lowest Prevalence",
                f"{min_group}",
                f"{min_val:.1f}%"
            )
        else:
            st.metric(
                "Lowest Mean",
                f"{min_group}",
                f"{min_val:.1f} teeth"
            )

    # Disparity magnitude
    st.markdown("#### Disparity Magnitude")
    abs_diff = abs(max_val - min_val)
    rel_ratio = max_val / min_val if min_val > 0 else float('inf')

    if is_binary:
        st.write(f"- **Absolute difference:** {abs_diff:.1f} percentage points")
        st.write(f"- **Relative ratio:** {rel_ratio:.2f}x (highest vs. lowest)")
    else:
        st.write(f"- **Absolute difference:** {abs_diff:.1f} teeth")
        st.write(f"- **Relative ratio:** {rel_ratio:.2f}x (highest vs. lowest)")

    # Statistical significance note
    st.info("""
    ### Understanding Confidence Intervals

    The error bars show 95% confidence intervals. When intervals for two groups don't overlap,
    this suggests a statistically significant difference (though not a definitive test).
    All estimates account for NHANES's complex survey design.
    """)

    # Download section
    st.markdown("---")
    st.markdown("### ⬇️ Download Data")

    col1, col2 = st.columns(2)

    with col1:
        # Download CSV
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"{outcome}_by_{demographic}.csv",
            mime="text/csv"
        )

    with col2:
        # Download figure data (not the image itself, but could add that)
        st.markdown("""
        ### Download Chart

        **Tip:** Right-click on the chart above and select "Download plot as a png"
        to save the visualization.
        """)

except FileNotFoundError:
    st.error("""
    **Data file not found!**

    Please run the data processing pipeline first:
    ```bash
    python src/data_processing.py
    ```
    """)
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.exception(e)

# Help section in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### ℹ️ Help")
    with st.expander("How to use this page"):
        st.markdown("""
        1. **Select an outcome** from the dropdown (e.g., untreated decay)
        2. **Choose a demographic variable** to compare (e.g., race/ethnicity)
        3. **View the interactive chart** - hover for details
        4. **Read the interpretation** below the chart
        5. **Download the data** if needed for reports

        **Tip:** Try different combinations to explore various disparities!
        """)

    with st.expander("What are confidence intervals?"):
        st.markdown("""
        **Confidence intervals (CI)** show the range where we expect the true population
        value to fall 95% of the time.

        - **Wider intervals** = more uncertainty (smaller sample size or more variability)
        - **Narrower intervals** = more precision (larger sample size)
        - **Non-overlapping intervals** suggest statistically significant differences

        All our estimates account for NHANES's complex sampling design, which affects the
        width of confidence intervals.
        """)
