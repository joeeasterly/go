#!/usr/bin/env python3
#
from create_record import create_record
from search_records import search_records
from update_record import update_record
from delete_record import delete_record
#
#
# Show the main menu
def main():
    while True:
        print('''     __  _____  ___   ____________
    /  |/  / / / / | / / ____/ __ \\
   / /|_/ / / / /  |/ / / __/ / / /
  / /  / / /_/ / /|  / /_/ / /_/ /
 /_/  /_/\\____/_/ |_/\\____/\\____/

Inventory Management System
1) Create
2) Search
3) Update
4) Delete
5) Exit''')

        choice = input('Select an option: ')

        if choice == '1':
            create_record()
        elif choice == '2':
            search_records()
        elif choice == '3':
            update_record()
        elif choice == '4':
            delete_record()
        elif choice == '5':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please select a valid option.')

if __name__ == "__main__":
    main()