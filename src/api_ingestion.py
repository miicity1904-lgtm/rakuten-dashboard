#interacts with rakuten api, handles multiples pages, deals with errors, saves raw data to data/raw

import requests
import json
import os
from datetime import datetime
import streamlit as st

url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260701"


headers = {
        "accessKey": "pk_ArLWb4HT8mmzZwNlpSY5BulxK2yTsljOARf7kz0QbGE",
        "Referer": "https://example.com/",
        "Origin": "https://example.com/",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }



def fetch_page(keyword, page):
    params = {
        "applicationId": "22dff658-8f6e-42de-8875-d0f67bd85641",
        "keyword": keyword,
        "format": "json",
        "page": page,
        "hits": 30
    }
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()   #for errors
        return response.json()

    except Exception as e:
        print(f"[ERROR] Failed to fetch page {page}: {e}")
        return None
@st.cache_data(show_spinner=False)
def fetch_all_items(keyword, max_pages=3):
    all_items = []

    for page in range(1, max_pages + 1):
        data = fetch_page(keyword, page)

        #stopsif API fails or no items returned
        if not data or "Items" not in data:
            break

        #add items from this page
        all_items.extend(data["Items"])

        #the API sometimes returns fewer items on last page
        if len(data["Items"]) < 30:
            break

    return all_items

def save_raw_json(keyword, items):
    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = (f"data/raw/{keyword}_{timestamp}.json")
    with open(filename, "w", encoding= "utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
