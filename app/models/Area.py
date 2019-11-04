import json
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from app import db

class Area(db.Model):
    __tablename__ = "Area"

    AreaCode = db.Column('AreaCode', db.String(20), primary_key=True) # ISO 31661a2 or ISO 3166-2 code
    AreaType = db.Column('AreaType', db.String(20), nullable=False) # The ISO standard it follows
    AreaName = db.Column('AreaName', db.String(150), nullable=False) # Free text identifier
    Geometry = db.Column('Geometry', MEDIUMTEXT) # Boundary data


    @classmethod
    def is_area_exist(cls, areacode):
    # OUTPUT - Returns BOOL based on whether the areacode exists in the database
        if cls.query.filter_by(AreaCode=areacode).first() is None:
            return False
        else:
            return True

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