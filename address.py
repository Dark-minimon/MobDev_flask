#import os
import psycopg2
import json
#from dotenv import load_dotenv
from flask import Flask, request, Blueprint, jsonify, Response

#load_dotenv()
#url = os.getenv('DATABASE_URL')
#connection = psycopg2.connect(url)
connection = psycopg2.connect(dbname="addressdb", user="postgres", password="87654321", host="127.0.0.1", port="5432")

CREATE_ADDRESSES_TABLE = """CREATE TABLE IF NOT EXISTS addresses ( id serial NOT NULL PRIMARY KEY, 
Person character varying(20), Street character varying(20), Building character varying(10), 
Office character varying(10), CityID INTEGER, FOREIGN KEY (CityID) REFERENCES cities(id) ON DELETE CASCADE);"""

INSERT_ADDRESS = "INSERT INTO addresses (Person, Street, Building, Office, CityID) VALUES (%s, %s, %s, %s, %s) ;"

DELETE_ADDRESS = "DELETE FROM addresses WHERE id = %s"

SELECT_ADDRESS_BY_ID = "SELECT id, Person, Street, Building, Office, CityID FROM addresses WHERE id = %s"

EDIT_ADDRESS = "UPDATE addresses SET Person = %s, Street = %s, Building = %s, Office = %s, CityID = %s WHERE id = %s"

SELECT_ALL_CITIES = "SELECT id, NameCity, RegionID from cities ORDER BY id"

SELECT_CITY_BY_ID = "SELECT id, NameCity, RegionID FROM cities WHERE id = %s"

SELECT_ALL_ADDRESSES_IN_CITY = "SELECT id, Person, Street, Building, Office, CityID FROM addresses WHERE CityID = %s ORDER BY id"

SELECT_ALL_ADDRESSES = "SELECT id, Person, Street, Building, Office FROM addresses ORDER BY id"

address = Blueprint('address', __name__, template_folder='templates')


@address.route('/api/country/<idCountry>/region/<idRegion>/city/<idCity>/address', methods=('GET', 'POST'))
def create_address_in_city(idCountry, idRegion, idCity):
    if request.method == 'POST':
        data = request.get_json()
        Person = data["Person"]
        Street = data["Street"]
        Building = data["Building"]
        Office = data["Office"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_ADDRESSES_TABLE)
                cursor.execute(INSERT_ADDRESS, (Person, Street, Building, Office, idCity, ))
        return {"message": f"Адрес клиента {Person} добавлен."}, 201
    elif request.method == 'GET':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_ALL_ADDRESSES_IN_CITY, idCity)
                addresses = cursor.fetchall()
                ads = []
                for address in addresses:
                    cursor.execute(SELECT_CITY_BY_ID, (address[5],))
                    curcity = cursor.fetchone()[1]
                    dict = {"id": address[0], "Person": address[1], "Street": address[2], "Building": address[3],
                            "Office": address[4], "CityID": curcity}
                    ads.append(dict)
                return {"addresses": ads}, 200


@address.route('/api/country/<idCountry>/region/<idRegion>/city/<idCity>/address/<idAddress>',
               methods=('GET', 'DELETE', 'PUT'))
def get_address_in_city(idCountry, idRegion, idCity, idAddress):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ADDRESS_BY_ID, (idAddress,))
            address = cursor.fetchone()
            id = address[0]
            Person = address[1]
            Street = address[2]
            Building = address[3]
            Office = address[4]
            CityID = address[5]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_CITIES)
            cities = cursor.fetchall()
    if request.method == 'GET':
        return {"id": id, "Person": Person, "Street": Street, "Building": Building, "Office": Office, "CityID": CityID}, 200
    elif request.method == 'DELETE':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DELETE_ADDRESS, (idAddress,))
        return {"message": f"Адрес клиента {Person} удалён."}, 200
    elif request.method == 'PUT':
        data = request.get_json()
        newPerson = data["newPerson"]
        newStreet = data["newStreet"]
        newBuilding = data["newBuilding"]
        newOffice = data["newOffice"]
        newCityID = data["newidCity"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(EDIT_ADDRESS, (newPerson, newStreet, newBuilding, newOffice, newCityID, idAddress, ))
        return {"message": f"Адрес клиента {newPerson} отредактирован."}, 200


@address.route('/api/address', methods=('GET', 'POST'))
def create_address():
    if request.method == 'POST':
        data = request.get_json()
        Person = data["Person"]
        Street = data["Street"]
        Building = data["Building"]
        Office = data["Office"]
        CityID = data["CityID"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_ADDRESSES_TABLE)
                cursor.execute(SELECT_CITY_BY_ID, (CityID,))
                cityid = cursor.fetchone[0]
                cursor.execute(INSERT_ADDRESS, (Person, Street, Building, Office, cityid, ))
        return {"message": f"Адрес клиента {Person} добавлен."}, 201
    elif request.method == 'GET':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_ALL_ADDRESSES)
                # transform result
                columns = list(cursor.description)
                result = cursor.fetchall()
                # make dict
                results = []
                for row in result:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        row_dict[col.name] = row[i]
                    results.append(row_dict)
                # display
                s = type(result[0])
                return results




@address.route('/api/address/<idAddress>',
               methods=('GET', 'DELETE', 'PUT'))
def get_address(idAddress):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_CITIES)
            cities = cursor.fetchall()
            cursor.execute(SELECT_ADDRESS_BY_ID, (idAddress,))
            address = cursor.fetchone()
            id = address[0]
            Person = address[1]
            Street = address[2]
            Building = address[3]
            Office = address[4]
            CityID = address[5]
    if request.method == 'GET':
        return {"id": id, "Person": Person, "Street": Street, "Building": Building, "Office": Office, "CityID": CityID}, 200
    elif request.method == 'DELETE':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DELETE_ADDRESS, (idAddress,))
        return {"message": f"Адрес клиента {Person} удалён."}, 200
    elif request.method == 'PUT':
        data = request.get_json()
        newPerson = data["newPerson"]
        newStreet = data["newStreet"]
        newBuilding = data["newBuilding"]
        newOffice = data["newOffice"]
        newCityID = data["newidCity"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(EDIT_ADDRESS, (newPerson, newStreet, newBuilding, newOffice, newCityID, idAddress, ))
        return {"message": f"Адрес клиента {newPerson} отредактирован."}, 200
