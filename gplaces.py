import time
import whois
import sys
import argparse
from googleplaces import GooglePlaces, types, lang
from urllib.parse import urlparse
from datetime import datetime

# Parse arguments
my_parser = argparse.ArgumentParser(description='Search places nearby in a certain radius')

# Add the arguments
my_parser.add_argument('--apikey',
                       type=str,
                       help='the Google Cloud API key')
my_parser.add_argument('--search',
                       type=str,
                       help='the search string')
my_parser.add_argument('--radius',
                       type=int,
                       help='the radius in km')
my_parser.add_argument('--lat',
                       type=float,
                       help='the latitute')
my_parser.add_argument('--lon',
                       type=float,
                       help='the longitude')

args = my_parser.parse_args()

google_places = GooglePlaces(args.apikey)

lat_start = args.lat
lon_start = args.lon
radius_km = args.radius
step_width = 3.0
steps = radius_km/step_width

def addPlaces(places):
    for element in places:
        element.get_details()
        print("Adding " + element.name)
        if element.website == None or len(element.website) < 2:
            allPlaces.append({'name': element.name, 'rating': element.rating})
        else:
            domainstr = urlparse(element.website).netloc
            domainstr = '.'.join(domainstr.split('.')[-2:])
            try:
                domain = whois.query(domainstr)
                allPlaces.append({'name': element.name, 'rating': element.rating, 'website': element.website, 'updated': domain.last_updated})
            except:
                allPlaces.append({'name': element.name, 'rating': element.rating, 'website': element.website, 'updated': 0})

def printResults():
    printedNames = []
    for element in allPlaces:
        if element['name'] in printedNames:
            continue

        printedNames.append(element['name'])
        if 'website' in element:
            print(element['name'] + ";" + str(element['rating']) + ";" + element['website'] + ";" + str(element['updated']))
        else:
            print(element['name'] + ";" + str(element['rating']))

allPlaces = []
stepx = -steps/2
while stepx < steps/2:
    lat = lat_start + (stepx * 0.04)
    stepx = stepx + 1
    stepy = -steps/2
    print("Lat changed: " + str(lat))
    while stepy < steps/2:
        lon = lon_start + (stepy * 0.04)
        stepy = stepy + 1
        print("Lon changed: " + str(lon))
        next_page_token = None

        results = google_places.nearby_search(lat_lng={'lat': lat, 'lng': lon}, keyword="Zahnarzt", radius=4000, rankby='distance')
        addPlaces(results.places)
        time.sleep(2)
        if results.has_next_page_token:
            next_page_token = results.next_page_token
        
        while next_page_token != None:
            print("Requesting further pages: " + next_page_token)
            results = google_places.nearby_search(pagetoken=next_page_token)
            addPlaces(results.places)
            time.sleep(2)
            if results.has_next_page_token:
                next_page_token = results.next_page_token
            else:
                next_page_token = None

printResults()
