import httpx
import sqlite3
from contextlib import closing
from collections import namedtuple
from prefect import flow, task

ArtistData = namedtuple("ArtistData", ["name", "listeners", "tags"])


# Extract
@task
def fetch_stats(artist_name: str):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": "meow",
        "format": "json"
    }
    response = httpx.get(url, params=params)
    return response.json()


# Transform
@task
def parse_artist_data(raw_data, artist_name):
    artist_info = raw_data.get("artist", {})

    listeners = artist_info.get("stats", {}).get("listeners", "N/A")

    # Extrae los tags de manera segura
    tag_list = artist_info.get("tags", {}).get("tag", [])
    tags = [tag["name"] for tag in tag_list] if isinstance(tag_list, list) else []

    return ArtistData(name=artist_name, listeners=listeners, tags=", ".join(tags))


# Load
@task
def store_artists(parsed_data):
    create_script = '''CREATE TABLE IF NOT EXISTS artists (
        name TEXT PRIMARY KEY,
        listeners INTEGER,
        tags TEXT
    )'''
    insert_cmd = "INSERT OR REPLACE INTO artists VALUES (?, ?, ?)"

    with closing(sqlite3.connect("lastfm.db")) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executescript(create_script)
            cursor.executemany(insert_cmd, [parsed_data])
            conn.commit()


# Flow principal
@flow(log_prints=True)
def show_ratings(artist_names: list[str]):
    for artist in artist_names:
        raw_data = fetch_stats(artist)
        parsed_data = parse_artist_data(raw_data, artist)
        store_artists(parsed_data)
        print(f"{artist}: {parsed_data.listeners} oyentes | Tags: {parsed_data.tags}")


if __name__ == "__main__":
    show_ratings([
        "Tool",
        "Nine Inch Nails",
        "KMFDM", 
        "David Bowie",
    ])
