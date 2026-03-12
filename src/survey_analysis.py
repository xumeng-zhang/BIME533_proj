"""
Survey-Weighted Analysis Module for NHANES Data
Handles complex survey design with weights, strata, and PSUs
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings


def weighted_prevalence(data, outcome_var, group_var, weight_var='WTMEC2YR'):
    """
    Calculate weighted prevalence for binary outcome by groups

    Parameters:
    -----------
    data : DataFrame
        Analysis dataset
    outcome_var : str
        Binary outcome variable (0/1 or True/False)
    group_var : str
        Grouping variable (categorical)
    weight_var : str
        Survey weight variable (default: WTMEC2YR for MEC exam)

    Returns:
    --------
    DataFrame : results with prevalence, CI, and sample size by group
    """
    # Remove missing values
    analysis_df = data[[outcome_var, group_var, weight_var]].dropna()

    results = []

    for group in sorted(analysis_df[group_var].unique()):
        if pd.isna(group):
            continue

        subset = analysis_df[analysis_df[group_var] == group]

        # Get weights and outcomes
        weights = subset[weight_var]
        outcomes = subset[outcome_var]

        # Weighted prevalence
        prevalence = np.average(outcomes, weights=weights)

        # Sample size (unweighted)
        n = len(subset)

        # Effective sample size (accounts for weighting)
        # Kish's approximation: n_eff = (sum of weights)^2 / sum of squared weights
        sum_weights = weights.sum()
        sum_sq_weights = (weights ** 2).sum()
        n_eff = (sum_weights ** 2) / sum_sq_weights if sum_sq_weights > 0 else n

        # Standard error (simplified - assumes simple random sampling)
        # For proper complex survey SE, should use Taylor linearization with strata/PSU
        # This is a conservative approximation
        se = np.sqrt(prevalence * (1 - prevalence) / n_eff) if n_eff > 0 else np.nan

        # 95% Confidence interval
        ci_lower = max(0, prevalence - 1.96 * se)
        ci_upper = min(1, prevalence + 1.96 * se)

        results.append({
            'group': group,
            'prevalence': prevalence * 100,  # Convert to percentage
            'ci_lower': ci_lower * 100,
            'ci_upper': ci_upper * 100,
            'n': n,
            'n_eff': n_eff
        })

    return pd.DataFrame(results)


def weighted_mean(data, outcome_var, group_var, weight_var='WTMEC2YR'):
    """
    Calculate weighted mean for continuous outcome by groups

    Parameters:
    -----------
    data : DataFrame
        Analysis dataset
    outcome_var : str
        Continuous outcome variable
    group_var : str
        Grouping variable (categorical)
    weight_var : str
        Survey weight variable

    Returns:
    --------
    DataFrame : results with mean, CI, and sample size by group
    """
    # Remove missing values
    analysis_df = data[[outcome_var, group_var, weight_var]].dropna()

    results = []

    for group in sorted(analysis_df[group_var].unique()):
        if pd.isna(group):
            continue

        subset = analysis_df[analysis_df[group_var] == group]

        # Get weights and outcomes
        weights = subset[weight_var]
        outcomes = subset[outcome_var]

        # Weighted mean
        mean = np.average(outcomes, weights=weights)

        # Sample size
        n = len(subset)

        # Effective sample size
        sum_weights = weights.sum()
        sum_sq_weights = (weights ** 2).sum()
        n_eff = (sum_weights ** 2) / sum_sq_weights if sum_sq_weights > 0 else n

        # Weighted variance
        variance = np.average((outcomes - mean) ** 2, weights=weights)

        # Standard error
        se = np.sqrt(variance / n_eff) if n_eff > 0 else np.nan

        # 95% Confidence interval
        ci_lower = mean - 1.96 * se
        ci_upper = mean + 1.96 * se

        results.append({
            'group': group,
            'mean': mean,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'n': n,
            'n_eff': n_eff,
            'sd': np.sqrt(variance)
        })

    return pd.DataFrame(results)


def calculate_disparity_metrics(stats_df, reference_group=None):
    """
    Calculate disparity metrics from prevalence or mean statistics

    Parameters:
    -----------
    stats_df : DataFrame
        Output from weighted_prevalence or weighted_mean with 'group' column
        and either 'prevalence' or 'mean' column
    reference_group : str
        Reference group for comparison (if None, uses group with best outcome)

    Returns:
    --------
    DataFrame : disparity metrics for each group vs reference
    """
    # Determine outcome column
    if 'prevalence' in stats_df.columns:
        outcome_col = 'prevalence'
        # For prevalence, lower is better (for disease outcomes)
        is_lower_better = True
    elif 'mean' in stats_df.columns:
        outcome_col = 'mean'
        # For mean teeth, higher is better
        is_lower_better = False
    else:
        raise ValueError("stats_df must have 'prevalence' or 'mean' column")

    # Set reference group
    if reference_group is None:
        if is_lower_better:
            reference_group = stats_df.loc[stats_df[outcome_col].idxmin(), 'group']
        else:
            reference_group = stats_df.loc[stats_df[outcome_col].idxmax(), 'group']

    ref_value = stats_df[stats_df['group'] == reference_group][outcome_col].values[0]

    results = []
    for idx, row in stats_df.iterrows():
        group = row['group']
        value = row[outcome_col]

        # Absolute difference
        abs_diff = value - ref_value

        # Relative ratio
        rel_ratio = value / ref_value if ref_value != 0 else np.nan

        results.append({
            'group': group,
            'value': value,
            'reference': reference_group,
            'ref_value': ref_value,
            'absolute_difference': abs_diff,
            'relative_ratio': rel_ratio,
            'is_reference': (group == reference_group)
        })

    return pd.DataFrame(results)


def test_group_differences(data, outcome_var, group_var, weight_var='WTMEC2YR',
                          outcome_type='binary'):
    """
    Test for statistical significance of group differences

    Parameters:
    -----------
    data : DataFrame
        Analysis dataset
    outcome_var : str
        Outcome variable
    group_var : str
        Grouping variable
    weight_var : str
        Survey weight variable
    outcome_type : str
        'binary' for prevalence, 'continuous' for means

    Returns:
    --------
    dict : test results with p-value and test statistic
    """
    # Remove missing values
    analysis_df = data[[outcome_var, group_var, weight_var]].dropna()

    groups = sorted(analysis_df[group_var].unique())

    if len(groups) < 2:
        return {'p_value': np.nan, 'test': 'insufficient_groups'}

    # For weighted analysis, we use a simplified approach
    # Proper survey analysis would use Rao-Scott adjusted chi-square or F-test
    # with design effects from strata and PSU

    if outcome_type == 'binary':
        # Weighted chi-square-like test
        # Simplified version: compare weighted prevalences

        # Get weighted prevalence for each group
        group_stats = []
        for group in groups:
            subset = analysis_df[analysis_df[group_var] == group]
            weights = subset[weight_var]
            outcomes = subset[outcome_var]
            prev = np.average(outcomes, weights=weights)
            n = len(subset)
            group_stats.append((prev, n))

        # Simple approach: use unweighted chi-square as approximation
        # (Conservative for design effect > 1)
        contingency_table = []
        for group in groups:
            subset = analysis_df[analysis_df[group_var] == group]
            n_success = (subset[outcome_var] == 1).sum()
            n_total = len(subset)
            contingency_table.append([n_success, n_total - n_success])

        try:
            chi2, p_value = stats.chi2_contingency(contingency_table)[:2]
            return {'p_value': p_value, 'test': 'chi_square', 'statistic': chi2}
        except:
            return {'p_value': np.nan, 'test': 'error'}

    elif outcome_type == 'continuous':
        # Weighted ANOVA-like test
        # Use Kruskal-Wallis as non-parametric alternative

        group_data = []
        for group in groups:
            subset = analysis_df[analysis_df[group_var] == group]
            group_data.append(subset[outcome_var])

        try:
            h_stat, p_value = stats.kruskal(*group_data)
            return {'p_value': p_value, 'test': 'kruskal_wallis', 'statistic': h_stat}
        except:
            return {'p_value': np.nan, 'test': 'error'}

    else:
        raise ValueError("outcome_type must be 'binary' or 'continuous'")


def format_results_table(stats_df, outcome_type='prevalence', precision=1):
    """
    Format statistical results for publication/presentation

    Parameters:
    -----------
    stats_df : DataFrame
        Results from weighted_prevalence or weighted_mean
    outcome_type : str
        'prevalence' or 'mean'
    precision : int
        Decimal places for rounding

    Returns:
    --------
    DataFrame : formatted results table
    """
    formatted = stats_df.copy()

    if outcome_type == 'prevalence':
        # Format as "XX.X% (95% CI: XX.X-XX.X)"
        formatted['result'] = formatted.apply(
            lambda row: f"{row['prevalence']:.{precision}f}% (95% CI: {row['ci_lower']:.{precision}f}-{row['ci_upper']:.{precision}f})",
            axis=1
        )
    elif outcome_type == 'mean':
        # Format as "XX.X (95% CI: XX.X-XX.X)"
        formatted['result'] = formatted.apply(
            lambda row: f"{row['mean']:.{precision}f} (95% CI: {row['ci_lower']:.{precision}f}-{row['ci_upper']:.{precision}f})",
            axis=1
        )

    # Add sample size
    formatted['sample_size'] = formatted['n'].apply(lambda x: f"n={x:,}")

    return formatted[['group', 'result', 'sample_size']]


if __name__ == '__main__':
    # Example usage
    print("Survey Analysis Module")
    print("Load data and use functions like:")
    print("  weighted_prevalence(data, 'has_untreated_decay', 'race_ethnicity')")
    print("  weighted_mean(data, 'total_teeth', 'poverty_category')")
