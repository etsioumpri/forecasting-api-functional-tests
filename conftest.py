import os
import pytest

@pytest.fixture
def api_url():

    return os.getenv("FORECASTING_API_URL",
                    "http://127.0.0.1:8000")

@pytest.fixture
def api_headers():

    api_key = os.getenv("FORECASTING_API_KEY")

    if not api_key:

        raise RuntimeError("FORECASTING_API_KEY environment variable not set")

    return {"X-Api-Key": api_key}

# for gd_lic
# @pytest.fixture
# def valid_request():
#
#     return {
#         "meter": os.getenv("FORECASTING_API_METER"),
#         "site": os.getenv("FORECASTING_API_SITE"),
#         "start_time": os.getenv("FORECASTING_API_START_TIME"),
#     }
#for enbro
@pytest.fixture
def valid_request():

    return {
        "location": os.getenv("FORECASTING_API_LOCATION"),
        "start_time": os.getenv("FORECASTING_API_START_TIME"),
    }