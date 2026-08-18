#module for all ui components of my streamlit dashboard (search bar, dark mode, sidebar filters etc)


import streamlit as st

#SEARCH BAR (no dark mode)
def search_and_darkmode():
    col_search = st.columns([1])[0]
    search_query = col_search.text_input(" ", placeholder="🔍 Search products…")
    return search_query


#METRICS ROW
def metric_row(metrics, currency, convert):
    st.markdown("""
        <style>
            .metric-card {
                background-color: #1e1e1e;
                padding: 18px;
                border-radius: 12px;
                border: 1px solid #333;
                text-align: left;
                margin-bottom: 10px;
            }
            .metric-title {
                font-size: 16px;
                color: #bbbbbb;
                margin-bottom: 6px;
            }
            .metric-value {
                font-size: 26px;
                font-weight: 600;
                color: white;
                margin-bottom: 4px;
            }
        </style>
    """, unsafe_allow_html=True)

    #Apply conversion
    converted_avg_new = convert(metrics["avg_new"], currency)
    converted_avg_sold = convert(metrics["avg_sold"], currency)

    symbol = "£" if currency else "¥"

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🆕 New Listings</div>
                <div class="metric-value">{metrics['new']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">💸 Sold Listings</div>
                <div class="metric-value">{metrics['sold']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">📈 Avg. Price (New)</div>
                <div class="metric-value">{symbol}{converted_avg_new:,}</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">📉 Avg. Price (Sold)</div>
                <div class="metric-value">{symbol}{converted_avg_sold:,}</div>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">📦 Total Listings</div>
                <div class="metric-value">{metrics['total']}</div>
            </div>
        """, unsafe_allow_html=True)




#LISTING CARD (correct signature)
def listing_card(item):
    st.image(item["image"], use_container_width=True)
    st.write(f"**{item['name']}**")
    st.write(f"Price: ¥{item['price']:,}")
    st.write(f"Shop: {item['shop']}")
    st.write(f"Reviews: {item['reviews']} ⭐")


#SIDEBAR FILTERS
def sidebar_filters():
    with st.sidebar:

        # Title
        st.markdown("""
            <h2 style='margin-bottom: 10px;'>🛍️ Rakuten Dashboard</h2>
            <hr style='margin-top: 0px; margin-bottom: 15px;'>
        """, unsafe_allow_html=True)

        if "page" not in st.session_state:
            st.session_state.page = "Overview"

        #Navigation buttons
        st.markdown("### Navigation")

        if st.button("🏠 Overview"):
            st.session_state.page = "Overview"
        if st.button("🛒 New Listings"):
            st.session_state.page = "New Listings"
        if st.button("💸 Sold Listings"):
            st.session_state.page = "Sold Listings"
        if st.button("📊 Trends"):
            st.session_state.page = "Trends"

        #Filters
        keyword = st.text_input("🔍 Search keyword")
        price_range = st.slider("Price range", 0, 50000, (0, 50000))
        review_score = st.slider("Minimum reviews", 0, 500, 0)

        #Currency toggle (BOTTOM OF SIDEBAR)
        st.markdown("---")
        currency = st.toggle("Show prices in GBP (£)")

        return st.session_state.page, keyword, price_range, review_score, currency









