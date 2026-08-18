#module for charts found in streamlit dashboard (bar charts, line graphs)

import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import plotly.express as px

#listings over time chart
def price_bucket_chart(items):
    if not items:
        return px.bar(title="No data available")

    buckets = {
        "0–2000": 0,
        "2000–5000": 0,
        "5000–10000": 0,
        "10000+": 0
    }

    for item in items:
        p = item["price"]
        if p < 2000:
            buckets["0–2000"] += 1
        elif p < 5000:
            buckets["2000–5000"] += 1
        elif p < 10000:
            buckets["5000–10000"] += 1
        else:
            buckets["10000+"] += 1

    fig = px.bar(
        x=list(buckets.keys()),
        y=list(buckets.values()),
        title="Price Bucket Distribution",
        labels={"x": "Price Range", "y": "Listings"},
        color_discrete_sequence=["#4C78A8"]
    )

    fig.update_layout(template="plotly_dark")
    return fig


#price distriubtion chart (new)
def price_distribution_chart(items):
    if not items:
        return px.bar(title="No data available")
    prices = [item["price"] for item in items]

    fig = px.histogram(
        prices,
        nbins=20,
        title="Price Distribution (New)",
        labels={"value": "Price (¥)", "count": "Number of Listings"},
        color_discrete_sequence=["#4C78A8"]
    )

    fig.update_layout(template="plotly_dark")
    return fig

#top shops chart
def top_shops_chart(items):
    if not items:
        return px.bar(title="No data available")
    shops = [item.get("shop", "Unknown") for item in items]
    shop_counts = Counter(shops)

    labels = list(shop_counts.keys())
    values = list(shop_counts.values())

    fig = px.bar(
        x=values,
        y=labels,
        orientation="h",
        title="Top Shops (Listings Count)",
        labels={"x": "Listings", "y": "Shop"},
        color_discrete_sequence=["#F58518"]
    )

    fig.update_layout(template="plotly_dark")
    return fig

#review distriubtion chart (shows how popular items are)
def review_distribution_chart(items):
    if not items:
        return px.bar(title="No data available")
    reviews = [item.get("reviews", 0) for item in items]

    fig = px.histogram(
        reviews,
        nbins=20,
        title="Review Distribution",
        labels={"value": "Review Count", "count": "Number of Listings"},
        color_discrete_sequence=["#4C78A8"]
    )

    fig.update_layout(template="plotly_dark")
    return fig

#price vs reviews
def price_vs_reviews_scatter(items):
    if not items:
        return px.bar(title="No data available")

    prices = [item.get("price", 0) for item in items]
    reviews = [item.get("reviews", 0) for item in items]

    #Clean English hover text
    hover = [
        f"{item['shop']} — ¥{item['price']:,} — {item['reviews']} reviews"
        for item in items
    ]

    fig = px.scatter(
        x=prices,
        y=reviews,
        hover_name=hover,
        title="Price vs Reviews",
        labels={"x": "Price (¥)", "y": "Review Count"},
        color_discrete_sequence=["#9C755F"]
    )

    fig.update_layout(template="plotly_dark")
    fig.update_yaxes(type="log")

    return fig
