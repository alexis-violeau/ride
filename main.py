from api.download import download_data
from api.sql_utils import get_connection
from api.io import upload_to_db
import datetime


def main() -> None:
    data = download_data()
    conn = get_connection()
    try:
        dt = data["lastUpdatedOther"]
        dt = datetime.datetime.fromtimestamp(dt)
        print(f"Data last updated at: {dt}")
        # Pass the datetime to upload_to_db
        upload_to_db(data["data"]["stations"], conn, dt)
        print("Data downloaded and saved successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
