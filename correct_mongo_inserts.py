import sys
import pymongo
import requests
import time


def remove_insertions():
    client = pymongo.MongoClient("mongodb://worker:password@ec2-52-24-146-167.us-west-2.compute.amazonaws.com")
    db=client["lol"]
    coll=db["match_data"]
    for _ in range(30):
        entry_in_question=coll.find_one({"done":"true","data":{"status":{"message":"Forbidden","status_code":403}}})
        coll.update_one({"_id":entry_in_question["_id"]},{"$set":{"done":"false","data":"removed"}})

remove_insertions()
