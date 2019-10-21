# Scrape GPlaces API

GPlaces API limits you to 60 results per request.
This script performs multiple requests with smaller radius by sampling lat/lon values within the defined larger radius.

Run it like this to find lots of beer gardens:
```python3 gplaces.py --search "Biergarten" --lat xx.xxxxx --lon xx.xxxxx --radius 30 --apikey "YOUR_API_KEY"```

