#!/usr/local/gh/go/.venv/bin/python3
#
import os
from create_record import create_record
from create_media import create_media
from search_records import search_records
from update_record import update_record
from update_consumable import update_consumable
from add_consumable_instance import add_consumable_instance
from delete_consumable import delete_consumable
from lib_storage import add_storage, update_storage_record
from delete_record import delete_record
from reshelve import reshelve_record
#
#
# Show the main menu
logo = '''
    __  _____  ___   ____________ 
   /  |/  / / / / | / / ____/ __ \\
  / /|_/ / / / /  |/ / / __/ / / /
 / /  / / /_/ / /|  / /_/ / /_/ /
/_/  /_/\____/_/ |_/\____/\____/

##################################################
#          Inventory Management System           #
##################################################
'''
menu = '''
    1) Create  2) Search 3) Update Item      
    4) Storage 5) Delete 6) Reshelve Items
    7) Update Github 8) Update Consumable 0) Exit'''

def main():
    os.system('clear')  # Clear the screen first.
    on_launch = True
    while True:
        if on_launch:
            print(logo + menu)
            on_launch = False
        else:
            print(menu)
        print()
        choice = input('Select an option: ')

        if choice == '1':
            create_record()
        elif choice == '2':
            search_records()
        elif choice == '3':
            update_record()
        elif choice == '4':
            add_storage()
        elif choice == '41':
            update_storage_record()
        elif choice == '5':
            delete_record()
        elif choice == '51':
            delete_consumable()
        elif choice == '6':
            reshelve_record()
        elif choice == '7':
            os.system("/usr/local/gh/go/.venv/bin/python3 /usr/local/gh/go/bin/update_github.py")  # Execute the update_github.py script
        elif choice == '71':
            os.system("/usr/local/gh/go/.venv/bin/python3 /usr/local/gh/go/bin/export_shelves.py")  # Execute the update_github.py script
        elif choice == '8':
            update_consumable()
        elif choice == '81':
            add_consumable_instance()
        if choice == 'm':
            create_media()
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Please select a valid option.')

if __name__ == "__main__":
    main()