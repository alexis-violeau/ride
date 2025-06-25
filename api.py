BASE_URL = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/"

SYSTEM_INFO = "system_information.json"
CURRENT = "gbfs.json"
STATION_STATUS = "station_status.json"
STATION_INFO = "station_information.json"

import geopandas as gpd
import pandas as pd
from sqlalchemy.engine.base import Engine
from typing import Literal


def load_api_response(layer: str) -> dict | None:
    import requests

    response = requests.get(BASE_URL + layer)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to load station information: {response.status_code}")


def parse_api_reponse(reponse_dict: dict) -> pd.DataFrame:
    return pd.json_normalize(reponse_dict, record_path=["data", "stations"])


def parse_station_info(station_info: dict) -> gpd.GeoDataFrame:
    station_info = parse_api_reponse(station_info)
    return gpd.GeoDataFrame(
        data=station_info,
        geometry=gpd.points_from_xy(station_info.lon, station_info.lat),
        crs="EPSG:4326",
    )


def save_station_info(station_info: gpd.GeoDataFrame, con: Engine) -> None:
    station_info[["station_id", "name", "capacity", "geometry"]].to_postgis(
        name="velib_stations", con=con, index=False, if_exists="replace"
    )


def save_station_status(station_status: pd.DataFrame, con: Engine) -> None:
    station_status[["station_id", "update_time", "num_bikes_available"]].to_sql(
        name="velib_station_status", con=con, index=False, if_exists="append"
    )
