import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestClearbit(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}
        self.maxDiff=None

        null='null'
        false='false'

        self.body={
            "email":"dzenan.kosuta@triglav.rs"
        }
        self.exit={
            "Dodatne informacije o korisniku": {
                "company": {
                    "category": {
                        "industry": "Insurance",
                        "industryGroup": "Insurance",
                        "naicsCode": "52",
                        "sector": "Financials",
                        "sicCode": null,
                        "subIndustry": "Insurance"
                    },
                    "crunchbase": {
                        "handle": null
                    },
                    "description": null,
                    "domain": "triglav.rs",
                    "domainAliases": [],
                    "emailProvider": false,
                    "facebook": {
                        "handle": null,
                        "likes": null
                    },
                    "foundedYear": null,
                    "geo": {
                        "city": "Beograd",
                        "country": "Serbia",
                        "countryCode": "RS",
                        "lat": 44.8197544,
                        "lng": 20.4551462,
                        "postalCode": null,
                        "state": null,
                        "stateCode": null,
                        "streetName": "Kralja Petra",
                        "streetNumber": "28",
                        "subPremise": null
                    },
                    "id": "f9e06ee3-bc08-46be-81b1-8f6d2247d24b",
                    "identifiers": {
                        "usEIN": null
                    },
                    "indexedAt": "2021-10-02T23:44:37.494Z",
                    "legalName": null,
                    "linkedin": {
                        "handle": "company/triglav-osiguranje-beograd"
                    },
                    "location": "Kralja Petra 28, Beograd, Serbia",
                    "logo": null,
                    "metrics": {
                        "alexaGlobalRank": 1290165,
                        "alexaUsRank": null,
                        "annualRevenue": null,
                        "employees": 210,
                        "employeesRange": "51-250",
                        "estimatedAnnualRevenue": "$10M-$50M",
                        "fiscalYearEnd": null,
                        "marketCap": null,
                        "raised": null,
                        "roleCounts": {
                            "marketing": "1-10"
                        }
                    },
                    "name": "Triglav osiguranje ADO Beograd",
                    "parent": {
                        "domain": null
                    },
                    "phone": null,
                    "site": {
                        "emailAddresses": [
                            "korisnickicentar@triglav.rs",
                            "office@triglav.rs",
                            "zdravstveno.osiguranje@triglav.rs"
                        ],
                        "phoneNumbers": [
                            "+381 11 3305150",
                            "+381 11 3305100",
                            "+381 11 3122420"
                        ]
                    },
                    "tags": [
                        "Insurance"
                    ],
                    "tech": [
                        "microsoft_exchange_online",
                        "facebook_advertiser",
                        "outlook",
                        "microsoft_office_365",
                        "google_analytics",
                        "highcharts",
                        "facebook_connect",
                        "apache",
                        "mailgun"
                    ],
                    "techCategories": [
                        "email_hosting_service",
                        "advertising",
                        "productivity",
                        "analytics",
                        "data_visualization",
                        "authentication_services",
                        "web_servers",
                        "email_delivery_service"
                    ],
                    "ticker": null,
                    "timeZone": "Europe/Belgrade",
                    "twitter": {
                        "avatar": null,
                        "bio": null,
                        "followers": null,
                        "following": null,
                        "handle": null,
                        "id": null,
                        "location": null,
                        "site": null
                    },
                    "type": "private",
                    "ultimateParent": {
                        "domain": null
                    },
                    "utcOffset": 2
                },
                "person": null
            }
        }

    def test_cbit(self,client):
        resp = client.get('/cbit', json=self.body, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
