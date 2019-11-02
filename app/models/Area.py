import json
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from app import db

class Area(db.Model):
    __tablename__ = "Area"

    AreaCode = db.Column('AreaCode', db.String(20), primary_key=True) # ISO31661a2 code
    AreaType = db.Column('AreaType', db.String(20), nullable=False)
    AreaName = db.Column('AreaName', db.String(150), nullable=False)
    Geometry = db.Column('Geometry', MEDIUMTEXT)


    @classmethod
    def get_area(cls, areaCode):
    # INPUT - LIST of area code in 2 alphanumeric combination
    # OUTPUT - LIST of Area object that are in INPUT list
        return cls.query.filter(cls.AreaCode.in_(areaCode)).all()

    @classmethod
    def geojson_constructor(cls, area_list):
    # Input - LIST of Area object; containing all details from Area
    # Output - geoJSON data containing the boundary of the areas in the input object
        geojson = {}
        geojson['type'] = 'FeatureCollection'
        geojson['features'] = []
        if isinstance(area_list, list):
            for area in area_list:
                area_json = {}
                area_json['type'] = 'Feature'
                area_json['properties'] = {}
                # area_json['properties']['ADMIN'] = area.CountryName
                # area_json['properties']['ISO_A3'] = area.ISO31661a3
                area_json['geometry'] = json.loads(area.Geometry)
                geojson['features'].append(area_json)
        return geojson