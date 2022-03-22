import json

from fastapi import status

from tests.conftest import client, app, db_session

data_1 = {
    'title': 'test post creation',
    'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi nec',
    'file': 'https://google.com'
}
data_2 = {
    'title': 'test num2',
    'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi nec',
    'file': 'https://google.com'
}

POST_CREATION = '/blog/create'


def test_create_post(client):
    global data_1
    response = client.post(POST_CREATION, json.dumps(data_1))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == data_1['title']


def test_get_post(client):
    global data_1
    client.post(POST_CREATION, json.dumps(data_1))

    response = client.get('blog/1')

    assert response.status_code == status.HTTP_200_OK


def test_get_all(client):
    client.post(POST_CREATION, json.dumps(data_1))
    client.post(POST_CREATION, json.dumps(data_2))

    response = client.get('/blog')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['title'] == data_1['title']
    assert response.json()[1]['title'] == data_2['title']
