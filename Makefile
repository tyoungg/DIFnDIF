.PHONY: install download-data build-panel notebooks streamlit test clean help

help:
	@echo "Market Structure Lab - Index Inclusion Research Platform"
	@echo ""
	@echo "Using: yfinance (free, no credentials required)"
	@echo ""
	@echo "Available commands:"
	@echo "  make install            Install package in development mode"
	@echo "  make download-data      Download prices and fundamentals from yfinance"
	@echo "  make build-panel        Build master_panel.parquet from raw data"
	@echo "  make data               Download + build (full pipeline)"
	@echo "  make notebooks          Launch Jupyter Lab"
	@echo "  make streamlit          Launch Streamlit dashboard"
	@echo "  make test               Run pytest suite"
	@echo "  make clean              Remove __pycache__ and .pyc files"
	@echo ""

install:
	pip install -e ".[dev]"

download-data:
	@echo "Downloading price and fundamental data from yfinance..."
	python src/ingestion/data_downloader.py

build-panel: download-data
	@echo "Building master panel..."
	python src/panels/build_master.py
	@echo "✓ Master panel ready at data/processed/master_panel.parquet"

data: download-data build-panel
	@echo "✓ Data pipeline complete!"

notebooks:
	jupyter lab

streamlit:
	streamlit run streamlit/app.py

test:
	pytest tests/ -v --cov=src

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
