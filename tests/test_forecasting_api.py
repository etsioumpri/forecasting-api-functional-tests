import math
import os
import datetime
import requests

from conftest import valid_request

############################### API AVAILABILITY ##################################################
print("API AVAILABILITY TESTS")
def test_api_is_reachable(api_url, api_headers, valid_request):
    print("Testing that the forcasting API is accessible and does not return a server side error")

    url = f"{api_url}/forecast/gd_lic"

    response = requests.post(url,
                             json=valid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code < 500

############################### CORE FUNCTIONALITIES ################################################
print("CORE FUNCTIONALITY TESTS")
def test_valid_request_produces_successful_response(api_url, api_headers, valid_request):
    print("Testing that a valid request produces a successful response")

    url = f"{api_url}/forecast/gd_lic"

    response = requests.post(url,
                             json=valid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 200

def test_response_has_expected_structure(api_url, api_headers, valid_request):
    print("Testing that the response has the expected structure")

    url = f"{api_url}/forecast/gd_lic"

    response = requests.post(url,
                             json=valid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 200

    data = response.json()

    assert "meter" in data
    assert "start_time" in data
    assert "demand_forecast" in data

    assert isinstance(data["demand_forecast"], list)

def test_response_matches_request(api_url, api_headers, valid_request):
    print("Testing that the response contains the requested meter and start time")

    url = f"{api_url}/forecast/gd_lic"

    response = requests.post(url,
                             json=valid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 200

    data = response.json()

    assert data["meter"] == valid_request["meter"]
    assert data["start_time"] == valid_request["start_time"]

def test_forecast_points_have_required_fields(api_url, api_headers, valid_request):
    print("Testing that every forecast point is a dictionary with a timestamp, forecast, 5th and 95th percentiles")

    url = f"{api_url}/forecast/gd_lic"

    response = requests.post(url,
                             json=valid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 200

    data = response.json()

    for point in data["demand_forecast"]:

        assert isinstance(point, dict)
        assert "timestamp" in point
        assert "forecast" in point
        assert "p5" in point
        assert "p95" in point


def test_response_has_192_points(api_url, api_headers, valid_request):
    print("Testing that the response contains exactly 192 forecast points (48-hour ahead forecast at a 15-min resolution)")

    url = f"{api_url}/forecast/gd_lic"

    response = requests.post(url,
                             json=valid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 200

    data = response.json()

    assert len(data["demand_forecast"]) == 192

def test_forecasts_are_numerical_values(api_url, api_headers, valid_request):
    print("Testing that the forecast, 5th and 95th percentiles are valid numerical values")

    url = f"{api_url}/forecast/gd_lic"

    response = requests.post(url,
                             json=valid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 200

    data = response.json()

    for point in data["demand_forecast"]:

        forecast = point["forecast"]
        p5 = point["p5"]
        p95 = point["p95"]

        assert isinstance(forecast, (int, float))
        assert isinstance(p5, (int, float))
        assert isinstance(p95, (int, float))

        assert math.isfinite(forecast)
        assert math.isfinite(p5)
        assert math.isfinite(p95)

def test_consistent_prediction_intervals(api_url, api_headers, valid_request):
    print("Testing that the prediction intervals are consistent (p5 <= forecast <= 95th) for every forecast point")

    url = f"{api_url}/forecast/gd_lic"

    response = requests.post(url,
                             json=valid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 200

    data = response.json()

    for point in data["demand_forecast"]:
        assert point["p5"] <= point["forecast"] <= point["p95"]


def test_response_timestamps_are_valid(api_url, api_headers, valid_request):
    print("Testing that the timestamps are valid for every forecast point")

    url = f"{api_url}/forecast/gd_lic"

    response = requests.post(url,
                             json=valid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 200

    data = response.json()

    for point in data["demand_forecast"]:
        timestamp = point["timestamp"]

        assert isinstance(timestamp, str)

        datetime.datetime.fromisoformat(timestamp)

def test_datetimes_are_15min_apart(api_url, api_headers, valid_request):
    print("Testing that the timestamps of successive forecast points are 15 minutes apart")

    url = f"{api_url}/forecast/gd_lic"

    response = requests.post(url,
                             json=valid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 200

    data = response.json()

    forecasts = data["demand_forecast"]

    timestamps = [datetime.datetime.fromisoformat(point["timestamp"]) for point in forecasts]

    for current_timestamp, next_timestamp in zip(timestamps, timestamps[1:]):
        assert next_timestamp - current_timestamp == datetime.timedelta(minutes=15)


def test_identical_requests_produce_identical_responses(api_url, api_headers, valid_request):
    print("Testing that requests with identical input produce the same output")

    url = f"{api_url}/forecast/gd_lic"

    response_1 = requests.post(url,
                               json=valid_request,
                               headers=api_headers,
                               timeout=60)

    response_2 = requests.post(url,
                               json=valid_request,
                               headers=api_headers,
                               timeout=60)

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    data_1 = response_1.json()
    data_2 = response_2.json()

    assert data_1["demand_forecast"] == data_2["demand_forecast"]

############################### INPUT VALIDATION ####################################################
print("INPUT VALIDATION TESTS")
def test_request_without_meter_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with missing field 'meter' produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request.pop("meter")

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 422

def test_request_without_site_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with missing field 'site' produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request.pop("site")

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 422

def test_request_without_start_time_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with missing field 'start_time' produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request.pop("start_time")

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 422

def test_request_with_empty_meter_field_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with empty 'meter' field produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request["meter"] = None

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 422

def test_request_with_empty_site_field_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with empty 'site' field produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request["site"] = None

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 422

def test_request_with_empty_start_time_field_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with empty 'start_time' field produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request["start_time"] = None

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 422

def test_request_with_invalid_meter_type_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with invalid 'meter' type produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request["meter"] = ["invalid_type"]

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 422

def test_request_with_invalid_site_type_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with invalid 'site' type produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request["site"] = ["invalid_type"]

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 422

def test_request_with_invalid_start_time_type_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with invalid 'start_time' type produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request["start_time"] = ["invalid_type"]

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 422

def test_request_with_unsupported_meter_value_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with unsupported 'meter' value produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request["meter"] = "unsupported_meter_name"

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == f"Meter id {invalid_request['meter']} not valid for site {invalid_request['site']}"

def test_request_with_unsupported_site_value_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with unsupported 'site' value produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request["site"] = "unsupported_site_name"

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == f"Invalid site {invalid_request['site']}. Choose LugaggiaInnovationCommunity or GaramèDistrict."

def test_request_with_invalid_start_time_format_produces_appropriate_response(api_url, api_headers, valid_request):
    print("Testing that requests with invalid 'start_time' format produce the appropriate response")

    url = f"{api_url}/forecast/gd_lic"

    invalid_request = valid_request.copy()
    invalid_request["start_time"] = "2026/09/16 10:00:00+00:00"

    response = requests.post(url,
                             json=invalid_request,
                             headers=api_headers,
                             timeout=60)

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == f"Invalid start time format {invalid_request['start_time']}"
