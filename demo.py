from datetime import date, datetime
import json
import sqlite3
from dateutil import parser
from datetime import date
 
# predicate = json.load(open('rules.json'))

# value = predicate["4"]['value']
# print(value)
def db_connection():

    conn = sqlite3.connect("Email.db")
    return conn


def apply_rules(user_id):

    conn = db_connection()
    from_db = []
  
    # data = conn.execute('SELECT * FROM email_data;')
    # email_from_db =[]
    # for i in data:
    #     email_from_db.append(i)
    #     print(i)

    predicate = json.load(open('rules.json'))

    pred1 = predicate["1"]['criteria']
    value = predicate["1"]['value']
    find_pred = predicate["1"]['predicate']

    for pred in pred1:
   
        values = pred['value'][1]
        from_db.append(values)
   
    email_from = from_db[0]
    email_to = from_db[1]
    email_sub= from_db[2]
    email_date = from_db[3]
    # print(from_db)

    # print(type(email_date))
    # # print(int(email_date))
    # d1 = date(2008, 9, 26)
    # DT = parser.parse(email_date)
    # print(DT)

    date_string = '2021-12-31'
    # datetime = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
    # print(datetime)

    # final_days = DT - d1
    # print(final_days.days)

    # data = conn.execute("SELECT Mail_id from email_data WHERE Email_From != ?;", (email_from, ) )
    # final_mail_id = data.fetchall()
    # print(final_mail_id)
    datetime = datetime.datetime.strptime(date_string, '%Y/%m/%d')
    print(datetime.data)
    now = datetime.today().strftime('%Y-%m-%d')
    print(now)


apply_rules('me')

# from datetime import date

# d0 = date(2008, 8, 18)
# d1 = date(2008, 9, 26)
# delta = d1 - d0
# print(delta.days)