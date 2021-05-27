import os
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


conn = mongo_connect(MONGO_URI)

coll = conn[DATABASE][COLLECTION]

new_doc = {
    "first": "douglas",
    "last": "adams",
    "dob": "11/03/1952",
    "hair_color": "grey",
    "occupation": "writter",
    "nationality": "british",
}

# To insert multiple entries at once you must create an array of dictionaries
# new_docs = [{     --notice how it starts with a square bracket []
#    "first":"terry",
#    "last":"pratchett",
#    "dob":"28/04/1948",
#    "anything":"else"
# }, {              --after we end our 1st new entry, close it with a }, and open the next one with {
#                   --you can keep adding stuff as usual
# }]                --remember to close everything with }]


# coll.insert(new_doc) -- insert a sigle entry
# coll.insert_many(new_docs) --to insert multiple entries
documents = coll.find()

for doc in documents:
    print(doc)
