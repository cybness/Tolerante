import requests
import json
from collections import namedtuple
from contextlib import closing
import sqlite3

from prefect import task, flow

## extract
@task
def get_complaint_data():
    r = requests.get("https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/", params={'size':10})
    response_json = r.json()  
    return response_json['hits']['hits']

## transform
@task
def parse_complaint_data(raw):
    complaints = []
    Complaint = namedtuple('Complaint', ['date_received', 'state', 'product', 'company', 'complaint_what_happened'])
    for row in raw:
        source = row.get('_source', {})
        this_complaint = Complaint(
            date_received=source.get('date_received'), 
            state=source.get('state'),
            product=source.get('product'),
            company=source.get('company'),
            complaint_what_happened=source.get('complaint_what_happened')
        )
        complaints.append(this_complaint)
    return complaints

## load
@task
def store_complaints(parsed):
    create_script = '''CREATE TABLE IF NOT EXISTS complaint (
        date_received TEXT, 
        state TEXT, 
        product TEXT, 
        company TEXT, 
        complaint_what_happened TEXT
    )'''
    insert_cmd = "INSERT INTO complaint VALUES (?, ?, ?, ?, ?)"

    with closing(sqlite3.connect("cfpbcomplaints.db")) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executescript(create_script)
            cursor.executemany(insert_cmd, parsed)
            conn.commit()

@flow
def my_etl_flow():
    raw = get_complaint_data()
    parsed = parse_complaint_data(raw)
    store_complaints(parsed)

# Ejecutar el flujo
if __name__ == "__main__":
    my_etl_flow()



