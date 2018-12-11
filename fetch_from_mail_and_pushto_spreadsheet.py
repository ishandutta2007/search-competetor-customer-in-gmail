import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from apiclient import errors, discovery
import csv
import codecs
import random
import email
import constants

import requests
import csv

import urllib.error
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import time
import gspread

from oauth2client.service_account import ServiceAccountCredentials

query_term = "\"SDE 4\""

def get_service_account_credentials():
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('bigbullscollab-55669a1c65c2.json', scope)
    return credentials

def get_oath_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, constants.CREDENTIAL_FILE_NAME)
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(constants.CLIENT_SECRET_FILE, constants.SCOPES)
        flow.user_agent = constants.APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print(('Storing credentials to ' + credential_path))
    return credentials

def list_messages_matching_query(service, user_id, query=''):
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                    pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        # print('Message snippet: %s' % message['snippet'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def update_sheet(row, col, sheet_name, wk, val):
    try:
        wks = wk.worksheet(sheet_name)
    except Exception:
        wks = wk.add_worksheet(title=sheet_name, rows="100", cols="20")
        cell_list = wks.range('A1:B1')
        cell_list[0].value = 'Competetor'
        cell_list[1].value = 'Customor'
        wks.update_cells(cell_list)

    if row + 2 > wks.row_count:
        wks.add_rows(100)

    wks.update_cell(row+2, col, val)
    time.sleep(1)

def check_potential_competetor(totcomp, header, sheet_name, wk):
    if header['name']=='From':
        emails = header['value'].split(',')
        emails = map(str.strip, emails)
        emails = [x.strip(' ') for x in emails]
        emails.sort()
        for email in emails:
            print('From', email)
            update_sheet(totcomp, 1, sheet_name, wk, email)
            totcomp = totcomp + 1
    return totcomp

def check_potential_customer(totcust, header, sheet_name, wk):
    if header['name']=='Cc':
        emails = header['value'].split(',')
        emails = map(str.strip, emails)
        emails = [x.strip(' ') for x in emails]
        emails.sort()
        for email in emails:
            print('Cc', email)
            update_sheet(totcust, 2, sheet_name, wk, email)
            totcust = totcust + 1
    return totcust

def main():
    sheet_name = query_term.replace(' ','_')
    gc = gspread.authorize(get_service_account_credentials())
    wk = gc.open("competetor-customer-fetch-from-email")

    credentials = get_oath_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    messages = list_messages_matching_query(service, "me", query=query_term)
    totcust, totcomp = 0, 0
    for message in messages[]:
        print("\n" + message['id'] + ":\n")
        msg = get_message(service, "me", message['id'])
        headers = msg['payload']['headers']
        for header in headers:
            totcomp = check_potential_competetor(totcomp, header, sheet_name, wk)
            totcust = check_potential_customer(totcust, header, sheet_name, wk)

if __name__ == '__main__':
    main()
