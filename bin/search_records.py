import pymongo
import sys
from library.print_inventory import print_inventory
from library.parse_qrcode_input import parse_qrcode_input
from library.get_record_by_identifier import get_record_by_identifier
from library.get_key_press import get_key_press
from library.connect_mungo import connect_mungo
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