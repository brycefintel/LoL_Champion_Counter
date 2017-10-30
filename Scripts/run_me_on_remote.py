import json
import requests
import time
import pickle
import ast

with open("10000playerIds.txt") as f:
    player_ids_set=set(ast.literal_eval(f.read()))

with open("api_key_1.txt") as f:
    api_key=f.read()

def write_list_to_file(list_to_write,file_to_store):
    with open(str(file_to_store), "a") as f:
        f.write(str(list_to_write))
        f.write("\n")
        f.write("\n")

big_bad_list_of_gameIds=[]
big_bad_set_of_gameIds=set()
for iteration, playerId in enumerate(player_ids_set):
    if (iteration+1)%17==0:
        time.sleep(1)
    if (iteration+1)%97==0:
        with open("log.txt","a") as f:
            f.write("sleeping_120")
        time.sleep(120)
    if (iteration+1)%2000==0:
        with open("log.txt","a") as f:
            f.write("writing list")
        write_list_to_file(big_bad_list_of_gameIds, "big_bad_list")
    url="https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(playerId)+"/recent?api_key="+api_key
    match_history=requests.get(url).json()
    try:
        for match in match_history["matches"]:
            big_bad_list_of_gameIds.append(match["gameId"])
            big_bad_set_of_gameIds.add(match["gameId"])
    except:
        with open("log.txt","a") as f:
            f.write("error:")
            f.write(str(match_history.keys()))

pickle.dump( big_bad_list_of_gameIds, open( "2mill_gameIds.p", "wb" ) )
pickle.dump( big_bad_set_of_gameIds, open( "2mill_gameIds_set.p", "wb" ) )
