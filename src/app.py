#final app, importing all modules etc

import streamlit as st
import datetime
import plotly.express as px

from charts import price_bucket_chart

from api_ingestion import fetch_all_items
from data_cleaning import clean_all_items

from filters import combined_filter
from metrics import compute_metrics
from charts import (
    price_bucket_chart,
    price_distribution_chart,
    top_shops_chart,
    review_distribution_chart,
    price_vs_reviews_scatter
)

from ui_components import (
    search_and_darkmode,
    sidebar_filters,
    metric_row,
    listing_card
)

# --- DATA LOADING ---
search_query = search_and_darkmode()

# fetch items from Rakuten API
if search_query:
    raw_items = fetch_all_items(search_query)
else:
    raw_items = fetch_all_items("fashion")  # default keyword

# clean items
items = clean_all_items(raw_items)

# --- SIDEBAR FILTERS ---
page, keyword, price_range, review_score, currency = sidebar_filters()
def convert(price, currency):
    if currency:
        return int(price * 0.0052)  #example rate
    return price


# --- APPLY FILTERS ---
filtered_items = combined_filter(
    items,
    keyword,
    price_range[0],
    price_range[1],
    review_score
)

# --- METRICS ---
metrics = compute_metrics(filtered_items)

# --- PAGE ROUTING ---
# --- PAGE ROUTING ---
if page == "Overview":

    # --- METRICS ---
    metric_row(metrics, currency, convert)

    # --- CHARTS IN TWO COLUMNS ---
    col1, col2 = st.columns(2)

    #Chart 1: price bucket
    with col1:
        fig_buckets = price_bucket_chart(filtered_items)
        st.plotly_chart(fig_buckets, use_container_width=True, key="bucket_chart_overview")

    # Chart 2: price distribution (New)
    fig_price = price_distribution_chart(filtered_items)

    with col2:
        st.plotly_chart(fig_price, use_container_width=True, key="price_chart")
    # --- SEPARATOR ---
    st.markdown("---")

    # --- LATEST LISTINGS ---
    st.subheader("Latest Listings")

    latest_items = filtered_items[:6]

    if latest_items:
        cols = st.columns(6)

        for idx, item in enumerate(latest_items):
            with cols[idx]:
                st.markdown(
                    f"""
                    <a href="{item['url']}" target="_blank" style="text-decoration:none; color:inherit;">
                        <div style="
                            padding:12px;
                            border-radius:10px;
                            margin-bottom:15px;
                            height: 420px;
                            overflow: hidden;
                        ">
                            <img src="{item['image']}" style="width:100%; border-radius:8px;"/>
                            <h4 style="margin-top:10px; font-size:16px; line-height:1.2; height:40px; overflow:hidden;">
                                {item['name']}
                            </h4>
                            <p>Price: {'£' if currency else '¥'}{convert(item['price'], currency):,}</p>
                            <p>Shop: {item['shop']}</p>
                            <p>Reviews: {item['reviews']} ⭐</p>
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )


    else:
        st.write("No listings found.")

    # --- SEPARATOR ---
    st.markdown("---")

    # --- ADDITIONAL CHARTS (3 SIDE-BY-SIDE) ---
    st.subheader("Market Insights")

    colA, colB, colC = st.columns(3)

    with colA:
        st.plotly_chart(top_shops_chart(filtered_items), use_container_width=True, key="top_shops_chart")
    with colB:
        st.plotly_chart(review_distribution_chart(filtered_items), use_container_width=True, key="review_chart")
    with colC:
        st.plotly_chart(price_vs_reviews_scatter(filtered_items), use_container_width=True, key="scatter_chart")


#newlistings page
elif page == "New Listings":

    st.title("New Listings")
    # Sort by lowest reviews (newest listings)
    new_items = sorted(filtered_items, key=lambda x: x["reviews"])

    st.subheader("Latest New Listings")

    if not new_items:
        st.write("No new listings found.")
    else:
        cols = st.columns(3)

        for idx, item in enumerate(new_items):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <a href="{item['url']}" target="_blank" style="text-decoration:none; color:inherit;">
                        <div style="
                            padding:12px;
                            border-radius:10px;
                            margin-bottom:15px;
                            height: 420px;
                            overflow: hidden;
                        ">
                            <img src="{item['image']}" style="width:100%; border-radius:8px;"/>
                            <h4 style="margin-top:10px; font-size:16px; line-height:1.2; height:40px; overflow:hidden;">
                                {item['name']}
                            </h4>
                            <p>Price: {'£' if currency else '¥'}{convert(item['price'], currency):,}</p>
                            <p>Reviews: {item['reviews']} ⭐</p>
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )


#sold listings page
elif page == "Sold Listings":
    st.title("Sold Listings")

    # Sort by highest reviews (most popular items)
    sold_items = sorted(filtered_items, key=lambda x: x["reviews"], reverse=True)

    st.subheader("Most Popular Listings")

    if not sold_items:
        st.write("No sold listings found.")
    else:
        cols = st.columns(3)

        for idx, item in enumerate(sold_items):
            with cols[idx % 3]:
                listing_card(item)

#trends (sidebar)
elif page == "Trends":
    if not filtered_items:
        st.subheader("No results found")
        st.write("Try adjusting your search or filters.")
        st.markdown("---")
        st.stop()

    st.subheader("Price Trends")

    col_summary, col_chart = st.columns([1, 1])

    with col_summary:
        st.write("")
        st.write("")

        prices = [item["price"] for item in filtered_items]
        st.write(f"Lowest price: ¥{min(prices):,}")
        st.write(f"Highest price: ¥{max(prices):,}")
        st.write(f"Average price: ¥{sum(prices) / len(prices):,.0f}")

        # Price buckets
        low = len([i for i in filtered_items if i["price"] < 3000])
        mid = len([i for i in filtered_items if 3000 <= i["price"] < 7000])
        high = len([i for i in filtered_items if i["price"] >= 7000])

        total = len(filtered_items)
        low_pct = (low / total) * 100
        mid_pct = (mid / total) * 100
        high_pct = (high / total) * 100

        st.markdown("#### Analysis")
        if low > mid and low > high:
            st.write("Most items are low-priced, suggesting this keyword is dominated by budget products.")
        elif mid > low and mid > high:
            st.write("Most items fall in the mid-price range, indicating a balanced market.")
        else:
            st.write("High-priced items dominate this keyword, suggesting a premium market.")

    with col_chart:
        bucket_fig = px.bar(
            x=["Low (<¥3000)", "Mid (¥3000–7000)", "High (¥7000+)"],
            y=[low, mid, high],
            text=[f"{low_pct:.1f}%", f"{mid_pct:.1f}%", f"{high_pct:.1f}%"],
            title="Price Buckets",
            labels={"x": "Bucket", "y": "Listings"},
            color_discrete_sequence=["#4C78A8"]
        )
        bucket_fig.update_traces(textposition="outside")
        bucket_fig.update_layout(height=320)
        st.plotly_chart(bucket_fig, use_container_width=True, key="bucket_chart")
        st.markdown("---")
    #review summary
    st.subheader("Review Trends")

    col_summary, col_chart = st.columns([1, 1])

    with col_summary:
        st.write("")
        st.write("")

        #Extract review counts
        reviews = [item["reviews"] for item in filtered_items]

        avg_reviews = sum(reviews) / len(reviews)
        median_reviews = sorted(reviews)[len(reviews) // 2]
        max_reviews = max(reviews)

        st.write(f"Average reviews: {avg_reviews:.1f}")
        st.write(f"Median reviews: {median_reviews}")
        st.write(f"Most reviews on a single item: {max_reviews}")

        #review buckets
        low_r = len([r for r in reviews if r < 50])
        mid_r = len([r for r in reviews if 50 <= r < 300])
        high_r = len([r for r in reviews if r >= 300])

        total_r = len(reviews)
        low_r_pct = (low_r / total_r) * 100
        mid_r_pct = (mid_r / total_r) * 100
        high_r_pct = (high_r / total_r) * 100

        #Analysis
        st.markdown("#### Analysis")
        if low_r > mid_r and low_r > high_r:
            st.write("Most items have low review counts, suggesting limited buyer engagement.")
        elif mid_r > low_r and mid_r > high_r:
            st.write("Most items have moderate review counts, indicating steady buyer activity.")
        else:
            st.write("Highly reviewed items dominate this keyword, suggesting strong buyer interest.")

    with col_chart:
        review_fig = px.bar(
            x=["Low (<50)", "Mid (50–300)", "High (300+)"],
            y=[low_r, mid_r, high_r],
            text=[f"{low_r_pct:.1f}%", f"{mid_r_pct:.1f}%", f"{high_r_pct:.1f}%"],
            title="Review Buckets",
            labels={"x": "Bucket", "y": "Listings"},
            color_discrete_sequence=["#4C78A8"]
        )
        review_fig.update_traces(textposition="outside")
        review_fig.update_layout(height=320)
        st.plotly_chart(review_fig, use_container_width=True, key="review_bucket_chart")
        st.markdown("---")


    st.subheader("Shop Trends")

    col_summary, col_chart = st.columns([1, 1])

    with col_summary:
        st.write("")
        st.write("")

        shops = [item["shop"] for item in filtered_items]
        unique_shops = set(shops)

        # Count listings per shop
        shop_counts = {shop: shops.count(shop) for shop in unique_shops}

        # Top shop
        top_shop = max(shop_counts, key=shop_counts.get)
        dominance = (shop_counts[top_shop] / len(filtered_items)) * 100

        st.write(f"Unique shops: {len(unique_shops)}")
        st.write(f"Top shop: {top_shop}")
        st.write(f"Top shop dominance: {dominance:.1f}% of all listings")

        # Analysis
        st.markdown("#### Analysis")
        if dominance > 50:
            st.write(f"{top_shop} strongly dominates this keyword, indicating a concentrated seller market.")
        elif dominance > 30:
            st.write(f"{top_shop} has a notable presence, but competition remains healthy.")
        else:
            st.write("Listings are evenly distributed across shops, suggesting a competitive market.")

    with col_chart:
        shop_fig = px.bar(
            x=list(shop_counts.keys()),
            y=list(shop_counts.values()),
            title="Shop Listing Distribution",
            labels={"x": "Shop", "y": "Listings"},
            text=[f"{(count / len(filtered_items)) * 100:.1f}%" for count in shop_counts.values()],
            color_discrete_sequence=["#4C78A8"]
        )
        shop_fig.update_traces(textposition="outside")
        shop_fig.update_layout(height=340)
        st.plotly_chart(shop_fig, use_container_width=True, key="shop_chart")

    st.markdown("---")

