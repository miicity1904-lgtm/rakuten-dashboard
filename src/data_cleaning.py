#this module cleans raw data from api output. created a schema
#{
#    "name": str,
#   "price": int,
#   "shop": str,
#  "reviews": int,
#   "genre": int,
#  "url": str,
#   "image": str}
def clean_item(raw_item):
    raw = raw_item.get("Item", {})

    name = raw.get("itemName", "")
    price = int(raw.get("itemPrice", 0))
    shop = raw.get("shopName", "")
    reviews = int(raw.get("reviewCount", 0))
    genre = int(raw.get("genreId", 0))
    url = raw.get("itemUrl", "")

    # NEW FIELDS
    brand = raw.get("brandName", "Unknown")
    condition = raw.get("itemCondition", "Unknown")

    images = raw.get("mediumImageUrls") or []
    image = images[0].get("imageUrl", "") if images else ""

    cleaned = {
        "name": name,
        "price": price,
        "shop": shop,
        "reviews": reviews,
        "genre": genre,
        "url": url,
        "image": image,
        "brand": brand,
        "condition": condition
    }

    return cleaned


def clean_all_items(raw_items):
    return [clean_item(item) for item in raw_items]



