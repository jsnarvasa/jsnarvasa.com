from datetime import datetime
from flask import request
from models.Area import Area
import config

class Utils():

    @staticmethod
    def get_geojson(image_names):
        regions = []
        areas = []
        for image in image_names:
            regions.append(image.Region)
        for (idx, region) in enumerate(regions):
            if Area.is_area_exist(region):
                # Check first, if region boundary data exists
                areas.append(region)
            else:
                # Default to country boundary data
                areas.append(image_names[idx].Country)
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
    def get_start_end_date_params():
        # To accommodate for timeline start and end date request
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