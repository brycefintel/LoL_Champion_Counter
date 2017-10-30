import pymongo
import requests
import time
import pickle
import ast
def gameIds_to_mongo(list_of_gameIds,mongo_db,mongo_collection,api_key):
    """
    Inputs: (list of numbers, str, str, str)
    Output: None
    Makes api calls to retrieve full match data for each gameId in input list
    and stores match data as json/dict in specified mongo database
    """
    working_list=list(list_of_gameIds)
    mc = pymongo.MongoClient()
    db = mc[mongo_db]
    game_events = db[mongo_collection]
    i=0
    while len(working_list)>0:
        if (i+1)%17==0:
            time.sleep(1)
        if (i+1)%97==0:
            time.sleep(120)
        i+=1
        response=requests.get("https://na1.api.riotgames.com/lol/match/v3/matches/"+str(working_list.pop(0))+"?api_key="+api_key)
        if str(response)=="<Response [200]>":
            game_events.insert_one(response.json())
        else:
            with open("leftovers.txt","a") as f:
                f.write("I made it through "+str(i)+" loops.")
                f.write(str(working_list))

with open("api_key.txt") as f:
    key=f.read()

with open("gameids_chunk.txt") as f:
    gameids=set(ast.literal_eval(f.read()))

gameIds_to_mongo(gameIds,"lol_1","games_data",key)
