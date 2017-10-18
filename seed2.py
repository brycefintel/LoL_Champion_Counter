from collections import defaultdict
import json
from pprint import pprint
import numpy as np
import requests
import time
import pickle
import ast

with open("seed2_10kgameids.txt") as f:
    gameIds=ast.literal_eval(f.read())
player_ids=[]
player_ids_set=set()
for iteration, match_id in enumerate(gameIds):
    if iteration%17==0:
        time.sleep(1)
    if iteration%90==0:
        print "sleeping_120"
        time.sleep(120)

    url="https://na1.api.riotgames.com/lol/match/v3/matches/"+str(match_id)+"?api_key=RGAPI-fe1a3194-1cf3-4534-825c-c3acb1f7d9ef"
    match=requests.get(url).json()
    try:
        for player in match["participantIdentities"]:
            try:
                player_ids.append(player["player"]["currentAccountId"])
            except:
                print "missed one"
    except:
        print "missed one match['participantIdentities']"
pickle.dump( player_ids, open( "100kplayerids_list.p", "wb" ) )
