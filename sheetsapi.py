from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


# If modifying these scopes, delete the file token.json.

class table:

    def __init__(self):
        self.waitList = []
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'keys.json'
        self.SPREADSHEET_ID = '1oba360gqYTp2QFqMIgLwzE4VHiYJr-1VPXpwHtIJ488'

        self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        self.service = build('sheets', 'v4', credentials=self.credentials)

        self.sheets = self.service.spreadsheets()

    def getTable(self, col):
        x = self.sheets.values().get(spreadsheetId=self.SPREADSHEET_ID, range=str(col)).execute()
        return x

    def check_status(self):
        x = self.sheets.values().get(spreadsheetId=self.SPREADSHEET_ID, range="A1:J2000").execute()
        rows = x.get('values', []) #[a,b,c,r]
        remove = []
        for x in rows:
            self.waitList.append(x)
            print(x)
        for t in range(0,len(self.waitList)):
            g = self.waitList[t]
            if not(g[-1] == "Bekleniyor"):
                remove.append(self.waitList[t])

        for r in remove:
            if self.waitList.__contains__(r):
                self.waitList.remove(r)

        self.waitList.pop(0)

        print(self.waitList)



a = table()
a.check_status()
