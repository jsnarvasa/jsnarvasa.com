import iso_code
import countries

areas = countries.geojson['features']
sql_text = []

def match_areacode(areaname):
    for area in iso_code.mapping:
        if area[0] == areaname:
            return area[1]

for area in areas:
    areatype = '31661a2'
    areaname = area['properties']['ISO_A3']
    geometry = str(area['geometry'])
    geometry = geometry.replace("'","\"")
    areacode = str(match_areacode(areaname))
    area_sql = f"INSERT IGNORE INTO Area VALUES ('{areacode}', '{areatype}', '{areaname}', '{geometry}')"
    sql_text.append(area_sql)

sql_text = ";".join(str(sql) for sql in sql_text)

sql_file = open("boundaries.sql", "w")
sql_file.write(sql_text)
sql_file.close()