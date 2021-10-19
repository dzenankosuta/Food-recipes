import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestSearchByText(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}

    def test_search_by_1name(self,client):
        resp = client.get('/search_by_name', headers=self.headers)
        self.assertEqual(resp.status_code, 200)

    def test_search_by_2text(self,client):
        resp = client.get('/search_by_text', headers=self.headers)
        self.assertEqual(resp.status_code, 200)

    def test_search_by_3ingredients(self,client):
        resp = client.get('/search_by_ingredients', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
