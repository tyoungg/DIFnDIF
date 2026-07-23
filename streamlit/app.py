"""Main Streamlit application."""
import streamlit as st
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px

# Add root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils.data_loader import load_processed_data

st.set_page_config(page_title="DIFnDIF", layout="wide")

st.title("DIFnDIF - Financial Analysis Dashboard")

st.markdown("""
Welcome to the DIFnDIF financial data analysis platform.
**Data Pipeline Status:**
- 🟢 This is a read-only viewer for processed financial data.
- ⚙️ Data ingestion runs separately to generate parquet files.
- 📂 Check `data/processed/` for available datasets.
""")

# Load Data
master_panel = load_processed_data("master_panel.parquet")

if master_panel is not None:
    st.success("✓ Master panel data loaded")

    # --- Sidebar Navigation ---
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Data Overview", "Data Quality", "Returns Analysis"])

    if page == "Data Overview":
        st.subheader("Master Panel Explorer")
        st.write(f"Dataset Dimensions: **{master_panel.shape[0]} rows × {master_panel.shape[1]} columns**")

        # Allow user to filter by ticker in the viewer
        tickers = master_panel['ticker'].unique()
        selected_ticker = st.selectbox("Filter by Ticker", options=tickers)
        filtered_df = master_panel[master_panel['ticker'] == selected_ticker]

        st.dataframe(filtered_df, use_container_width=True)

    elif page == "Data Quality":
        st.subheader("Data Health Check")

        # Calculate missing values percentage
        null_counts = master_panel.isnull().mean() * 100
        null_df = pd.DataFrame({"Variable": null_counts.index, "Missing %": null_counts.values})

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("Missing Data Percentage")
            st.table(null_df)

        with col2:
            # Visualizing missingness
            fig_nulls = px.bar(null_df, x="Variable", y="Missing %",
                               title="Missingness by Variable",
                               color="Missing %", color_continuous_scale="Viridis")
            st.plotly_chart(fig_nulls, use_container_width=True)

    elif page == "Returns Analysis":
        st.subheader("Monthly Returns Visualization")

        tickers = master_panel['ticker'].unique()
        selected_tickers = st.multiselect("Select Tickers to Compare", options=tickers, default=tickers[:3])

        if selected_tickers:
            plot_df = master_panel[master_panel['ticker'].isin(selected_tickers)]

            # Plotting Cumulative Returns for a better visual of performance
            # Cumulative Return = (1 + r).cumprod()
            plot_df = plot_df.sort_values(['ticker', 'date'])
            plot_df['cum_return'] = plot_df.groupby('ticker')['return'].transform(lambda x: (1 + x).cumprod())

            fig_returns = px.line(plot_df, x='date', y='cum_return', color='ticker',
                                  title="Cumulative Returns Over Time",
                                  labels={'cum_return': 'Growth of $1', 'date': 'Date'})
            st.plotly_chart(fig_returns, use_container_width=True)
        else:
            st.warning("Please select at least one ticker to visualize.")

else:
    st.info("No processed data available yet. Please run `python main.py` to generate the datasets.")
