import requests

from conftest import API_URL

def test_api_is_reachable():

    url = f"{API_URL}/forecast/gd_lic"

    response = requests.post(url,
                             json={"meter" : "LugaggiaInnovationCommunity",
                                   "site" : "LugaggiaInnovationCommunity",
                                   "start_time": "2026-09-15T00:00:00+00:00"},
                             timeout=90)

    assert response.status_code == 200