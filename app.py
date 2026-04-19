"""
Main Streamlit app for a reusable FRED dashboard.

This file follows the same overall structure as your example project.
Most customization should happen in config.py, not here.

Beginner note:
- Think of app.py as the "main dashboard screen"
- Think of config.py as the "settings and topic choices"
- Think of the src/ folder as the "behind the scenes helpers"
"""

import pandas as pd
import streamlit as st

# Import ALL project settings from config.py
from config import *

# Import helper functions from the src folder
from src.data_loader import load_fred_data
from src.analysis import build_regression_table, compute_summary_metrics, build_regime_comparison
from src.visuals import (
    plot_time_series,
    plot_multi_line_chart,
    plot_correlation_heatmap,
    plot_scatter_with_trendline,
)

# -----------------------------------------------------------------------------
# PAGE SETUP
# -----------------------------------------------------------------------------
# This controls the browser tab title and the overall page layout.
# You usually do NOT need to edit this unless you want a different layout.

st.set_page_config(
    page_title=PROJECT_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def rename_columns_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw FRED series IDs into nice labels for charts and tables.

    Example:
    UNRATE -> Unemployment Rate
    CPIAUCSL -> Consumer Price Index
    """
    rename_map = {series_id: label for series_id, label in SERIES.items()}
    rename_map[RECESSION_SERIES_ID] = RECESSION_SERIES_LABEL
    return df.rename(columns=rename_map)


@st.cache_data
def get_data() -> pd.DataFrame:
    """
    Load the target series plus all supporting series.

    - TARGET_VARIABLE is the main thing you are studying
    - SERIES contains all the variables you want in the dashboard
    - RECESSION_SERIES_ID is added for recession shading on charts
    """
    main_series = {
        "id": TARGET_VARIABLE,
        "label": SERIES[TARGET_VARIABLE]
    }

    supporting_series = [
        {"id": sid, "label": label}
        for sid, label in SERIES.items()
        if sid != TARGET_VARIABLE
    ]

    # Add recession indicator for historical context
    supporting_series.append({
        "id": RECESSION_SERIES_ID,
        "label": RECESSION_SERIES_LABEL
    })

    return load_fred_data(main_series, supporting_series, start_date=START_DATE, target_frequency=TARGET_FREQUENCY)

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------

raw_df = get_data()

if raw_df is None or raw_df.empty:
    st.error("No data loaded. Check your FRED API key, internet connection, and series IDs.")
    st.stop()

# Rename technical column names into human-readable display names.
df = rename_columns_for_display(raw_df.copy())

# Make sure the date column is a real datetime column
df["date"] = pd.to_datetime(df["date"])

# These labels are used in the rest of the app
target_label = SERIES[TARGET_VARIABLE]
feature_labels = [SERIES[sid] for sid in MODEL_FEATURES]
recession_label = RECESSION_SERIES_LABEL

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------------------------------

st.sidebar.title("Dashboard Controls")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

start_date = st.sidebar.date_input(
    "Start date",
    value=max(pd.to_datetime(START_DATE).date(), min_date),
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

show_recessions = st.sidebar.checkbox("Show recession shading", value=True)

scatter_x = st.sidebar.selectbox(
    "Scatterplot x-axis",
    options=feature_labels,
    index=0
)

# Apply date filtering
filtered_df = df[
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
].copy()

if filtered_df.empty:
    st.warning("No data is available for the selected date range.")
    st.stop()

# -----------------------------------------------------------------------------
# OPTIONAL DEBUG BLOCK
# -----------------------------------------------------------------------------
# Turn this on only if you are troubleshooting missing values or blank charts.
# When you are ready for expo or final submission, set SHOW_DEBUG_TABLES = False
# in config.py so this section does not appear.

if SHOW_DEBUG_TABLES:
    st.write("Preview of filtered data")
    st.dataframe(filtered_df.head(20))

    st.write("Missing values by column")
    st.write(filtered_df.isna().sum())

    st.write("Column names")
    st.write(filtered_df.columns.tolist())

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------

st.title(PROJECT_TITLE)
st.subheader(PROJECT_SUBTITLE)
st.caption(PROJECT_TAGLINE)

st.markdown(f"## {SECTION_TITLES['overview']}")
st.markdown(INTRO_PARAGRAPH)

st.markdown("### Research Question")
st.write(RESEARCH_QUESTION)

with st.expander("Project summary and data description"):
    st.write(EXECUTIVE_SUMMARY)
    st.write(DATASET_DESCRIPTION)

# -----------------------------------------------------------------------------
# METRIC CARDS
# -----------------------------------------------------------------------------
# These top cards summarize the target variable.

summary = compute_summary_metrics(filtered_df[target_label])

col1, col2, col3, col4 = st.columns(4)
col1.metric(PRIMARY_METRIC_LABEL, summary["latest"])
col2.metric(SECONDARY_METRIC_LABEL, summary["average"])
col3.metric(LOW_METRIC_LABEL, summary["minimum"])
col4.metric(HIGH_METRIC_LABEL, summary["maximum"])

# -----------------------------------------------------------------------------
# MAIN TIME SERIES
# -----------------------------------------------------------------------------

st.markdown(f"## {SECTION_TITLES['main_chart']}")

fig_main = plot_time_series(
    df=filtered_df,
    y_col=target_label,
    title=target_label,
    recession_col=recession_label if show_recessions else None,
    add_zero_line=ADD_ZERO_LINE_TO_MAIN_CHART
)
st.plotly_chart(fig_main, use_container_width=True)

# -----------------------------------------------------------------------------
# COMPARISON GROUPS
# -----------------------------------------------------------------------------
# app.py loops through CHART_GROUPS from config.py.
# This is why you usually customize config.py and not app.py.

st.markdown(f"## {SECTION_TITLES['comparison_groups']}")

for _group_key, group_info in CHART_GROUPS.items():
    st.markdown(f"### {group_info['title']}")

    # Turn FRED IDs into nice labels
    display_cols = [SERIES[sid] for sid in group_info["series_ids"] if sid in SERIES]

    if group_info["chart_type"] == "line":
        fig_group = plot_multi_line_chart(
            df=filtered_df,
            y_cols=display_cols,
            title=group_info["title"],
            recession_col=recession_label if show_recessions else None
        )
        st.plotly_chart(fig_group, use_container_width=True)

    st.markdown(group_info["description"])

# -----------------------------------------------------------------------------
# CORRELATION HEATMAP
# -----------------------------------------------------------------------------

st.markdown(f"## {SECTION_TITLES['correlation']}")

corr_cols = [target_label] + feature_labels
corr_df = filtered_df[corr_cols].dropna()

if len(corr_df) >= 3:
    fig_corr = plot_correlation_heatmap(
        df=corr_df,
        title="Correlation Heatmap"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("Not enough complete observations to calculate correlations.")

# -----------------------------------------------------------------------------
# SCATTERPLOT EXPLORER
# -----------------------------------------------------------------------------

st.markdown(f"## {SECTION_TITLES['scatter']}")

scatter_df = filtered_df[[scatter_x, target_label]].dropna()

if len(scatter_df) >= 3:
    fig_scatter = plot_scatter_with_trendline(
        df=scatter_df,
        x_col=scatter_x,
        y_col=target_label,
        title=f"{target_label} vs {scatter_x}"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("Not enough data for the scatterplot in the selected range.")

# -----------------------------------------------------------------------------
# MODELING SECTION
# -----------------------------------------------------------------------------
# This section uses a simple linear regression model.
# Beginner note:
# - This is regression, not logistic regression
# - Use this when your target variable is a number, not a category

st.markdown(f"## {SECTION_TITLES['modeling']}")
st.markdown(METHODS_PARAGRAPH)

coef_df, metrics = build_regression_table(
    df=filtered_df,
    target_col=target_label,
    feature_cols=feature_labels,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
)

if coef_df is not None:
    left, right = st.columns([2, 1])

    with left:
        st.markdown("**Feature importance (sorted by magnitude of standardized coefficient)**")
        st.dataframe(coef_df, use_container_width=True, hide_index=True)
        st.caption(
            "Standardized coefficients let you compare predictors on equal footing. "
            "The feature with the largest absolute standardized coefficient has the "
            "strongest linear relationship with vehicle sales, holding the others constant."
        )

    with right:
        st.metric("Test R²", f"{metrics['test_r2']:.3f}")
        st.metric("Test MAE", f"{metrics['test_mae']:.3f}",
                  help="Mean absolute error on held-out data, in millions of vehicles.")
        st.metric("Train R²", f"{metrics['train_r2']:.3f}")
        st.caption(f"Train: {metrics['n_train']} obs • Test: {metrics['n_test']} obs")
else:
    st.info("Not enough complete observations to fit the baseline model.")


# -----------------------------------------------------------------------------
# REGIME ANALYSIS
# -----------------------------------------------------------------------------
# Splits data into positive vs. negative YoY vehicle sales growth and fits
# the same model separately on each regime. If feature importance shifts
# between regimes, that's evidence for the executive summary's claim.

st.markdown("## Regime Analysis: Does Feature Importance Shift?")
st.markdown(
    "The same linear regression is fit separately on months when vehicle "
    "sales were growing year-over-year versus months when they were "
    "contracting. If the standardized coefficient ranking reshuffles between "
    "regimes, the relationship between predictors and vehicle sales is "
    "regime-dependent — meaning no single model tells the whole story."
)

regime_results = build_regime_comparison(
    df=filtered_df,
    target_col=target_label,
    feature_cols=feature_labels,
    periods=12,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
)

regime_cols = st.columns(2)

regime_labels = [
    ("positive", "Expansion (Positive YoY Growth)", regime_cols[0]),
    ("negative", "Contraction (Negative YoY Growth)", regime_cols[1]),
]

for key, label, col in regime_labels:
    with col:
        st.markdown(f"### {label}")
        result = regime_results[key]
        if result["coef_df"] is not None:
            st.dataframe(result["coef_df"], use_container_width=True, hide_index=True)
            sub1, sub2 = st.columns(2)
            sub1.metric("Test R²", f"{result['metrics']['test_r2']:.3f}")
            sub2.metric("Test MAE", f"{result['metrics']['test_mae']:.3f}")
            st.caption(f"{result['n_obs']} observations in this regime")
        else:
            st.info(
                f"Not enough observations in the {label.lower()} regime "
                "to fit a model on the selected date range."
            )

st.caption(
    "Compare the top feature (largest absolute standardized coefficient) in "
    "each column. If they differ — or if the sign flips — the predictors "
    "matter differently depending on whether the auto market is expanding "
    "or contracting."
)

# -----------------------------------------------------------------------------
# CONCLUSION
# -----------------------------------------------------------------------------

st.markdown(f"## {SECTION_TITLES['conclusion']}")
st.markdown(FINDINGS_PARAGRAPH)
st.info(TEAM_NOTES)

# -----------------------------------------------------------------------------
# DOWNLOAD BUTTON
# -----------------------------------------------------------------------------

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered dataset",
    data=csv_data,
    file_name="fred_dashboard_filtered_data.csv",
    mime="text/csv"
)
