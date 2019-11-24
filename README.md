# Scrape GPlaces API

This script uses the GPlaces API to return search results within a larger area. It uses whois domain name queries and checks the reviews on Google Maps to find out how "old" a search result might be.

GPlaces API limits you to 60 results per request.
This script performs multiple requests with smaller radius by sampling lat/lon values within the defined larger radius.

Run it like this to find lots of beer gardens:
```python3 gplaces.py --search "Biergarten" --lat xx.xxxxx --lon xx.xxxxx --radius 30 --stopafter 1000--apikey "YOUR_API_KEY"```

