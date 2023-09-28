import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scopes you need
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Function to authorize and create a calendar service
def authorize_and_create_service():
    """Authorizes and creates a calendar service."""

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'verification.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build and return the Google Calendar service
    service = build('calendar', 'v3', credentials=creds)
    return service

if __name__ == '__main__':
    # Create the Google Calendar service
    service = authorize_and_create_service()

    try:

        task = {
            'name': 'Appointment',
            'location': 'Somewhere',
            'start': {
                'dateTime': '2023-06-03T10:00:00.000-07:00',
                'timeZone': 'America/Los_Angeles'
            },
            'end': {
                'dateTime': '2011-06-03T10:25:00.000-07:00',
                'timeZone': 'America/Los_Angeles'
             },
             'recurrence': [
                'RRULE:FREQ=WEEKLY;UNTIL=20230928T170000Z',
            ],
        }

        recurring_event = service.events().insert(calendarId='primary', body=task).execute()

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
  authorize_and_create_service()