from dataclasses import dataclass
from datetime import date
from tqdm import tqdm


@dataclass
class PlaylistItem:
    title: str
    description: str
    id: str


@dataclass
class Playlist:
    title: str
    description: str
    items: list[PlaylistItem]


def fetch_playlist(youtube, playlist_id) -> Playlist:
    "Retrieve a playlist and its items."

    response = youtube.playlists().list(part="snippet", id=playlist_id).execute()
    playlist_snippet = response["items"][0]["snippet"]

    items = []

    page_token = None
    while True:
        response = (
            youtube.playlistItems()
            .list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page_token,
            )
            .execute()
        )

        for item in response["items"]:
            snippet = item["snippet"]

            items.append(
                PlaylistItem(
                    title=snippet["title"],
                    description=snippet["description"],
                    id=snippet["resourceId"]["videoId"],
                )
            )

        page_token = response.get("nextPageToken")

        if page_token is None:
            break

    return Playlist(
        title=playlist_snippet["title"],
        description=playlist_snippet["description"],
        items=items,
    )


@dataclass
class Event:
    date: date
    title: str
    description: str
    source: str


def create_calendar(calendar, name: str) -> str:
    "Create a new secondary calendar and returns its ID."

    response = calendar.calendars().insert(body={"summary": name}).execute()
    return response["id"]


def create_events(calendar, calendar_id: str, events: list[Event]) -> None:
    for event in tqdm(events):
        body = {
            "summary": event.title,
            "description": event.description,
            "start": {
                "date": event.date.strftime("%Y-%m-%d"),
            },
            "end": {
                "date": event.date.strftime("%Y-%m-%d"),
            },
            "source.url": event.source,
        }

        calendar.events().insert(
            calendarId=calendar_id,
            body=body,
        ).execute()
