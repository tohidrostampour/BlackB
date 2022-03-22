import json

from fastapi import status

from tests.conftest import client, app, db_session


USER_REGISTER = '/auth/register'

user_data = {
    "name": "test user register",
    "username": "register",
    "email": "register@gmail.com",
    "password": "test"
}


def test_user_register(client):
    global user_data

    response = client.post(USER_REGISTER, json.dumps(user_data))

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['username'] == user_data['username']
