import pymongo
import pickle
client = pymongo.MongoClient("mongodb://worker:password@ec2-52-24-146-167.us-west-2.compute.amazonaws.com")
db=client["lol"]
coll=db["match_data"]
gameids = set(pickle.load( open( "2mill_gameIds.p", "rb" ) ))


for i,single_id in enumerate(gameids):
    coll.insert_one(
    {"_id":i,"gameid":single_id, "batch":i%4,"done":"false"})
