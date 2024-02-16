import pymongo
import sys
from print_inventory import print_inventory
from lib_identifier import parse_qrcode_input
from lib_mungo import get_record_by_identifier
from get_key_press import get_key_press
from pprint import pprint
def search_records():
    print("Search Records:")
    existing_record = get_record_by_identifier(parse_qrcode_input())

    if existing_record:
        print_inventory(existing_record)
        print("Press J to view JSON, or any other key to return.")
        # After your print statements
        key_input = get_key_press()  # Convert to lowercase to ensure both 'J' and 'j' are captured.
        if key_input == 'j':
            print()
            pprint(existing_record)
            print()