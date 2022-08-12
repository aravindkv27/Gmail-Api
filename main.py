#  A standalone Python script that integrates with GMail API and performs some rule based operations on emails.
#
#  Created By: Aravind K V
#  
#  Created On: August, 2022.
#
#  Source: https://youtu.be/vgk7Yio-GQw, https://www.thepythoncode.com/article/use-gmail-api-in-python
#
#

# importing required packages
from cProfile import label
from distutils.log import error
from email import message, parser
import json
import os
import pickle
import sqlite3
from typing import final
from unittest import result
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
import email
import base64
import dateutil.parser as parser

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
# SCOPES = ['https://mail.google.com/']

my_mail = "aravind27032002@gmail.com"

final_list = []

email_data = {}

label_names = []

# Connect to Database
def db_connection():

    conn = sqlite3.connect("Email.db")
    return conn



# Authentication to Gmail OAuth API
def gmail_authenticate():


    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service=  build('gmail', 'v1', credentials=creds)
    return service



# Search emails using label IDs
def search_messages(service, user_id, label_ids=[]):

    try:

        search_id = service.users().messages().list(userId=user_id, labelIds=label_ids).execute()

        # print(search_id)
        
        number_results = search_id['resultSizeEstimate']
        
        if number_results > 0:

            message_id = search_id['messages']

            for id in message_id:

                final_list.append(id['id'])

            return final_list

        else:

            print("There are no results in the search string")
            return "Empty"

            
    except errors.HttpError as error:

        print("An error occured: %s" % error )



# Get/extract the messages from the mail, seprate and store in list(email_data).
def get_messages(service, user_id, message_id):

    try:


        message_list = service.users().messages().get(userId = user_id,  id = message_id, format = 'raw').execute()

        message = message_list

        # converting raw fromat into message string
        raw_to_message_string = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            
        message_string = email.message_from_bytes(raw_to_message_string)

        # Finding email content main type
        string_content_type = message_string.get_content_maintype()

        date_parser = (parser.parse(message_string['Date']))
        date_for = date_parser.date()

        email_data['from'] = message_string['From']
        email_data['to'] = message_string['To']
        email_data['date'] = str(date_for)
        # email_data['date'] = message_string['Date']
        email_data['subject'] = message_string['Subject']
        
        if string_content_type == "multipart":

            # content 1 is a plain text and content 2 is a HTML text
            content1, content2 = message_string.get_payload()
            
            email_data['body'] = content1.get_payload()
            
        else:

            # return message_string.get_payload()
            email_data['body'] = message_string.get_payload()

        # print(email_data)
        return email_data

    except errors.HttpError as error:

        print("An error occured: %s" % error )



# TO check all the labels available
def all_labels(service, user_id):

    check_labels = service.users().labels().list(userId = user_id).execute()

    find_all_labels = check_labels.get('labels',[])

    len_of_labels = len(find_all_labels)

    print(len_of_labels)

    if len_of_labels > 0:

        for label in find_all_labels:
            label_names.append(label['name'])
        # print(label_names)
    else:
        print("No Labels")



# Storing emails and it's content to the database
def email_to_db():

    # get the Gmail API service
    conn = db_connection()
    cur = conn.cursor()

    conn.execute("DELETE FROM email_data")
    print("data deleted")

    for i in range(0,len(final_list)):
        message_id = final_list[i]
        get_messages(service, user_id, message_id)

        result = email_data
        # print(result['from']) 
        cur.execute(
            f""" 
            INSERT INTO email_data 
            (
                Mail_id , Email_From, Email_To  , Email_date, Email_Subject, Email_Message
            ) VALUES 

            (
               ? ,? , ?, ?, ?, ?
            )  """,  
            (str(message_id), result['from'], result['to'], result['date'],result['subject'],result['body'])
        )
        conn.commit()
        print(f"{str(message_id)} Inserted Successfully")

    # data = conn.execute('SELECT * FROM email_data;')
    # email_from_db =[]
    # for i in data:
    #     email_from_db.append(i)
    #     print(i)



# Apply rules to perform action
def apply_rules(user_id):

    conn = db_connection()
    from_db = []
  
    # data = conn.execute('SELECT * FROM email_data;')
    # email_from_db =[]
    # for i in data:
    #     email_from_db.append(i)
    #     print(i)

    predicate = json.load(open('rules.json'))

    pred1 = predicate["3"]['criteria']
    value = predicate["3"]['value']
    find_pred = predicate["3"]['predicate']

    for pred in pred1:
   
        values = pred['value'][1]
        from_db.append(values)
   
    email_from = from_db[0]
    email_to = from_db[1]
    email_sub= from_db[2]
    email_date = from_db[3]

    global final_mail_id
    #### Fetching the mails which matches the condition
    

    # if predicate is ALL this condition applies.
    if find_pred[0] == "ALL" and (value == "contains" or value == "Equals"):
       
        data = conn.execute("select Mail_id from email_data WHERE Email_From = ? AND Email_To = ? AND Email_Subject = ? AND Email_date = ?;", (email_from, email_to, email_sub, email_date,  ) )
   
        final_mail_id = data.fetchall()
        # print (final_mail_id)

    elif find_pred[0] == "ANY" and (value == "contains" or value == "Equals"):
        # print(find_pred[0])
        data = conn.execute("SELECT Mail_id from email_data WHERE Email_From = ? OR Email_to = ? OR Email_Subject = ? OR Email_date = ?;", (email_from, email_to, email_sub, email_date,  ))
        final_mail_id = data.fetchall()


    elif find_pred[0] == "ALL" and (value == "Does not contains" or value == "Does not equal"):

        data = conn.execute("select Mail_id from email_data WHERE Email_From != ? AND Email_To != ? AND Email_Subject != ? AND Email_date != ?;", (email_from, email_to, email_sub, email_date,  ) )
        final_mail_id = data.fetchall()

    elif find_pred[0] == "ANY" and (value == "Does not contains" or value == "Does not equal"):
        
        data = conn.execute("SELECT Mail_id from email_data WHERE Email_From != ? OR Email_to != ? OR Email_Subject != ? OR Email_date != ?;", (email_from, email_to, email_sub, email_date,  ))
        final_mail_id = data.fetchall()

    else:
        print("No data")

    ## Perform the action for the mail_ids
    for item in final_mail_id:
      
        ## To get the message id from the list
        final_id = ''
        for i in item:

            final_id = final_id + i

        action1 = predicate['1']['action']['removeLabelIds']
        action2 = predicate['1']['action']['addLabelIds']
        all_labels(service,user_id)

        if "UNREAD" in label_names:
            result = service.users().messages().modify(userId=user_id, id=final_id,body={ 'removeLabelIds': action1}).execute() 
            print("Marked as READ")
        else:
            result = service.users().messages().modify(userId=user_id, id=final_id,body={ 'addLabelIds': action2}).execute() 
            print("Marked as UNREAD")

        print(result)


    conn.close()



if __name__ == "__main__":

    user_id = 'me'
    service = gmail_authenticate()  
    # all_labels(service,user_id)
    search_messages(service, user_id, ['STARRED'])
    email_to_db()
    apply_rules(user_id)