import requests
import time
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session():
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )

    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    return session


def get_auth_headers():
    """
    Supports Bearer token authentication
    """
    token = os.getenv("API_TOKEN")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def fetch_data():
    session = create_session()
    url = "https://jsonplaceholder.typicode.com/posts"

    headers = get_auth_headers()
    all_data = []
    page = 1
    limit = 20

    while True:
        params = {"_page": page, "_limit": limit}
        response = session.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        if not data:
            break

        all_data.extend(data)
        page += 1
        time.sleep(1)

    return all_data
