import os
import pytest

@pytest.fixture
def api_url():

    return os.getenv("FORECASTING_API_URL",
                    "https://localhost:8000")

@pytest.fixture
def api_headers():

    api_key = os.getenv("FORECASTING_API_KEY")

    if not api_key:

        raise RuntimeError("FORECASTING_API_KEY environment variable not set")

    return {"X-Api-Key": api_key}

@pytest.fixture
def valid_request():

    return {
        "meter": os.getenv("FORECASTING_API_METER"),
        "site": os.getenv("FORECASTING_API_SITE"),
        "start_time": os.getenv("FORECASTING_API_START_TIME"),
    }