#!/usr/bin/env python3
import os
import requests
from pprint import pprint

def link_notion_consumable(notion_id, mungo_id, shcn, mungo_label, expires, upc, percentage, quantity = None):
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
            # Assuming there's only one result, update Mungo ID and SHCN fields
            page_id = data['results'][0]['id']
            update_data = {
                "properties": {
                    "Mungo ID": { "rich_text": [ { "type": "text", "text": { "content": mungo_id } } ] },
                    "SHCN": { "rich_text": [ { "type": "text", "text": { "content": shcn } } ] },
                    "Type": { "multi_select": [ { "name": "Consumable" } ] },
                    "UPC": { "rich_text": [ { "type": "text", "text": { "content": upc } } ] },
                    "Count": { "number": float(quantity) },
                    "Remaining": { "number": float(percentage) },
                    "Expires": { "date": { "start": expires } },
                    "Name": {
                        "type": "title",
                        "title": [{
                            "type": "text",
                            "text": {
                                "content": mungo_label
                            }
                        }]
                    }
                }
            }
            update_response = requests.patch(
                f'https://api.notion.com/v1/pages/{page_id}',
                headers=headers,
                json=update_data
            )
            print(f'response: {update_response.status_code}')
            pprint(update_response.json())
            if update_response.status_code == 200:
                return "Notion record updated successfully: https://notion.so/inv-" + notion_id
            else:
                return "Failed to update Notion record."
        else:
            return "Notion record not found."
    else:
        return "Failed to query the Notion database."
# notion_id = "947"
# mungo_id = "5k9m"
# shcn = "10"
# mungo_label = "Mungo's Dog Treats"
# expires = "2021-10-31"
# upc = "123456789012"
# percentage = "100"
# quantity = "1"
# link_notion_consumable(notion_id, mungo_id, shcn, mungo_label, expires, upc, percentage, quantity)