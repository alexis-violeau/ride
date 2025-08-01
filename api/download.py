import requests
from typing import Any, Dict

API_URL = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole"

def download_data() -> Dict[str, Any]:
    """
    Downloads the latest station status data from the Velib API.
    """
    response = requests.get(f"{API_URL}/station_status.json")
    response.raise_for_status()
    return response.json()
