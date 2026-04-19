[README.md](https://github.com/user-attachments/files/26863691/README.md)
# Driving Demand

**Predicting U.S. Light Vehicle Sales Through Consumer Financial Conditions and Energy Costs**

A Streamlit dashboard that investigates whether U.S. total light vehicle sales can be explained and predicted using three FRED macroeconomic indicators: average hourly earnings, real disposable personal income, and regular gasoline prices.

## Research question

To what extent can U.S. light vehicle sales be predicted by consumer financial conditions and energy costs, and does the importance of each factor shift between economic expansions and contractions?

## Key findings

- A baseline linear regression on the three predictors achieves a test R² of only 0.076 — confirming that the relationship between these macroeconomic variables and vehicle sales is not well-described by a simple linear model.
- Real disposable personal income is the dominant predictor in the pooled model; wages and disposable income show multicollinearity that produces a misleading negative coefficient on hourly earnings.
- The relationship is clearly regime-dependent. During months of positive year-over-year sales growth, the linear model achieves a modest test R² of 0.267. During contraction months, test R² is negative — worse than predicting the mean — and the sign on gas prices flips between regimes.
- The takeaway is that choosing the right *model* matters as much as choosing the right features. Tree-based or regime-switching models would likely handle these structural breaks better than linear regression.

## Data

All series come from the Federal Reserve Economic Data (FRED) database:

| FRED ID | Description |
|---|---|
| `TOTALSA` | Total Vehicle Sales (target, millions of units, SAAR) |
| `CES0500000003` | Average Hourly Earnings, All Private Employees |
| `DSPIC96` | Real Disposable Personal Income |
| `GASREGW` | U.S. Regular Retail Gasoline Prices |
| `USREC` | NBER Recession Indicator (used for chart shading) |

Monthly data from April 2006 onward.

## Project structure

project/
├── app.py                 # Streamlit dashboard
├── config.py              # Project settings (edit this to customize)
├── narrative_blocks.py    # Optional reusable text helpers
├── requirements.txt
├── .env                   # Your FRED API key (not committed)
├── README.md
└── src/
├── data_loader.py     # FRED data fetching and frequency alignment
├── analysis.py        # Summary stats, regression, regime analysis
└── visuals.py         # Plotly chart builders
## Setup

### 1. Create a virtual environment

**Mac / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your FRED API key

Create a file named `.env` in the project root containing:
FRED_API_KEY=your_32_character_key_here
Grab a free key at https://fredaccount.stlouisfed.org/apikeys.

### 4. Run the dashboard
```bash
streamlit run app.py
```

## Dashboard sections

1. **Project Overview** — research question and context
2. **Main Time Series** — total vehicle sales over time with recession shading
3. **Comparative Views** — predictors overlaid against vehicle sales
4. **Correlation Analysis** — heatmap of pairwise correlations
5. **Scatterplot Explorer** — pick any predictor and see its relationship with sales
6. **Baseline Modeling** — linear regression with train/test split, R², MAE, and standardized coefficients
7. **Regime Analysis** — same model fit separately on expansion vs. contraction months
8. **Key Takeaways** — findings and limitations
