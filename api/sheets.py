# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from google.oauth2.credentials import Credentials

# # Set up credentials for Google Sheets API
# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# creds = Credentials.from_authorized_user_file('client_secret_814875837614-310nsvg2nnd5iu68btuq5knrrh24gf2h.apps.googleusercontent.com.json', scope)
# # client = gspread.authorize(creds)

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1JtOwB0UfJHJWdaePdEzsjEEoGRnjC5rkJBNOc6ARgw8'
RANGE_NAME = 'Data!A2:E'

def main():
    creds = authenticate()
    read_sheet(creds)
    append_to_sheet(creds, 'Samitha', '', 'samitha.312@gmail.com', '0414885443', '123 Smith Street, Cranbourne')

def authenticate():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

    

def read_sheet(creds):
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Name, Company, Email, Mobile, Address:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)
    except HttpError as err:
        print(err)

def append_to_sheet(creds, name, company, email, mobile, address):
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        value_input_option = 'RAW'
        insert_data_option = 'INSERT_ROWS'
        value_range_body = {
            "range": RANGE_NAME,
            "values": [
                [name, company, email, mobile, address]
            ]
        }

        request = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
        response = request.execute()

        print(response)
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
