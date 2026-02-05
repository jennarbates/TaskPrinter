import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from escpos.printer import Usb

# --- CONFIGURATION ---
# Your Printer IDs
VENDOR_ID = 0x0fe6
PRODUCT_ID = 0x811e

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_next_events():
    """Fetches the next 5 events from the primary calendar."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Login flow for the first run
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Get events from "Now" onwards
    now = datetime.datetime.utcnow().isoformat() + 'Z' 
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=5, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def print_floral_tasks(events):
    try:
        p = Usb(VENDOR_ID, PRODUCT_ID)
        
        # Floral ASCII Art
        flower_line = "   (@)   (@)   (@)   \n"
        vine_line   = "~^~^~^~^~^~^~^~^~^~^~\n"
        leaf_accent = "      \\  |  /      \n"

        if not events:
            # Simple message if nothing is scheduled
            p.text("\n\n")
            p.set(align='center', bold=True, width=2, height=2)
            p.text("No Tasks\n")
            p.text("Relax.\n")
            p.text("\n\n")
            p.cut()
            return

        for event in events:
            # 1. Parse Time & Title
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event['summary']
            
            # Format time (e.g., "2:30 PM")
            if 'T' in start:
                dt = datetime.datetime.fromisoformat(start)
                time_str = dt.strftime("%I:%M %p").lstrip('0') # "2:30 PM"
            else:
                time_str = "All Day"

            # 2. Print The Card
            p.set(align='center')
            p.text("\n") 
            
            # Top Vines
            p.set(font='b', align='center')
            p.text(vine_line)
            p.text(flower_line)
            p.text(vine_line)
            p.text("\n")

            # The Task (Big & Bold)
            p.set(font='a', align='center', bold=True, width=2, height=2)
            p.text(f"{summary}\n")
            
            # The Time (Smaller, below task)
            p.set(font='b', align='center', bold=False, width=1, height=1)
            p.text(f"- {time_str} -\n")

            # Bottom Vines
            p.set(font='a', align='center') # Reset for spacing
            p.text("\n")
            p.set(font='b')
            p.text(leaf_accent)
            p.text(vine_line)
            
            # Cut
            p.text("\n\n")
            p.cut()

    except Exception as e:
        print(f"Printer Error: {e}")

if __name__ == '__main__':
    print("Fetching Calendar...")
    my_events = get_next_events()
    if my_events:
        print(f"Found {len(my_events)} events. Printing...")
        print_floral_tasks(my_events)
    else:
        print("No events found.")
