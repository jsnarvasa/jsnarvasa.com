from datetime import datetime
from flask import request
import urllib.parse as urlparse
from urllib.parse import parse_qs
from modules.Area import Area
import config

class Utils():

    @staticmethod
    def get_geojson(image_names):
        """Aggregates the list of areas to be added to the geoJSON object, based on the list of image names provided"""
        areas = [image.Region if Area.is_area_exist(image.Region) else image.Country for image in image_names]
        boundaries = Area.get_area(areas)
        geojson = Area.geojson_constructor(boundaries)

        return geojson


    @staticmethod
    def get_mapbox_token(hostname):
        if hostname == config.hostname['PROD']:
            token = config.mapbox['TOKEN']['PROD']
        else:
            token = config.mapbox['TOKEN']['DEV']        
        return token


    @staticmethod
    def get_start_end_date_params(is_feed=False):
        """To accommodate for timeline start and end date request"""

        if is_feed:
            parsed = urlparse.urlparse(request.referrer)
            start_date = parse_qs(parsed.query).get('start')
            end_date = parse_qs(parsed.query).get('end')
            try:
                start_date, end_date = start_date[0], end_date[0]
            except TypeError:
                pass
        else:
            start_date = request.args.get('start')
            end_date = request.args.get('end')

        if start_date is not None and end_date is not None:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Expected date format is 'YYYY-MM-DD'")
        else:
            start_date, end_date = None, None

        return (start_date, end_date)