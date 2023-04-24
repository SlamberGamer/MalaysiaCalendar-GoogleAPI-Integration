import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path
from googleapiclient.discovery import build
import datetime

# Replace these with your own credentials
SERVICE_ACCOUNT_FILE = 'YOUR_JSON_FILES'
SCOPES = ['https://www.googleapis.com/auth/calendar.events.readonly']

# Authenticate with the Google API

def create_calendar_client():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SERVICE_ACCOUNT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

# Define your date
date = datetime.date(2023, 3, 10)
date2 = datetime.date(2023, 4, 10)


# Get the holiday calendar ID for the specified country
calendar_id = 'en.malaysia#holiday@group.v.calendar.google.com'

# Fetch calendar data based on country and date
start_date = datetime.datetime.combine(date, datetime.time(0, 0, 0)).isoformat() + 'Z'
end_date = datetime.datetime.combine(date2, datetime.time(23, 59, 59)).isoformat() + 'Z'

create_calendar = create_calendar_client()

# now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

events = create_calendar.events().list(calendarId=calendar_id, timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()

print(events)

# Print the fetched events
# for event in events.get('items', []):
#     print(event['summary'], event['start']['dateTime'])

