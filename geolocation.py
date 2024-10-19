#! /usr/bin/env python
# coding=utf-8
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
        geolocator = Nominatim(timeout=7, proxies={'http': None, 'https': None}, user_agent='My_agent')
        x = geolocator.geocode(text)
        if x:
            return Location(x.latitude, x.longitude)
        return Location(0, 0)
    except Exception as e:
        logger.error(f"Error geolocate: {e}")




def main():
    logger.info(f"Starting geolocation service")
    text = 'Бердск'
    location = geolocate(text)
    logger.info(f"Location: {location}")


if __name__ == '__main__':
    main()
