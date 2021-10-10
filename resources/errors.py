from http import HTTPStatus
from flask_restful import HTTPException

auth_error_dict = {"message": "Access Denied"}


class NoSuchUser(HTTPException):
    pass


class PasswordIsTooShort(HTTPException):
    pass


class PhoneAlreadyTaken(HTTPException):
    pass


class InvalidAPIToken(HTTPException):
    pass


class APITokenExpired(HTTPException):
    pass


class InternalServerError(HTTPException):
    pass


class NoSuchStory(HTTPException):
    pass


class NoSuchEvent(HTTPException):
    pass


class TagAlreadyExists(HTTPException):
    pass


class EventAlreadyExists(HTTPException):
    pass


class StoryAlreadyExists(HTTPException):
    pass


class NotAuthorized(HTTPException):
    pass


class CantParticipateInOwnEvent(HTTPException):
    pass


class NoSuchParticipant(HTTPException):
    pass


class InvalidUser(HTTPException):
    pass


class InvalidTitleForEvent(HTTPException):
    pass


errors = {
    "NoSuchUser": {
        "message": "No user was found with the given data",
        "status": HTTPStatus.NOT_FOUND
    },
    "PasswordIsTooShort": {
        "message": "Given password is shorter than 10 characters",
        "status": HTTPStatus.BAD_REQUEST
    },
    "InvalidTitleForEvent": {
        "message": "Please add title to the event",
        "status": HTTPStatus.BAD_REQUEST
    },
    "PhoneAlreadyTaken": {
        "message": "This phone is taken",
        "status": HTTPStatus.BAD_REQUEST
    },
    "InvalidAPIToken": {
        "message": "Invalid API Token",
        "status": HTTPStatus.UNAUTHORIZED
    },
    "APITokenExpired": {
        "message": "API Token expired",
        "status": HTTPStatus.UNAUTHORIZED
    },
    "InternalServerError": {
        "message": "An internal server error occurred",
        "status": HTTPStatus.INTERNAL_SERVER_ERROR
    },
    "NoSuchStory": {
        "message": "No such story was found",
        "status": HTTPStatus.NOT_FOUND
    },
    "NoSuchEvent": {
        "message": "No such event was found",
        "status": HTTPStatus.NOT_FOUND
    },
    "TagAlreadyExists": {
        "message": "Tag already exists",
        "status": HTTPStatus.SEE_OTHER
    },
    "EventAlreadyExists": {
        "message": "Event already exists",
        "status": HTTPStatus.SEE_OTHER
    },
    "StoryAlreadyExists": {
        "message": "Story already exists",
        "status": HTTPStatus.SEE_OTHER
    },
    "NotAuthorized": {
        "message": "Access Denied",
        "status": HTTPStatus.UNAUTHORIZED
    },
    "CantParticipateInOwnEvent": {
        "message": "You can't participate in your own event",
        "status": HTTPStatus.BAD_REQUEST
    },
    "NoSuchParticipant": {
        "message": "This is not a participant of that event",
        "status": HTTPStatus.BAD_REQUEST
    },
    "InvalidUser": {
        "message": "Bad user parameters",
        "status": HTTPStatus.BAD_REQUEST
    }
}
