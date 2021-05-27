import os
from typing import NamedTuple, Optional
import pymongo
if os.path.exists("env.py"):
    import env
    

MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("could not connect to MongoDB: %s") % e


def show_menu():
    print("")
    print("1. Add a Record")
    print("2. Find a Record by Name")
    print("3. Edit a Record")
    print("4. Delete a Record")
    print("5. Exit")
    
    option = input("Enter option: ")
    return option


def get_record():    
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")
    
    try:
        doc = coll.find({"first" : first.lower(), "last" : last.lower()})
    except:
        print("Error accessing database")
    
    if not doc:
        print("")
        print("Error! No results found.")
        
    return doc

def add_record():
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")
    dob = input("Enter date of birth > ")
    gender = input("Enter gender > ")
    hair_color = input("Enter hair color > ")
    occupation = input("Enter occupation > ")
    nationality = input("Enter nationality > ")
    
    new_doc = {
        "first" : first.lower(),
        "last" : last.lower(),
        "dob" : dob,
        "gender" : gender,
        "hair_color" : hair_color,
        "occupation" : occupation,
        "nationality" : nationality
    }
    
    try:
        coll.insert(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error accessing the database")


def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            print("You have selected option 2. Find a Record by Name")
        elif option == "3":
            print("You have selected option 3. Edit a Record")
        elif option == "4":
            print("You have selected option 4. Delete a Record")
        elif option == "5":
            print("Exiting...")
            conn.close()
            break
        else:
            print("Invalid option")
        print("")
        
        
conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()