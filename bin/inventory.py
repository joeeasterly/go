#!/usr/bin/env python3
import pymongo

# Set up the MongoDB connection
client = pymongo.MongoClient("mungo.local:27017")
db = client["go"]
collection = db["link"]

def create_record():
    # Code to create a new record in the collection
    pass

def search_records():
    # Code to search for records in the collection
    pass

def update_record():
    # Code to update a record in the collection
    pass

def delete_record():
    # Code to delete a record from the collection
    pass

def main():
    while True:
        print('''     __  _____  ___   ____________
    /  |/  / / / / | / / ____/ __ \\
   / /|_/ / / / /  |/ / / __/ / / /
  / /  / / /_/ / /|  / /_/ / /_/ /
 /_/  /_/\\____/_/ |_/\\____/\\____/
Menu:
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
