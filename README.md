# Happy-Fox

## Problem Statement:

```
Write a standalone Python script that integrates with GMail API and performs some rule based
operations on emails.
```

## Task Details & Breakdown:

- This project is meant to be a standalone Python script, not a web server project. Use any
3rd party libraries you need for the assignment
- Authenticate to Google’s GMail API using OAuth (use Google’s official Python client) and
fetch a list of emails from your Inbox. Do NOT use IMAP.
- Come up a database table representation and store these emails there. Use any
relational database for this (Postgres / MySQL / SQLite3).
- Now that you can fetch emails, write another script that can process emails (in Python
code, not using Gmail’s Search) based on some rules and take some actions on them
using the REST API.
- These rules can be stored in a JSON file. The file should have a list of rules. Each rule
has a set of conditions with an overall predicate and a set of actions.


### Step 1:
Create an Virtual Environment and activate it.
```
virtualenv env_name 
env_name\Scripts\activate
```

### Step 2:
Install the required pacakges
```
pip install -r requirements.txt
```

### Step 3:
Get the credentials from API and Services page 
```
https://console.cloud.google.com/
```

### Step 4:
Run the create-table.py to create a table.
```
python create-table.py
```

### Step 5:
Run the main.py 
```
python main.py
```