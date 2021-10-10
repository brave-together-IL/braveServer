import flask
from http import HTTPStatus
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort, request
from urllib.parse import parse_qs
import json
import psycopg2
import resources.errors as errors
from resources.db_connector import get_connection


class Event(Resource):

    def get(self):
        tags = request.args.getlist('tags')
        if tags is not None:
            connection = get_connection()
            cursor = connection.cursor()
            raw_data = []
            for i in range(len(tags)):
                cursor.execute("select * from events where %(tag)s=any(tags)", {'tag': tags[i]})
                raw_data.extend(cursor.fetchall())
            data = self.removeDuplicates(raw_data)
            return self.events_list_to_json(data), HTTPStatus.OK
        title = request.args.get('title')
        if title is not None:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("select * from events where %(title)s", {'title': title})
            raw_data = cursor.fetchall()
            data = self.removeDuplicates(raw_data)
            return self.events_list_to_json(data)
        raise errors.NoSuchEvent

    def post(self):
        title = self.getFormValue("title")
        description = self.getFormValue("description") or ""
        tags = request.form.getlist("tags") or []
        start_time = self.getFormValue("start_time") or ""
        end_time = self.getFormValue("end_time") or ""
        geolocation = self.getFormValue("geolocation") or ""
        participatedId = self.getFormValue("participatedId") or -1
        if title is None:
            raise errors.InvalidTitleForEvent
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from events where title=%(title)s", {'title': title})
        if len(cursor.fetchall()) != 0:
            raise errors.EventAlreadyExists
        cursor.execute(
            "insert into events(id, title, description, tags, start_time, end_time, geolocation, participatedId) values (DEFAULT, %(title)s, %(description)s, %(tags)s, %(start_time)s, %(end_time)s, %(geolocation)s, %(participatedId)s);",
            {
                'title': title,
                'description': description,
                'tags': tags,
                'start_time': start_time,
                'end_time': end_time,
                'geolocation': geolocation,
                'participatedId': participatedId
            })
        connection.commit()
        return "ok", HTTPStatus.OK

    @staticmethod
    def getFormValue(param):
        return request.form.get(param)

    @staticmethod
    def events_list_to_json(events: list[tuple]):
        data = []
        for title, description, tags, start_time, end_time, geolocation, participatedId, id in events:
            data.append({
                "title": title,
                "description": description,
                "tags": tags,
                "start_time": start_time,
                "end_time": end_time,
                "geolocation": geolocation,
                "participatedId": participatedId,
                "id": id
            })
        return data

    @staticmethod
    def removeDuplicates(arr: list):
        data = []
        [data.append(x) for x in arr if x not in data]
        return data
