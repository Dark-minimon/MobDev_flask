#import os
#import psycopg2
#from dotenv import load_dotenv
from flask import Flask, request
from flask_ngrok import run_with_ngrok # функция для доступа к приложению из сети
from pyngrok import ngrok

from country import country
from region import region
from city import city
from address import address

#load_dotenv()

app = Flask(__name__)
run_with_ngrok(app)
ngrok.set_auth_token('2MSW1UMdiqTtVnxv1YJnFKp0Ycq_22eGRH9hYSjhCySXhyHEK')
app.register_blueprint(country)
app.register_blueprint(region)
app.register_blueprint(city)
app.register_blueprint(address)
#url = os.getenv('DATABASE_URL')
#connection = psycopg2.connect(url)
#connection = psycopg2.connect(dbname="addressdb", user="postgres", password="87654321", host="127.0.0.1", port="5432")


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello world!'


if __name__ == '__main__':
    app.run()


