import os
from typing import NamedTuple, Optional
import pymongo

if os.path.exists("env.py"):
    import env  # imports the login info to access DB


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
    print("")  # empty line for clarity
    print("1. Add a Record")
    print("2. Find a Record by Name")
    print("3. Edit a Record")
    print("4. Delete a Record")
    print("5. Exit")

    option = input("Enter option: ")
    return option


def get_record():  # gets first+last names, searches collection for it and returns result
    print("")  # empty line for clarity
    # asks user for fname they're looking for
    # also asks for last name for a more precise search
    first = input("Enter first name > ")
    last = input("Enter last name > ")

    try:
        # uses the input names in a .find() and assigns result to 'doc'
        doc = coll.find_one({"first": first.lower(), "last": last.lower()})
    except:
        # generic message if any error
        print("Error accessing database")

    if not doc:
        # if 'doc' is empty, null, false or blank
        print("")
        print("Error! No results found.")

    return doc  # returns our search result to the get_record()


def add_record():
    print("")
    # series of inputs to help user add a new celeb to collection
    first = input("Enter first name > ")
    last = input("Enter last name > ")
    dob = input("Enter date of birth > ")
    gender = input("Enter gender > ")
    hair_color = input("Enter hair color > ")
    occupation = input("Enter occupation > ")
    nationality = input("Enter nationality > ")

    new_doc = {
        # Once inputs are answered we create a doc that will be
        # used to insert data into the collection.
        # new_doc is a dictionary
        # Here, .lower() used to make it easier to find data
        "first": first.lower(),
        "last": last.lower(),
        "dob": dob,
        "gender": gender,
        "hair_color": hair_color,
        "occupation": occupation,
        "nationality": nationality,
    }

    try:
        # attempts to .insert() the new_doc dictionary into our collection
        # coll is the variable that grants us access to the collection
        coll.insert_one(new_doc)
        print("")
        print("Document inserted")
    except:
        # if theres an error will print msg
        print("Error accessing the database")


def find_record():
    # assigns returned value from get_record() to var 'doc'
    # if doc is true (not null, not false, not empty string)
    # will loop through k(keys) and v(values) of the celeb
    # checks if key is NOT the unique id of the celeb
    # prints all the keys and values capitalized
    doc = get_record()
    if doc:
        print("")
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())


def edit_record():
    # assigns the returned value of get_record() to 'doc'
    # creates an empty dic called update_doc
    # loops through k(eys) and v(alues) of the celeb
    # checks if key is NOT unique id
    # if key is not unique id, prints current Key [value] and asks for input
    # -- example: Key [value] > newValueHere
    # if the input is empty string will use previous value as new value(no update)
    # after that attepts update using the new dict update_doc (filled with the input data)
    # -- example: coll.update_one(result of get_record, {"$set": new dict update_doc})
    doc = get_record()
    if doc:
        update_doc = {}  # defines empty dict
        print("")
        for k, v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")

                if update_doc[k] == "":
                    update_doc[k] = v
        try:
            coll.update_one(doc, {"$set": update_doc})
            print("")
            print("Document updated")
        except:
            print("Error accessing database.")


def delete_record():
    doc = get_record()
    if doc:
        print("")
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + " : " + v.capitalize())

        print("")
        confirmation = input("Is this the record you want to delete?\nY/N > ")
        print("")
        if confirmation.lower() == "y":
            try:
                coll.remove(doc)
                print("Document deleted!")
            except:
                print("Error accessing database.")
        else:
            print("Record not deleted.")


def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            print("You have selected option 4. Delete a Record")
            delete_record()
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
