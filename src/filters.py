#filters by sold items, new items, keyword, price, category or review score. (found in sidebar)

#filter by keyword (found in sidebar)
def filter_by_keyword(items, keyword):
    results = []
    keyword = keyword.lower()

    for item in items:
        title = item["name"].lower()
        if keyword in title:
            results.append(item)

    return results

#filter by category
def filter_by_category(items, category):
   pass

#filter by price range
def filter_by_price(items, min_price, max_price):
    results = []
    for item in items:
        if min_price <= item["price"] <= max_price:
            results.append(item)
    return results

#filter by review score filter
def filter_by_review(items, min_score):
    results = []
    for item in items:
        if item["reviews"] >= min_score:
            results.append(item)
    return results

#combined filter (multiple filters at once)
def combined_filter(items, keyword, min_price, max_price, min_score):
    filtered = items

    if keyword:
        filtered = filter_by_keyword(filtered, keyword)

    filtered = filter_by_price(filtered, min_price, max_price)

    filtered = filter_by_review(filtered, min_score)

    return filtered
