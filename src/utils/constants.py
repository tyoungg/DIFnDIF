"""Research constants and parameters."""

# Index definitions
INDICES = {
    "SP500": {
        "name": "S&P 500",
        "description": "Large-cap index",
    },
    "RUSSELL1000": {
        "name": "Russell 1000",
        "description": "Large-cap index",
    },
    "NASDAQ100": {
        "name": "Nasdaq 100",
        "description": "Tech-heavy large-cap index",
    },
}

# Matching variables (for propensity score or covariate matching)
MATCHING_VARS = [
    "log_market_cap",
    "revenue_growth",
    "ebitda_margin",
    "roic",
    "leverage",
    "momentum",
    "volatility",
    "beta",
]

# Outcome variables
OUTCOMES = {
    "valuation": [
        "pe_ratio",
        "pb_ratio",
        "ev_sales",
        "price_to_sales",
    ],
    "performance": [
        "return",
        "abnormal_return",
        "cumulative_return",
        "buy_hold_abnormal_return",
    ],
    "fundamentals": [
        "revenue",
        "revenue_growth",
        "ebitda",
        "ebitda_margin",
        "operating_margin",
        "eps",
        "eps_growth",
        "roic",
        "roe",
        "fcf",
        "fcf_growth",
    ],
}

# Time periods for heterogeneity analysis
DECADES = {
    "1990s": (1990, 1999),
    "2000s": (2000, 2009),
    "2010s": (2010, 2019),
    "2020s": (2020, 2024),
}

# Passive investing eras (based on market share of passive investing)
PASSIVE_ERAS = {
    "Pre-Passive": (0.00, 0.15),
    "Early Growth": (0.15, 0.30),
    "Acceleration": (0.30, 0.45),
    "Mature Passive": (0.45, 1.00),
}

# Industries (GICS)
GICS_SECTORS = {
    10: "Energy",
    15: "Materials",
    20: "Industrials",
    25: "Consumer Discretionary",
    30: "Consumer Staples",
    35: "Health Care",
    40: "Financials",
    45: "Information Technology",
    50: "Communication Services",
    55: "Utilities",
    60: "Real Estate",
}

# Firm size categories (by market cap)
SIZE_CATEGORIES = {
    "Large": (1_000_000_000, float('inf')),
    "Medium": (300_000_000, 1_000_000_000),
    "Small": (100_000_000, 300_000_000),
}
