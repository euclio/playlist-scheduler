from datetime import datetime, timedelta
import click
from playlist_scheduler.api import Event, create_calendar, create_events, fetch_playlist
from playlist_scheduler.auth import fetch_google_credentials

from googleapiclient.discovery import build


@click.command()
@click.argument("playlist_id")
def schedule_playlist(playlist_id):
    creds = fetch_google_credentials()

    youtube = build("youtube", "v3", credentials=creds)

    playlist = fetch_playlist(youtube, playlist_id)

    create = input(
        f"Are you sure you want to create a calendar for '{playlist.title}' with {len(playlist.items)} items [y/n]? "
    ).lower()
    if create not in ["y", "yes"]:
        print("Calendar not created.")
        return

    calendar = build("calendar", "v3", credentials=creds)

    calendar_id = create_calendar(calendar, playlist.title)

    events: list[Event] = []

    tomorrow = datetime.now() + timedelta(days=1)

    for i, item in enumerate(playlist.items):
        date = tomorrow + timedelta(days=i)

        events.append(
            Event(
                title=item.title,
                description=item.description,
                date=date,
                source=f"https://www.youtube.com/watch?v={item.id}&list={playlist_id}",
            )
        )

    create_events(calendar, calendar_id, events)

    print(f"Created calendar {calendar_id}")


def main() -> None:
    schedule_playlist()
