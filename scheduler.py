import datetime
import argparse
from api import (
    load_api_response,
    parse_api_reponse,
    save_station_status,
    STATION_STATUS,
)
from sql_utils import get_db_connection
import time
import schedule


def update_station_info():
    con = get_db_connection()
    raw_data = load_api_response(STATION_STATUS)
    dt = datetime.datetime.fromtimestamp(raw_data["lastUpdatedOther"])
    print(f"Parsing station status data... {dt=}")
    data = parse_api_reponse(raw_data)
    data["update_time"] = dt
    save_station_status(data, con)


if __name__ == "__main__":
    # code here runs only when the file is executed directly
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--interval", type=int, required=True, help="Interval between two calls"
    )
    args = parser.parse_args()

    schedule.every(args.interval).minutes.do(update_station_info)
    update_station_info()

    while True:
        schedule.run_pending()
        time.sleep(1)
