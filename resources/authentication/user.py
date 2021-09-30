import flask
from http import HTTPStatus
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort, request
from urllib.parse import parse_qs
import json
import psycopg2
import resources.errors as errors
from resources.db_connector import get_connection


class User(Resource):

    def get(self):
        pass

    def post(self):
        # print(request.form.get("bla"))
        fullname = self.getFormValue("fullname")
        city = self.getFormValue("city")
        identity = self.getFormValue("identity")
        password = self.getFormValue("password")
        phone = self.getFormValue("phone")
        role = self.getFormValue("role")
        if fullname is None or city is None or identity is None or password is None or phone is None or not self.isValidRole(
                role):
            raise errors.InvalidUser()
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(f"insert into users(id, fullname, city, identity, password, phone, role) values (DEFAULT, '{fullname}', '{city}', '{identity}', '{password}', '{phone}', '{role}')")
            connection.commit()
        except Exception:
            raise errors.InternalServerError
        return "ok",

    def getFormValue(self, param):
        return request.form.get(param)

    def isValidRole(self, role):
        return (role is not None) and (type(role) == int or role.isnumeric()) and (0 <= int(role) <= 3)
