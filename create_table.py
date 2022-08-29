import sqlite3

def new_table():

    conn = sqlite3.connect('Email.db')

    conn.execute(
        """
        CREATE TABLE email_data 
        (
            Mail_id TEXT, 
            Email_From TEXT, 
            Email_To TEXT, 
            Email_date TEXT, 
            Email_Subject TEXT, 
            Email_Message TEXT
        );
        """
    )

