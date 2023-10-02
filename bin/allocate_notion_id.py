import requests
import json
import os

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