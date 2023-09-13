#!/usr/bin/env python3
import os
import requests
from pprint import pprint
# get inventory item details from notion
def get_notion_record(notion_id):
    # Get the NOTION_API_KEY from the environment
    NOTION_API_KEY = os.getenv('NOTION_API_KEY')

    # Define the headers for the API request
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    # Define the filter for the query
    filter_data = {
        "property": "c_id",
        "formula": { 
            "string": {
            "equals": notion_id
            }
        }
    }

    # Create the request to search for the record by Notion ID
    query_data = {
        "filter": filter_data
    }

    # Hard-coded DATABASE_ID
    DATABASE_ID = '177ab2fbd98b487386071f2463e6ade1'

    response = requests.post(
        f'https://api.notion.com/v1/databases/{DATABASE_ID}/query',
        headers=headers,
        json=query_data
    )
    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            # Assuming there's only one result, update its "Mungo ID" field
            page_id = data['results'][0]['id']
            pprint(data['results'][0])