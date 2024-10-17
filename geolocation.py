#! /usr/bin/env python
import sys
from geopy.geocoders import Nominatim
from typing import NamedTuple
import logging


logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)



class Location(NamedTuple):
    latitude: float
    longitude: float

def geolocate(text: str) -> Location:
    try:

        geolocator = Nominatim(timeout=7, user_agent="my_Geocoder")
        x = geolocator.geocode(text)
        return Location(x.latitude, x.longitude)
    except Exception as e:
        logger.error(f"Error geolocate: {e}")




def main():
    logger.info(f"Starting geolocation service")
    text = 'Berdsk, Russia'
    location = geolocate(text)
    logger.info(f"Location: {location}")


if __name__ == '__main__':
    main()
