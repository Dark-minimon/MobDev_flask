#import os
import psycopg2
#from dotenv import load_dotenv
from flask import Flask, request, Blueprint

#load_dotenv()
#url = os.getenv('DATABASE_URL')
#connection = psycopg2.connect(url)
connection = psycopg2.connect(dbname="addressdb", user="postgres", password="87654321", host="127.0.0.1", port="5432")

CREATE_CITIES_TABLE = """CREATE TABLE IF NOT EXISTS cities ( id serial NOT NULL PRIMARY KEY, 
NameCity character varying(20), RegionID INTEGER, FOREIGN KEY (RegionID) REFERENCES regions(id) ON DELETE CASCADE);"""

INSERT_CITY_RETURN_ID = "INSERT INTO cities (NameCity, RegionID) VALUES (%s, %s) RETURNING id;"

DELETE_CITY = "DELETE FROM cities WHERE id = %s"

SELECT_CITY_BY_ID = "SELECT id, NameCity, RegionID FROM cities WHERE id = %s"

EDIT_CITY = "UPDATE cities SET NameCity = %s WHERE id = %s"

SELECT_ALL_CITIES_IN_REGION = "SELECT id, NameCity, RegionID from cities WHERE RegionID = %s ORDER BY id"

SELECT_REGION_BY_ID = "SELECT id, NameRegion, CountryID FROM regions WHERE id = %s"

SELECT_ALL_CITIES = "SELECT id, NameCity, RegionID from cities ORDER BY id"

city = Blueprint('city', __name__, template_folder='templates')


@city.route('/api/country/<idCountry>/region/<idRegion>/city/', methods=('GET', 'POST'))
def create_city_in_region(idCountry, idRegion):
    if request.method == "POST":
        data = request.get_json()
        NameCity = data["NameCity"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_CITIES_TABLE)
                cursor.execute(INSERT_CITY_RETURN_ID, (NameCity, idRegion, ))
                CityID = cursor.fetchone()[0]
        return {"id": CityID, "message": f"Город {NameCity} добавлен."}, 201
    elif request.method == "GET":
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_ALL_CITIES_IN_REGION, idRegion)
                cities = cursor.fetchall()
                cits = []
                for city in cities:
                    cursor.execute(SELECT_REGION_BY_ID, (city[2],))
                    curregion = cursor.fetchone()[1]
                    dict = {"id": city[0], "NameCity": city[1], "RegionID": curregion}
                    cits.append(dict)
                return {"products": cits}, 200


@city.route('/api/country/<idCountry>/region/<idRegion>/city/<idCity>', methods=('GET', 'DELETE', 'PUT'))
def get_city_in_region(idCountry, idRegion, idCity):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CITY_BY_ID, (idCity,))
            city = cursor.fetchone()
            id = city[0]
            NameCity = city[1]
            RegionID = city[2]
    if request.method == 'GET':
        return {"id": id, "NameCity": NameCity, "RegionID": RegionID}, 200
    elif request.method == 'DELETE':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DELETE_CITY, (idCity,))
        return {"message": f"Город {NameCity} удалён."}, 200
    elif request.method == 'PUT':
        data = request.get_json()
        newNameCity = data["newNameCity"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(EDIT_CITY, (newNameCity, idCity, ))
        return {"message": f"Город {newNameCity} отредактирован."}, 200


@city.route('/api/city', methods=('GET', 'POST'))
def create_city():
    if request.method == "POST":
        data = request.get_json()
        NameCity = data["NameCity"]
        RegionID = data["RegionID"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_CITIES_TABLE)
                cursor.execute(INSERT_CITY_RETURN_ID, (NameCity, RegionID))
                CityID = cursor.fetchone()[0]
        return {"id": CityID, "message": f"Город {NameCity} добавлен."}, 201
    elif request.method == "GET":
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_ALL_CITIES)
                cities = cursor.fetchall()
                cits = []
                for city in cities:
                    cursor.execute(SELECT_REGION_BY_ID, (city[2],))
                    curregion = cursor.fetchone()[1]
                    dict = {"id": city[0], "NameCity": city[1], "RegionID": curregion}
                    cits.append(dict)
                return {"products": cits}, 200


@city.route('/api/city/<idCity>', methods=('GET', 'DELETE', 'PUT'))
def get_city(idCity):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CITY_BY_ID, (idCity,))
            city = cursor.fetchone()
            id = city[0]
            NameCity = city[1]
            RegionID = city[2]
    if request.method == 'GET':
        return {"id": id, "NameCity": NameCity, "RegionID": RegionID}, 200
    elif request.method == 'DELETE':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DELETE_CITY, (idCity,))
        return {"message": f"Город {NameCity} удалён."}, 200
    elif request.method == 'PUT':
        data = request.get_json()
        newNameCity = data["newNameCity"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(EDIT_CITY, (newNameCity, idCity, ))
        return {"message": f"Город {newNameCity} отредактирован."}, 200