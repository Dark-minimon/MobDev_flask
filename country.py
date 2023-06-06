#import os
import psycopg2
#from dotenv import load_dotenv
from flask import Flask, request, Blueprint

#load_dotenv()
#url = os.getenv('DATABASE_URL')
#connection = psycopg2.connect(url)
connection = psycopg2.connect(dbname="addressdb", user="postgres", password="87654321", host="127.0.0.1", port="5432")

CREATE_COUNTRIES_TABLE = """CREATE TABLE IF NOT EXISTS countries ( id serial NOT NULL PRIMARY KEY, 
FullName character varying(20), ShortName character varying(5));"""

INSERT_COUNTRY_RETURN_ID = "INSERT INTO countries (FullName, ShortName) VALUES (%s, %s) RETURNING id;"

DELETE_COUNTRY = "DELETE FROM countries WHERE id = %s"

SELECT_COUNTRY_BY_ID = "SELECT id, FullName, ShortName FROM countries WHERE id = %s"

EDIT_COUNTRY = "UPDATE countries SET FullName = %s, ShortName = %s WHERE id = %s"

SELECT_ALL_COUNTRIES = "SELECT id, FullName, ShortName from countries ORDER BY id"

country = Blueprint('country', __name__, template_folder='templates')


@country.route('/api/country', methods=('GET', 'POST'))
def create_country():
    if request.method == "POST":
        data = request.get_json()
        FullName = data["FullName"]
        ShortName = data["ShortName"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_COUNTRIES_TABLE)
                cursor.execute(INSERT_COUNTRY_RETURN_ID, (FullName, ShortName, ))
                CountryID = cursor.fetchone()[0]
        return {"id": CountryID, "message": f"Страна {FullName} добавлена."}, 201
    elif request.method == "GET":
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_ALL_COUNTRIES)
                countries = cursor.fetchall()
                counts = []
                for country in countries:
                    dict = {"id": country[0], "FullName": country[1], "ShortName": country[2]}
                    counts.append(dict)
                return {"countries": counts}, 200


@country.route('/api/country/<idCountry>', methods=('GET', 'DELETE', 'PUT'))
def get_country(idCountry):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_COUNTRY_BY_ID, (idCountry,))
            region = cursor.fetchone()
            id = region[0]
            FullName = region[1]
            ShortName = region[2]
    if request.method == 'GET':
        return {"id": id, "FullName": FullName, "ShortName": ShortName}, 200
    elif request.method == 'DELETE':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DELETE_COUNTRY, (idCountry,))
        return {"message": f"Страна {FullName} удалёна."}, 200
    elif request.method == 'PUT':
        data = request.get_json()
        newFullName = data["newFullName"]
        newShortName = data["newShortName"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(EDIT_COUNTRY, (newFullName, newShortName, idCountry, ))
        return {"message": f"Страна {newFullName} отредактирована."}, 200
