#import os
import psycopg2
#from dotenv import load_dotenv
from flask import Flask, request, Blueprint

#load_dotenv()
#url = os.getenv('DATABASE_URL')
#connection = psycopg2.connect(url)
connection = psycopg2.connect(dbname="addressdb", user="postgres", password="87654321", host="127.0.0.1", port="5432")

CREATE_REGIONS_TABLE = """CREATE TABLE IF NOT EXISTS regions ( id serial NOT NULL PRIMARY KEY, 
NameRegion character varying(20), CountryID INTEGER, FOREIGN KEY (CountryID) REFERENCES countries(id) ON DELETE CASCADE);"""

INSERT_REGION_RETURN_ID = "INSERT INTO regions (NameRegion, CountryID) VALUES (%s, %s) RETURNING id;"

DELETE_REGION = "DELETE FROM regions WHERE id = %s"

SELECT_REGION_BY_ID = "SELECT id, NameRegion, CountryID FROM regions WHERE id = %s"

EDIT_REGION = "UPDATE regions SET NameRegion = %s WHERE id = %s"

SELECT_ALL_REGIONS_IN_COUNTRY = "SELECT id, NameRegion, CountryID from regions WHERE CountryID = %s ORDER BY id"

SELECT_COUNTRY_BY_ID = "SELECT id, FullName, ShortName FROM countries WHERE id = %s"

SELECT_ALL_REGIONS = "SELECT id, NameRegion, CountryID from regions ORDER BY id"

region = Blueprint('region', __name__, template_folder='templates')


@region.route('/api/country/<idCountry>/region', methods=('GET', 'POST'))
def create_region_in_country(idCountry):
    if request.method == "POST":
        data = request.get_json()
        NameRegion = data["NameRegion"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_REGIONS_TABLE)
                cursor.execute(INSERT_REGION_RETURN_ID, (NameRegion, idCountry, ))
                RegionID = cursor.fetchone()[0]
        return {"id": RegionID, "message": f"Регион {NameRegion} добавлен."}, 201
    elif request.method == "GET":
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_ALL_REGIONS_IN_COUNTRY, idCountry)
                regions = cursor.fetchall()
                regs = []
                for region in regions:
                    cursor.execute(SELECT_COUNTRY_BY_ID, (region[2],))
                    curcountry = cursor.fetchone()[1]
                    dict = {"id": region[0], "NameRegion": region[1], "CountryID": curcountry}
                    regs.append(dict)
                return {"regions": regs}, 200


@region.route('/api/country/<idCountry>/region/<idRegion>', methods=('GET', 'DELETE', 'PUT'))
def get_region_in_country(idCountry, idRegion):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_REGION_BY_ID, (idRegion,))
            region = cursor.fetchone()
            id = region[0]
            NameRegion = region[1]
            CountryID = region[2]
    if request.method == 'GET':
        return {"id": id, "NameCity": NameRegion, "RegionID": CountryID}, 200
    elif request.method == 'DELETE':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DELETE_REGION, (idRegion,))
        return {"message": f"Регион {NameRegion} удалён."}, 200
    elif request.method == 'PUT':
        data = request.get_json()
        newNameRegion = data["newNameRegion"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(EDIT_REGION, (newNameRegion, idRegion, ))
        return {"message": f"Регион {newNameRegion} отредактирован."}, 200


@region.route('/api/region', methods=('GET', 'POST'))
def create_region():
    if request.method == "POST":
        data = request.get_json()
        NameRegion = data["NameRegion"]
        CountryID = data["CountryID"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_REGIONS_TABLE)
                cursor.execute(INSERT_REGION_RETURN_ID, (NameRegion, CountryID, ))
                RegionID = cursor.fetchone()[0]
        return {"id": RegionID, "message": f"Регион {NameRegion} добавлен."}, 201
    elif request.method == "GET":
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_ALL_REGIONS)
                regions = cursor.fetchall()
                regs = []
                for region in regions:
                    cursor.execute(SELECT_COUNTRY_BY_ID, (region[2],))
                    curcountry = cursor.fetchone()[1]
                    dict = {"id": region[0], "NameRegion": region[1], "CountryID": curcountry}
                    regs.append(dict)
                return {"regions": regs}, 200


@region.route('/api/region/<idRegion>', methods=('GET', 'DELETE', 'PUT'))
def get_region(idRegion):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_REGION_BY_ID, (idRegion,))
            region = cursor.fetchone()
            id = region[0]
            NameRegion = region[1]
            CountryID = region[2]
    if request.method == 'GET':
        return {"id": id, "NameCity": NameRegion, "RegionID": CountryID}, 200
    elif request.method == 'DELETE':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DELETE_REGION, (idRegion,))
        return {"message": f"Регион {NameRegion} удалён."}, 200
    elif request.method == 'PUT':
        data = request.get_json()
        newNameRegion = data["newNameRegion"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(EDIT_REGION, (newNameRegion, idRegion, ))
        return {"message": f"Регион {newNameRegion} отредактирован."}, 200
