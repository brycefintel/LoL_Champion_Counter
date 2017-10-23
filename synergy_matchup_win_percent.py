import pymongo
import pickle
from collections import Counter

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

def count_matchups(allied_champions,enemy_champions,winning_team):
    """
    Returns counter dict of how many times [key] matchup has occured
    (4,7):3 == champion 4 has *matched against* champion 7 three times
    and
    Returns counter dict of how many times [key] matchup has resulted in a win
    (4,7):3 == champion 4 has *won against* champion 7 three times
    """
    matchups=Counter()
    matchups_wins=Counter()
    for champ in allied_champions:
        for enemychamp in enemy_champions:
            matchups[(champ,enemychamp)]+=1
            if winning_team==100:
                matchups_wins[(champ,enemychamp)]+=1
    for champ in enemy_champions:
        for enemychamp in allied_champions:
            matchups[(champ,enemychamp)]+=1
            if winning_team==200:
                matchups_wins[(champ,enemychamp)]+=1
    return matchups, matchups_wins

def total_and_wins_for_matchup(iterable_games_data):
    """
    Calls and aggregates results of count_matchups() over
    iterable collection of games data.
    Returns two counter dicts
    """
    total_vs=Counter()
    wins_vs=Counter()
    for game in iterable_games_data:
        matchups, matchups_wins=count_matchups(*pull_champions_from_game_data(game))
        total_vs+=matchups
        wins_vs+=matchups_wins
    return total_vs,wins_vs

def count_synergies(allied_champions,enemy_champions,winning_team):
    """
    Returns counter dict of how many times [key] synergy has occured
    (4,7):3 == champion 4 has *matched with* champion 7 three times
    and
    Returns counter dict of how many times [key] synergy has resulted in a win
    (4,7):3 == champion 4 has *won with* champion 7 three times
    """
    synergy=Counter()
    synergy_wins=Counter()
    for i,champ in enumerate(allied_champions):
        for i2,champ2 in enumerate(allied_champions):
            if i==i2:
                continue
            synergy[(champ,champ2)]+=1
            if winning_team==100:
                synergy_wins[(champ,champ2)]+=1
    for i,champ in enumerate(enemy_champions):
        for i2,champ2 in enumerate(enemy_champions):
            if i==i2:
                continue
            synergy[(champ,champ2)]+=1
            if winning_team==200:
                synergy_wins[(champ,champ2)]+=1
    return synergy,synergy_wins

def total_and_wins_for_synergy(iterable_games_data):
    """
    Calls and aggregates results of count_synergies() over
    iterable collection of games data.
    Returns two counter dicts
    """
    total_synergy=Counter()
    wins_synergy=Counter()
    for game in iterable_games_data:
        synergy,synergy_wins=count_synergies(*pull_champions_from_game_data(game))
        total_synergy+=synergy
        wins_synergy+=synergy_wins
    return total_synergy,wins_synergy

total_matchup, wins_matchup = total_and_wins_for_matchup(coll.find())
total_synergy, wins_synergy = total_and_wins_for_synergy(coll.find())
matchup_win_percent={}
synergy_win_percent={}

for key in total_matchup.keys():
    matchup_win_percent[key]=wins_matchup[key]/float(total_matchup[key])
for key in total_synergy.keys():
    synergy_win_percent[key]=wins_synergy[key]/float(total_synergy[key])

pickle.dump( matchup_win_percent, open( "matchup_win_percent.p", "wb" ) )
pickle.dump( synergy_win_percent, open( "synergy_win_percent.p", "wb" ) )
