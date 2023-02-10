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
        self.SPREADSHEET_ID = 'security'

        self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        self.service = build('sheets', 'v4', credentials=self.credentials)

        self.sheets = self.service.spreadsheets()

    def getTable(self, col):
        x = self.sheets.values().get(spreadsheetId=self.SPREADSHEET_ID, range=str(col)).execute()
        return x

    # 0 = isim, 1 = adres, -1 = tamamlandı mı
    def check_status(self):
        x = self.sheets.values().get(spreadsheetId=self.SPREADSHEET_ID, range="A1:J2000").execute()
        rows = x.get('values', []) #[a,b,c,r]
        print(rows)
        for x in rows:
            self.waitList.append(x)

        self.waitList.pop(0)

        return self.waitList

    def set_status(self,message,col):
        request = self.sheets.values().update(spreadsheetId=self.SPREADSHEET_ID, range=col,
                                              valueInputOption="USER_ENTERED", body={"values": message})
        request.execute()




a = table()
a.check_status()
