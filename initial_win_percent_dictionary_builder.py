from collections import Counter
import pymongo
import pickle

client = pymongo.MongoClient("mongodb://worker:password@ec2-52-40-148-30.us-west-2.compute.amazonaws.com")
db=client["lol"]
coll=db["match_data"]

def pull_champions_from_game_data(mongo_object):
    """Takes a dictionary stored in my mongodb.
    Returns ordered lists of allied champions,
    enemy champions, and the winning team id as an int.
    """
    champs=[]
    winning_team=0
    for player in mongo_object["data"]["participants"]:
        champs.append(player["championId"])
    allied_champions=champs[:5]
    enemy_champions=champs[5:]
    if mongo_object["data"]["teams"][0]["win"]=="Fail":
        winning_team=100
    else:
        winning_team=200

    return allied_champions,enemy_champions,winning_team

def build_initial_winrate_dict(iterable_mongo):
    champ_plays=Counter()
    champ_wins=Counter()
    win_percent={}
    for game in iterable_mongo:
        allies,enemies,win=pull_champions_from_game_data(game)
        for champ in allies:
            champ_plays[champ]+=1
            if win==100:
                champ_wins[champ]+=1
        for champ in enemies:
            champ_plays[champ]+=1
            if win==200:
                champ_wins[champ]+=1
    for x in champ_wins.keys():
        win_percent[x]=champ_wins[x]/float(champ_plays[x])
    return win_percent,champ_plays,champ_wins

flat_win_percent, champ_plays, champ_wins = build_initial_winrate_dict(coll.find())
pickle.dump( flat_win_percent , open( "flat_win_percent.p", "wb" ) )
pickle.dump( champ_plays , open( "champ_plays.p", "wb" ) )
pickle.dump( champ_wins , open( "champ_wins.p", "wb" ) )
