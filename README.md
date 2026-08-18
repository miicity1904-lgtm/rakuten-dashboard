# rakuten-dashboard
A modular Streamlit dashboard for real-time analysis of Rakuten Ichiba marketplace data

Project Overview
This project implements a modular Streamlit dashboard designed to retrieve, clean, and visualise real‑time marketplace data from the Rakuten Ichiba API. The dashboard helps users—especially foreign buyers and resellers—analyse pricing patterns, review behaviour, and shop activity across different product keywords.

The system was developed as part of my MSc Computer Science dissertation at Queen Mary University of London under the supervision of Dr. Sofia Bakogianni.
project-root/
│
├── src/
│   ├── api_client.py          # Handles API requests, pagination, timeouts
│   ├── data_cleaning.py       # Schema-based cleaning pipeline
│   ├── filters.py             # Keyword, price, and review filters
│   ├── metrics.py             # New vs sold classification, summary metrics
│   └── utils.py               # Helper functions, caching, formatting
│
├── dashboard/
│   ├── app.py                 # Main Streamlit application
│   ├── pages/
│   │   ├── overview.py        # Overview page with metrics and listings
│   │   ├── trends.py          # Visualisations and descriptive summaries
│   │   └── listings.py        # Latest listings with images and details
│   └── components/            # Reusable UI components
│
├── data/
│   └── sample_responses/      # Example API JSON responses for testing
│
├── requirements.txt           # Python dependencies
└── README.md                  # This file

To run the dashboard locally, install the required Python packages:
pip install -r requirements.txt
This project uses Streamlit, Plotly, Requests, and standard Python libraries.


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
