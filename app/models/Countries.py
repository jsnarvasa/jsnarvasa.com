import json
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from app import db

class Countries(db.Model):
    __tablename__ = "Countries"

    ISO31661a2 = db.Column('ISO31661a2', db.String(2), primary_key=True)
    CountryName = db.Column('CountryName', db.String(150), unique=True)
    ISO31661a3 = db.Column('ISO31661a3', db.String(3), unique=True)
    Geometry = db.Column('Geometry', MEDIUMTEXT)


    @classmethod
    def get_country(cls, countryCode):
    # INPUT - LIST of country code in 2 alphanumeric combination
    # OUTPUT - LIST of Countries object that are in INPUT list
        return cls.query.filter(cls.ISO31661a2.in_(countryCode)).all()

    @classmethod
    def geojson_constructor(cls, results_object):
    # Input - LIST of Countries object; containing all details from Countries
    # Output - geoJSON data containing the boundary of the areas in the input object
        geojson = {}
        geojson['type'] = 'FeatureCollection'
        geojson['features'] = []
        if isinstance(results_object, list):
            for country in results_object:
                country_json = {}
                country_json['type'] = 'Feature'
                country_json['properties'] = {}
                country_json['properties']['ADMIN'] = country.CountryName
                country_json['properties']['ISO_A3'] = country.ISO31661a3
                country_json['geometry'] = json.loads(country.Geometry)
                geojson['features'].append(country_json)
        return geojson