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
        return cls.query.filter(cls.ISO31661a2.in_(countryCode)).all()


    @classmethod
    def geojson_constructor(cls, results_object):
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