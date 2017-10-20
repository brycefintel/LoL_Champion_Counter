import sys
import pymongo
import requests
import time


def get_data_for_gameid_in_mongo(worker,apikey):
    client = pymongo.MongoClient("mongodb://worker:password@ec2-52-24-146-167.us-west-2.compute.amazonaws.com")
    db=client["lol"]
    coll=db["match_data"]
    _ids=[x["_id"] for x in coll.find({"done":"false","batch":2})]
    for i,_id in enumerate(_ids):
        if i%18==0:
            time.sleep(1)
        if (i+1)%98==0:
            time.sleep(120)
        if (i+1)%1000==0:
            print "1000 hits"
        entry_in_question=coll.find_one({"_id":_id})
        url="https://na1.api.riotgames.com/lol/match/v3/matches/"+str(entry_in_question["gameid"])+"?api_key="+str(apikey)
        data=requests.get(url).json()
        coll.update_one({"_id":entry_in_question["_id"]},{"$set":{"done":"true","data":data}})


args_list=sys.argv
get_data_for_gameid_in_mongo(args_list[1],args_list[2])
#(script name,worker_number,api_key)
