import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.cache import cache


def reverse_geocode(latitude, longitude):
    latitude = round(float(latitude), 6)
    longitude = round(float(longitude), 6)
    cache_key = f"maps:reverse:{latitude}:{longitude}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    if not settings.GOOGLE_MAPS_SERVER_API_KEY:
        raise RuntimeError("Google Maps server API key is not configured.")

    query = urlencode(
        {
            "latlng": f"{latitude},{longitude}",
            "key": settings.GOOGLE_MAPS_SERVER_API_KEY,
            "language": "en",
            "region": "ng",
        }
    )
    request = Request(
        f"https://maps.googleapis.com/maps/api/geocode/json?{query}",
        headers={"User-Agent": "Navigo-Locate/1.0"},
    )
    with urlopen(request, timeout=8) as response:
        document = json.load(response)

    if document.get("status") != "OK" or not document.get("results"):
        raise LookupError(document.get("error_message") or "No address was found for this location.")

    result = document["results"][0]
    components = {}
    for component in result.get("address_components", []):
        for component_type in component.get("types", []):
            components.setdefault(component_type, component.get("long_name", ""))

    payload = {
        "formatted_address": result.get("formatted_address", ""),
        "building": components.get("premise") or components.get("subpremise", ""),
        "street": components.get("route", ""),
        "neighborhood": components.get("neighborhood") or components.get("sublocality", ""),
        "locality": components.get("locality") or components.get("postal_town", ""),
        "lga": components.get("administrative_area_level_2", ""),
        "state": components.get("administrative_area_level_1", ""),
        "country": components.get("country", ""),
        "place_id": result.get("place_id", ""),
    }
    cache.set(cache_key, payload, timeout=60 * 60 * 24 * 30)
    return payload
