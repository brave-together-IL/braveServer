import flask
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort, request
import datetime
from urllib.parse import parse_qs
import json
import psycopg2
import os
from resources.authentication.user import User
from resources.events.event import Event
from resources.errors import errors
from resources.db_connector import get_connection

connection = get_connection()
cursor = connection.cursor()
try:
    cursor.execute("select * from users")
    print("table users found")

except psycopg2.errors.UndefinedTable:
    print("Creating table users...")
    connection.rollback()
    cursor.execute('CREATE TABLE users (fullname varchar(50), city varchar(50), identity varchar(10), password text, phone varchar(12), role int, id SERIAL PRIMARY KEY)')
    connection.commit()

try:
    cursor.execute("select * from events")
    print("table events found")

except psycopg2.errors.UndefinedTable:
    print("Creating table events...")
    connection.rollback()
    cursor.execute('CREATE TABLE events (title varchar (50), description text, tags text[], start_time text, end_time text, geolocation text, participatedId int, id SERIAL PRIMARY KEY)')
    connection.commit()


app = Flask(__name__)
api = Api(app, errors=errors)


class App(Resource):
    def get(self):
        return r

    def post(self):
        return flask.jsonify(data)


api.add_resource(User, "/user")
api.add_resource(Event, "/event")

if __name__ == "__main__":
    app.run(debug=False)
