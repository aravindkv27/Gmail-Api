import sqlite3


def createtable():
    
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

    print("table_created")