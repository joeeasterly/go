#!/usr/bin/env python3
import os
import time
import requests
import json
from pprint import pprint
def parse_notion_input(mungo_notion=""):
    # Prompt the user for input
    if mungo_notion:
        user_input = input(f"Notion ID: [{mungo_notion}] Enter to keep existing ID: ").lower().strip()
    else:
        user_input = input(f"Notion ID: [{mungo_notion}] Enter to allocate new ID: ").lower().strip()

    # If user inputs "+" or "new", allocate a new Notion ID
    if user_input in ["+", "new"]:
        notion_id = allocate_notion_id()
        print(f"Allocating Notion Inventory ID {notion_id}")

    # If user hits return/enter without any input, use the default behavior
    elif not user_input:
        if mungo_notion:
            notion_id = mungo_notion  # Use the existing mungo_notion if it exists
            print(f"Using existing Notion Inventory ID {notion_id}")
        else:
            notion_id = allocate_notion_id()  # Allocate a new notion_id if mungo_notion doesn't exist
            print(f"Allocating Notion Inventory ID {notion_id}")

    # Validate and use the user's input if provided and not a special keyword
    else:
        user_input = user_input.replace("inv-", "")  # Remove the prefix if present
        if not user_input.isdigit():
            raise ValueError("Notion ID must be a number (apart from prefix).")
        notion_id = user_input
        print(f"Using Notion Inventory ID {notion_id}")

    time.sleep(1)  # Play nice with the Notion API
    return notion_id

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
            return data['results'][0]
    else:
        raise Exception(f"Error getting record from Notion: {response.status_code} {response.text}")

def link_notion_inventory(notion_id, mungo_id, shcn, mungo_label, expires = None, upc = None, percentage = None, quantity = None):
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
                    "Mungo ID": {
                        "type": "rich_text",
                        "rich_text": [{"text": {"content": mungo_id}}]
                    },
                    "SHCN": {
                        "type": "rich_text",
                        "rich_text": [{"text": {"content": shcn}}]
                    },
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
            # Conditionally add fields if they exist
            if upc is not None:
                 update_data["properties"]["UPC"] = {
                    "number": upc
                }
            if percentage is not None:
                update_data["properties"]["Remaining"] = {
                    "number": percentage
                }
            if percentage is not None:
                update_data["properties"]["Type"] = {
                    "multi_select": [
                    { "name": "Consumable" }
                    ]
                }
            if expires is not None:
                update_data["properties"]["Expires"] = {
                "date": {
                    "start": expires
                }
                }
            if quantity is not None:
                update_data["properties"]["Count"] = {
                "number": quantity
                }
            update_response = requests.patch(
                f'https://api.notion.com/v1/pages/{page_id}',
                headers=headers,
                json=update_data
            )
            if update_response.status_code == 200:
                return "Notion record updated successfully: https://notion.so/inv-" + notion_id
            else:
                return "Failed to update Notion record."
        else:
            return "Notion record not found."
    else:
        return "Failed to query the Notion database."

def allocate_notion_id():
    url = "https://api.notion.com/v1/pages"
    NOTION_API_KEY = os.getenv('NOTION_API_KEY')
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }
    
    payload = {
        "parent": {"database_id": "177ab2fbd98b487386071f2463e6ade1"},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": "allocated_by_mungo"
                        }
                    }
                ]
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        page_data = json.loads(response.text)
        c_id_value = page_data['properties']['c_id']['formula']['string']
        return c_id_value
    else:
        print(f"Failed to create page: {response.text}")
        return None

def archive_notion_page(notion_id):
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
            # Assuming there's only one result, archive (i.e., delete) it
            page_id = data['results'][0]['id']
            update_response = requests.patch(
                f'https://api.notion.com/v1/pages/{page_id}',
                headers=headers,
                json={ "archived": True }
            )
            print(f'response: {update_response.status_code}')
            if update_response.status_code == 200:
                return "Notion record archived successfully: https://notion.so/inv-" + notion_id
            else:
                return "Failed to archive Notion record."
        else:
            return "Notion record not found."
    else:
        return "Failed to query the Notion database."