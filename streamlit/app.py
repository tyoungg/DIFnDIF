"""Main Streamlit application."""

import streamlit as st
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import load_processed_data

st.set_page_config(page_title="DIFnDIF", layout="wide")

st.title("DIFnDIF - Financial Analysis Dashboard")

st.markdown("""
Welcome to the DIFnDIF financial data analysis platform.

**Data Pipeline Status:**
- This is a read-only viewer for processed financial data
- Data ingestion runs separately to generate parquet files
- Check `data/processed/` for available datasets
""")

# Example: Check for master panel
master_panel = load_processed_data("master_panel.parquet")

if master_panel is not None:
    st.success("✓ Master panel data loaded")
    st.write(f"Shape: {master_panel.shape[0]} rows × {master_panel.shape[1]} columns")
    st.dataframe(master_panel.head())
else:
    st.info("No processed data available yet. Run the data pipeline to generate datasets.")
