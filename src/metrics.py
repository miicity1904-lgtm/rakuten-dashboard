#metrics module, showing new listings, sold listings, average price (new listings), average price (sold) and total listings

#total listings
def total_listings(items):
    return len(items)


#new listings (reviews == 0)
def new_listings(items):
    return sum(1 for item in items if item["reviews"] == 0)


#average price of ALL listings
def avg_price(items):
    if not items:
        return 0
    return sum(item["price"] for item in items) / len(items)


#average price of NEW listings
def avg_price_new(items):
    new = [item for item in items if item["reviews"] == 0]
    if not new:
        return 0
    return int(sum(item["price"] for item in new) / len(new))



#sold listings (reviews > 0)
def sold_listings(items):
    return sum(1 for item in items if item["reviews"] > 0)


#average price of SOLD listings
def avg_price_sold(items):
    sold = [item for item in items if item["reviews"] > 0]
    if not sold:
        return 0
    return int(sum(item["price"] for item in sold) / len(sold))



#bundle all metrics into one dictionary
def compute_metrics(items):
    return {
        "new": new_listings(items),
        "sold": sold_listings(items),
        "avg_new": avg_price_new(items),
        "avg_sold": avg_price_sold(items),
        "total": total_listings(items),
        "avg_all": avg_price(items)
    }
