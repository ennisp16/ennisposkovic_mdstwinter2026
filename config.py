"""
Project configuration for a reusable FRED dashboard.

THIS IS THE MAIN FILE YOU CUSTOMIZE.

Beginner note:
Most project changes should happen here, not in app.py.
"""

# -----------------------------------------------------------------------------
# PROJECT IDENTITY
# -----------------------------------------------------------------------------
# These values control the title and the top text in the dashboard.

PROJECT_TITLE = "Driving Demand"
PROJECT_SUBTITLE = "Predicting U.S. Light Vehicle Sales Through Consumer Financial Conditions and Energy Costs"
PROJECT_TAGLINE = "What moves metal off the lot — wages, income, or gas prices?"

# Main research question shown near the top of the dashboard
RESEARCH_QUESTION = """
To what extent can U.S. light vehicle sales be predicted by consumer financial conditions 
and energy costs? Additionally, which factor among wage growth, real disposable income, 
and fuel prices has the strongest predictive power across different economic regimes?
"""

EXECUTIVE_SUMMARY = (
    "Automobile purchases represent one of the largest discretionary expenditures for "
    "American households, making light vehicle sales a powerful barometer of consumer "
    "economic health. Yet the decision to buy a car is not driven by any single factor — "
    "it emerges from a complex interplay of household income dynamics and everyday cost "
    "pressures. This project investigates whether U.S. total light vehicle sales can be "
    "effectively predicted using three macroeconomic indicators sourced from the Federal "
    "Reserve Economic Data (FRED) database: average hourly earnings, real disposable "
    "personal income, and regular gasoline prices. Using machine learning techniques "
    "applied to historical monthly data, the analysis pursues two objectives. First, it "
    "evaluates the predictive accuracy of models trained on these features, comparing "
    "approaches to identify which best captures the nonlinear and potentially "
    "regime-dependent relationships between the predictors and vehicle sales. Second, it "
    "leverages feature importance analysis to determine which economic forces exert the "
    "greatest influence on auto demand — and whether that hierarchy shifts between periods "
    "of expansion and contraction. The findings aim to offer insight not only into the "
    "mechanics of consumer durable goods demand, but also into the broader question of how "
    "households weigh competing financial signals when making major purchasing decisions."
)

DATASET_DESCRIPTION = (
    "This project uses four time series from the Federal Reserve Economic Data (FRED) "
    "database. The target variable is Total Vehicle Sales (TOTALSA), reported as a "
    "seasonally adjusted annual rate in millions of units. The three predictor variables "
    "are Average Hourly Earnings of All Private Employees (CES0500000003), which tracks "
    "nominal wage trends; Real Disposable Personal Income (DSPIC96), which measures "
    "inflation-adjusted income available to households after taxes; and U.S. Regular All "
    "Formulations Retail Gasoline Prices (GASREGW), which captures fuel cost pressure on "
    "consumers. These series were chosen because they represent distinct channels through "
    "which economic conditions influence big-ticket purchasing decisions — what people earn, "
    "what they can actually spend, and what they pay to drive."
)

# -----------------------------------------------------------------------------
# SERIES SETUP
# -----------------------------------------------------------------------------
# VERY IMPORTANT:
# - The LEFT side must be real FRED series IDs
# - The RIGHT side is the nice label shown in charts and tables
#
# Replace the example series below with your own topic.

SERIES = {
    "TOTALSA": "Total Vehicle Sales",
    "CES0500000003": "Average Hourly Earnings",
    "GASREGW": "Gas Prices",
    "DSPIC96": "Real Disposable Personal Income",
}

# Optional recession indicator used for gray shaded regions on charts
RECESSION_SERIES_ID = "USREC"
RECESSION_SERIES_LABEL = "U.S. Recession Indicator"

# Start date for pulling data from FRED
# Change this if your series starts later and you want to avoid many missing values
START_DATE = "2006-04-01"

# Choose the final dashboard frequency
# Use:
# "A" for annual
# "Q" for quarterly
# "M" for monthly
TARGET_FREQUENCY = "M"

# If True, app.py will show debug tables for missing values and column names
# Set this to False before final presentation
SHOW_DEBUG_TABLES = False

# If True, the main chart will draw a horizontal zero line
# This is useful for variables like deficits, growth rates, or net change
ADD_ZERO_LINE_TO_MAIN_CHART = True

# -----------------------------------------------------------------------------
# METRIC CARDS
# -----------------------------------------------------------------------------
# These labels control the 4 metric cards at the top of the dashboard.

PRIMARY_METRIC_LABEL = "Latest Monthly Vehicle Sales (Millions)"
SECONDARY_METRIC_LABEL = "Average Monthly Vehicle Sales (Millions)"
LOW_METRIC_LABEL = "Lowest Monthly Vehicle Sales (Millions)"
HIGH_METRIC_LABEL = "Highest Monthly Vehicle Sales (Millions)"

# -----------------------------------------------------------------------------
# ANALYSIS TARGET AND MODEL FEATURES
# -----------------------------------------------------------------------------
# TARGET_VARIABLE must match one of the keys inside SERIES.
# MODEL_FEATURES should be a list of supporting variables that help explain the target.

TARGET_VARIABLE = "TOTALSA"

MODEL_FEATURES = [
    "CES0500000003",
    "DSPIC96",
    "GASREGW",
]

# -----------------------------------------------------------------------------
# OPTIONAL SETTINGS
# -----------------------------------------------------------------------------

TEST_SIZE = 0.2
RANDOM_STATE = 42

# -----------------------------------------------------------------------------
# NARRATIVE TEXT BLOCKS
# -----------------------------------------------------------------------------
# These appear in the dashboard as polished explanation text.

INTRO_PARAGRAPH = (
    "Every month, millions of Americans make one of the biggest purchases of their "
    "lives: a new vehicle. Total U.S. vehicle sales reflect far more than consumer "
    "preference — they signal how confident households feel about their financial "
    "situation. This dashboard explores whether three key economic indicators — average "
    "hourly earnings, real disposable personal income, and regular gasoline prices — can "
    "help explain and predict shifts in national vehicle sales. Understanding these "
    "relationships matters because auto sales ripple through the entire economy, from "
    "manufacturing and logistics to lending and insurance."
)

METHODS_PARAGRAPH = (
    "All data is sourced from the Federal Reserve Economic Data (FRED) database, which "
    "provides publicly available, regularly updated macroeconomic time series. The four "
    "series — Total Vehicle Sales (TOTALSA), Average Hourly Earnings (CES0500000003), "
    "Real Disposable Personal Income (DSPIC96), and Regular Gasoline Prices (GASREGW) — "
    "are aligned to a common monthly frequency and merged by date. After handling missing "
    "values and ensuring consistent time coverage, the dashboard visualizes each variable's "
    "trend over time and its correlation with vehicle sales. A baseline linear regression "
    "model is then trained on the three predictor variables to forecast vehicle sales, with "
    "performance evaluated using standard metrics like R-squared and mean absolute error."
)

FINDINGS_PARAGRAPH = (
    "The baseline linear regression achieves a test R² of just 0.076 and a mean "
    "absolute error of 1.63 million vehicles on held-out data — weak predictive "
    "performance that empirically confirms the concern raised in the executive "
    "summary: consumer auto demand is not well-described by a simple linear "
    "combination of these three predictors. Real disposable personal income "
    "emerges as the dominant signal in the pooled model (standardized coefficient "
    "of +2.06), while average hourly earnings carries a large negative "
    "standardized coefficient of -1.38. That negative sign should not be read "
    "as a genuine inverse relationship — wages and disposable income are highly "
    "correlated, so when both enter the regression together, the model tends to "
    "split a single underlying effect into opposing coefficients. Gas prices, by "
    "contrast, show essentially no independent effect in the pooled model "
    "(standardized coefficient of -0.03). The regime analysis provides the "
    "sharpest evidence that a single model cannot tell the whole story. During "
    "expansion months (positive year-over-year sales growth, n=132), the model "
    "achieves a modest test R² of 0.267. During contraction months (n=97), test "
    "R² falls to -0.07 — worse than simply predicting the mean — and the raw "
    "coefficient on gas prices flips sign from strongly negative during "
    "expansions to slightly positive during contractions. Taken together, these "
    "results suggest that macroeconomic fundamentals offer some linear signal "
    "when the auto market is growing, but the relationship breaks down during "
    "downturns, where structural shocks like the 2008 financial crisis and "
    "COVID-19 introduce nonlinearities that linear regression cannot "
    "accommodate. A natural next step would be to test tree-based or "
    "regime-switching models that can handle these structural breaks directly."
)

TEAM_NOTES = (
    "The most instructive part of this project is what the model gets wrong. "
    "The linear regression works passably during expansions but fails outright "
    "during contractions, and the sign flip on gas prices between regimes is a "
    "clear signal that the underlying relationship is not stable. For a "
    "presentation, the regime comparison is the key slide — it shows that "
    "choosing the right model matters as much as choosing the right features."
)
# -----------------------------------------------------------------------------
# SECTION TITLES
# -----------------------------------------------------------------------------

SECTION_TITLES = {
    "overview": "Project Overview",
    "main_chart": "Main Time Series",
    "comparison_groups": "Comparative Views",
    "correlation": "Correlation Analysis",
    "scatter": "Scatterplot Explorer",
    "modeling": "Baseline Modeling",
    "conclusion": "Key Takeaways",
}

# -----------------------------------------------------------------------------
# CHART GROUPS
# -----------------------------------------------------------------------------
# This is how you control the extra comparison charts without editing app.py.
#
# Each group has:
# - title: section title in the dashboard
# - description: explanation below the chart
# - chart_type: keep "line" for now
# - series_ids: list of FRED IDs from SERIES that should appear in that chart

CHART_GROUPS = {
    "group_1": {
        "title": "Earnings & Income vs. Vehicle Sales",
        "description": (
            "This chart overlays average hourly earnings and real disposable "
            "personal income against vehicle sales over time. Both measures "
            "capture household purchasing power, but from different angles — "
            "earnings reflect what workers take home per hour, while disposable "
            "income accounts for taxes, transfers, and inflation. Watching how "
            "these diverge or converge with sales reveals whether rising wages "
            "actually translate into big-ticket purchases."
        ),
        "chart_type": "line",
        "series_ids": ["CES0500000003", "DSPIC96"],
    },
    "group_2": {
        "title": "Gas Prices vs. Vehicle Sales",
        "description": (
            "This chart tracks regular gasoline prices alongside vehicle sales. "
            "Fuel costs act as both a direct expense and a psychological signal "
            "for consumers weighing a new vehicle purchase. Spikes in gas prices "
            "can suppress demand outright or shift buyers toward smaller, more "
            "fuel-efficient models — either way, the relationship is rarely as "
            "simple as 'gas goes up, sales go down.'"
        ),
        "chart_type": "line",
        "series_ids": ["GASREGW"],
    },
}

# -----------------------------------------------------------------------------
# SERIES DESCRIPTIONS
# -----------------------------------------------------------------------------
# Helpful for documentation, your README, or future expanders/tooltips.

SERIES_DESCRIPTIONS = {
    "TOTALSA": "Total vehicle sales in millions of units, seasonally adjusted annual rate. This is the target variable the model aims to predict.",
    "CES0500000003": "Average hourly earnings of all private employees in dollars, reflecting wage trends and household purchasing power.",
    "DSPIC96": "Real disposable personal income in billions of chained 2017 dollars, measuring inflation-adjusted income available after taxes.",
    "GASREGW": "U.S. regular all-formulations retail gasoline prices in dollars per gallon, capturing everyday energy cost pressure on consumers.",
    "USREC": "U.S. recession indicator used for chart shading.",
}
