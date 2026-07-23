# Market Structure Lab

A reproducible research platform for studying the causal effects of index inclusion on firm valuation, returns, and fundamentals.

**Status:** Switching from WRDS to yfinance for accessibility. You can now run this without institutional credentials!

## Research Question

**How much of the long-run valuation change associated with S&P 500 inclusion is explained by improvements in operating fundamentals versus changes in market demand?**

Secondary question: Has this relationship changed as passive investing has grown as a share of the market?

## Why This Matters

Index inclusion is a quasi-natural experiment. When a firm enters the S&P 500:
- Its float expands (more passive capital flows in)
- Its fundamentals may improve (increased scrutiny, better corporate governance)
- Its valuation may increase (passive demand, reduced cost of capital)

By separating these effects, we can ask: *Is the inclusion premium real economic value, or passive demand?*

## Quick Start (5 minutes)

### Prerequisites

- Python 3.9+
- No special credentials required (yfinance is free!)

### Installation

```bash
# Clone
git clone https://github.com/tyoungg/DIFnDIF.git
cd DIFnDIF

# Install
pip install -e .
```

### Download Data & Build Panel

```bash
# Download prices and fundamentals (takes ~2 min)
make download-data

# Build master panel
make build-panel

# Or do both at once
make data
```

### Launch Streamlit Dashboard

```bash
make streamlit
```

Open `http://localhost:8501`

## Project Architecture

```
market_structure_lab/
├── data/
│   ├── raw/
│   │   ├── prices/                 # Monthly adjusted close from yfinance
│   │   └── fundamentals/           # Quarterly fundamentals from yfinance
│   │
│   ├── processed/
│   │   └── master_panel.parquet    # Single source of truth
│   │
│   └── metadata/
│       └── reference.py            # Ticker list, variable dictionary
│
├── src/
│   ├── ingestion/
│   │   └── data_downloader.py      # yfinance wrapper
│   │
│   ├── panels/
│   │   └── build_master.py         # merge_asof (prevents look-ahead bias)
│   │
│   ├── analysis/                   # DiD, matching, robustness (coming soon)
│   │   ├── did/
│   │   ├── matching/
│   │   └── robustness/
│   │
│   ├── utils/
│   │   ├── config.py               # Paths and parameters
│   │   ├── constants.py            # Research definitions
│   │   └── data_loader.py          # Load master panel
│   │
│   └── __init__.py
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_descriptive_stats.ipynb
│   └── 03_event_study.ipynb
│
├── streamlit/
│   └── app.py
│
└── Makefile
```

## Data Pipeline

### Phase 1: Download (yfinance)

**Prices:** Monthly adjusted close (2015–present)
- Columns: date, ticker, adj_close, return

**Fundamentals:** Quarterly balance sheet & income statement
- Columns: date, ticker, revenue, net income, cash flow, etc.

```bash
python src/ingestion/data_downloader.py
```

### Phase 2: Master Panel

Merge prices with fundamentals using **merge_asof**:
- Prevents look-ahead bias
- Each monthly return matched to most recent quarterly report
- Result: one observation per ticker per month

```bash
python src/panels/build_master.py
```

**Output:** `data/processed/master_panel.parquet`

Example:

| ticker | date       | adj_close | return | Total Revenue | ... |
|--------|------------|-----------|--------|---------------|-----|
| AAPL   | 2023-01-31 | 145.43    | 0.025  | 394328000000  | ... |
| AAPL   | 2023-02-28 | 151.94    | 0.045  | 394328000000  | ... |
| MSFT   | 2023-01-31 | 232.01    | 0.010  | 198252000000  | ... |

## Key Technical Details

### merge_asof: Preventing Look-Ahead Bias

```python
master_panel = pd.merge_asof(
    prices,
    fundamentals,
    on='date',
    by='ticker',
    direction='backward',  # Use LAST known quarter
)
```

This is critical for causal inference:
- **Wrong:** Use quarterly report from 2023-Q2 to predict 2023-Q1 price → look-ahead bias
- **Right:** Use 2023-Q1 report (reported in April) to predict Q2 prices → no bias

### Ticker as Primary Key

Unlike WRDS (which uses PERMNO and GVKEY), yfinance uses **ticker symbols**.

**Pros:**
- Free, no credentials needed
- Reproducible (anyone can run it)
- Good enough for Streamlit and academic exploration

**Cons:**
- Ticker symbols change (rare but possible)
- For a publication-quality paper, consider adding PERMNO via separate crosswalk

## Running the Full Pipeline

```bash
# 1. Install
pip install -e .

# 2. Download data (first time takes ~2-3 min)
make download-data

# 3. Build panel
make build-panel

# 4. Explore in Streamlit
make streamlit

# 5. Run analysis in Jupyter (coming soon)
make notebooks
```

## Dependencies

- **Data:** yfinance (free Yahoo Finance API)
- **Analysis:** pandas, numpy, scipy, scikit-learn, statsmodels, linearmodels, did
- **Visualization:** streamlit, plotly
- **Development:** pytest, jupyter, black, ruff

See `pyproject.toml` for full list.

## Next Steps (Coming Soon)

- [ ] Event study plotting
- [ ] DiD analysis (Callaway & Sant'Anna)
- [ ] Matching algorithms
- [ ] Robustness checks (placebo, alternative estimators)
- [ ] Passive premium analysis
- [ ] Interactive Streamlit pages

## Important Notes

⚠️ **Data is not committed to Git**

- All `.csv` and `.parquet` files are in `.gitignore`
- Data is reproducible from yfinance
- Same analysis, fresh data each run

✅ **Reproducible research design**

- No institutional credentials needed
- Anyone can clone and run
- All code is version-controlled
- Data pipeline is fully documented

## Contributing

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes
git add src/ notebooks/

# Commit
git commit -m "description"

# Push
git push origin feature/your-feature
```

## References

- **merge_asof technique:** [Pandas Documentation](https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html)
- **DiD with staggered adoption:** Callaway & Sant'Anna (2021)
- **yfinance:** [GitHub](https://github.com/ranaroussi/yfinance)

## License

MIT

---

**Last Updated:** July 2026  
**Data Source:** yfinance (Yahoo Finance)  
**Status:** Active development
