import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestSearchByText(flask_unittest.ClientTestCase):

    app=create_app()


    def setUp(self,client):
        resp = client.post('/login', json={"username":"dzenankosuta","password":"afc14"})
        token= resp.get_json()[0]["token"]
        client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token


    def test_search_by_1name(self,client):
        resp = client.get('/search_by_name')
        self.assertEqual(resp.status_code, 200)

    def test_search_by_2text(self,client):
        resp = client.get('/search_by_text')
        self.assertEqual(resp.status_code, 200)

    def test_search_by_3ingredients(self,client):
        resp = client.get('/search_by_ingredients')
        self.assertEqual(resp.status_code, 200)
