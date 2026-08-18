# rakuten-dashboard
A modular Streamlit dashboard for real-time analysis of Rakuten Ichiba marketplace data

Project Overview
This project implements a modular Streamlit dashboard designed to retrieve, clean, and visualise real‑time marketplace data from the Rakuten Ichiba API. The dashboard helps users—especially foreign buyers and resellers—analyse pricing patterns, review behaviour, and shop activity across different product keywords.

README.md — Documentation describing the project, installation steps, and how to run the dashboard.
To run the dashboard locally, install the required Python packages:
pip install -r requirements.txt
This project uses Streamlit, Plotly, Requests, and standard Python libraries.


The system was developed as part of my MSc Computer Science dissertation at Queen Mary University of London under the supervision of Dr. Sofia Bakogianni.
project-root/
│
src — Contains all core backend logic for the dashboard.

api_client.py — Handles API requests, pagination, timeouts, error handling, and caching.

data_cleaning.py — Implements the schema‑based cleaning pipeline that extracts name, price, shop, reviews, brand, condition, and image.

filters.py — Applies keyword filtering, price range filtering, and minimum review thresholds.

metrics.py — Computes summary metrics and classifies listings as “new” or “sold” using the review‑based heuristic.

utils.py — Helper functions for formatting, caching, and shared utilities.

dashboard — Contains the Streamlit user interface.

app.py — The main Streamlit application entry point.

pages — Multi‑page Streamlit structure.

overview.py — Displays metrics, charts, and high‑level marketplace summaries.

trends.py — Shows deeper insights such as shop concentration, review distribution, and price patterns.

listings.py — Renders the latest listings with images, prices, shops, and review counts.

components — Reusable UI components such as cards, layout blocks, and chart wrappers.

data — Contains sample JSON responses for testing.

sample_responses — Example API outputs used when an API key is unavailable.

requirements.txt — Lists all Python dependencies needed to run the dashboard.



Running the Dashboard
After installing dependencies, run:
streamlit run src/app.py

This will launch the dashboard in your browser at:
http://localhost:8501

Executable / Deployment
A fully packaged executable is not provided because the Rakuten API requires a private key that cannot be bundled into a public binary.

However, the dashboard can be run locally using the steps above.

If deployed online (e.g., Streamlit Cloud), the API key must be added as a private environment variable.

Features
Real‑time API ingestion with bounded pagination

Schema‑based cleaning of messy marketplace data

Keyword search, price range filtering, and minimum review filtering

Metrics for new vs sold listings

Interactive Plotly charts (price buckets, review distribution, shop concentration)

Multi‑page Streamlit interface with Overview, Listings, and Trends pages

Lightweight, modular codebase designed for clarity and maintainability
