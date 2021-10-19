import flask_unittest
from app import create_app
from flask import request,json
import requests



class TestProsek(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}
        self.maxDiff=None

        self.exit={
            "Prosečne ocene recepata su": [
                [
                    "Naziv recepta: corba",
                    "Prosečna ocena je: None"
                ],
                [
                    "Naziv recepta: piroska",
                    "Prosečna ocena je: 2.0"
                ],
                [
                    "Naziv recepta: pizza",
                    "Prosečna ocena je: 5.0"
                ],
                [
                    "Naziv recepta: sladoled",
                    "Prosečna ocena je: 2.5"
                ],
                [
                    "Naziv recepta: torta",
                    "Prosečna ocena je: 4.0"
                ]
            ]
        }

    def test_prosek(self,client):
        resp = client.get('/prosek', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
