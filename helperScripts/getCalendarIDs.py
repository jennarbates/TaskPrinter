import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def list_calendars():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    service = build('calendar', 'v3', credentials=creds)

    print("Fetching your calendars...\n")
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            name = calendar_list_entry['summary']
            cal_id = calendar_list_entry['id']
            print(f"Name: {name}")
            print(f"ID:   {cal_id}")
            print("-" * 30)
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

if __name__ == '__main__':
    list_calendars()
