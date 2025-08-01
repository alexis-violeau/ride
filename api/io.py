from typing import Any, List, Dict

def upload_to_db(data: List[Dict[str, Any]], conn, dt) -> None:
    """
    Uploads station data to the velib table, including request timestamp.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS velib (
                station_id TEXT PRIMARY KEY,
                n_bikes_available INTEGER,
                request_time TIMESTAMP
            )
            """
        )
        for item in data:
            cur.execute(
                """
                INSERT INTO velib (station_id, n_bikes_available, request_time)
                VALUES (%s, %s, %s)
                ON CONFLICT (station_id) DO NOTHING
                """,
                (str(item.get("station_id")), item.get("numBikesAvailable"), dt),
            )
    conn.commit()
