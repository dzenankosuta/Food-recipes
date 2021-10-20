import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestRecipeWithMaxIng(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        resp = client.post('/login', json={"username":"dzenankosuta","password":"afc14"})
        token= resp.get_json()[0]["token"]
        client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token



    def test_max_ingredients(self,client):
        resp = client.get('/max_ingredients')
        self.assertEqual(resp.status_code, 200)

    def test_min_ingredients(self,client):
        resp = client.get('/min_ingredients')
        self.assertEqual(resp.status_code, 200)
