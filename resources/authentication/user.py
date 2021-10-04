import flask
from http import HTTPStatus
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort, request
from urllib.parse import parse_qs
import json
import psycopg2
import resources.errors as errors
from resources.db_connector import get_connection
from passlib.hash import sha256_crypt


class User(Resource):

    def get(self):
        # print(request.args)
        phone = request.args.get('phone')
        if phone is None or not (type(phone) == int or phone.isnumeric()):
            raise errors.NoSuchUser
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"select fullname, city, identity, phone, role from users where phone=%(phone)s;", {
            'phone': phone
        })
        user = cursor.fetchall()
        if len(user) == 0:
            raise errors.NoSuchUser

        return {
                   "fullname": user[0][0],
                   "city": user[0][1],
                   "identity": user[0][2],
                   "phone": user[0][3],
                   "role": user[0][4],
               }, HTTPStatus.OK

    def post(self):
        # print(request.form.get("bla"))
        fullname = self.getFormValue("fullname")
        city = self.getFormValue("city")
        identity = self.getFormValue("identity")
        password = self.getFormValue("password")
        phone = self.getFormValue("phone")
        role = self.getFormValue("role")
        if fullname is None or city is None or identity is None or password is None or phone is None or not self.isValidRole(
                role) or not self.isNumber(phone):
            raise errors.InvalidUser()
        # try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from users where phone=%(phone)s", {'phone': phone})
        if len(cursor.fetchall()) != 0:
            raise errors.PhoneAlreadyTaken
        cursor.execute(
            "insert into users(id, fullname, city, identity, password, phone, role) values (DEFAULT, %(fullname)s, %(city)s, %(identity)s, %(password)s, %(phone)s, %(role)s);",
            {
                'fullname': fullname,
                'city': 'city',
                'identity': identity,
                'password': self.hash_password(password),
                'phone': phone,
                'role': role
            })
        connection.commit()
        # except Exception:
        #     raise errors.InternalServerError
        return "ok",

    @staticmethod
    def getFormValue(param):
        return request.form.get(param)

    def isValidRole(self, role):
        return (role is not None) and self.isNumber(role) and (0 <= int(role) <= 3)

    @staticmethod
    def isNumber(value):
        return type(value) == int or value.isnumeric()

    @staticmethod
    def hash_password(password):
        return sha256_crypt.hash(password)
