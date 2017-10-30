import pymongo
import requests
import pickle
from collections import Counter

client = pymongo.MongoClient("mongodb://worker:password@ec2-52-40-148-30.us-west-2.compute.amazonaws.com")
db=client["lol"]
coll=db["match_data"]

def lane_dicts(mongo_object):
    """

    """
    allied={}
    enemy={}
    winning_team=0
    bot_flag=[0,0]
    for i,player in enumerate(mongo_object["data"]["participants"]):

        if i<5:
            if bot_flag[0]==0 and player["timeline"]["lane"] == "BOTTOM":
                allied[player["timeline"]["lane"]+"2"]= player["championId"]
                bot_flag[0]=1
            else:
                allied[player["timeline"]["lane"]]= player["championId"]
        else:
            if bot_flag[1]==0 and player["timeline"]["lane"] == "BOTTOM":
                enemy[player["timeline"]["lane"]+"2"]= player["championId"]
                bot_flag[1]=1
            else:
                enemy[player["timeline"]["lane"]]= player["championId"]


    if mongo_object["data"]["teams"][0]["win"]=="Fail":
        winning_team=100
    else:
        winning_team=200
    return allied, enemy, winning_team

def check_for_normal_lanes(gamedata):
    lanes=Counter()
    for champion in gamedata["data"]["participants"]:
        lanes[champion["timeline"]["lane"]]+=1
    return lanes["BOTTOM"]==4 and lanes["JUNGLE"] ==2 and lanes["TOP"] ==2 and lanes["MIDDLE"] ==2

def lane_matchups2(mongo_object):
    allied,enemy,winning_team=lane_dicts(mongo_object)

    if check_for_normal_lanes(mongo_object):
        lane_matchups=Counter()
        lane_matchups_wins=Counter()

        for lane in allied:
            lane_matchups[(allied[lane],enemy[lane])]+=1
            if winning_team==100:
                lane_matchups_wins[(allied[lane],enemy[lane])]+=1
        lane_matchups[(allied["BOTTOM"],enemy["BOTTOM2"])]+=1
        lane_matchups[(allied["BOTTOM2"],enemy["BOTTOM"])]+=1
        if winning_team==100:
            lane_matchups_wins[(allied["BOTTOM"],enemy["BOTTOM2"])]+=1
            lane_matchups_wins[(allied["BOTTOM2"],enemy["BOTTOM"])]+=1

        for lane in enemy:
            lane_matchups[(enemy[lane],allied[lane])]+=1
            if winning_team==200:
                lane_matchups_wins[(enemy[lane],allied[lane])]+=1
        lane_matchups[(enemy["BOTTOM"],allied["BOTTOM2"])]+=1
        lane_matchups[(enemy["BOTTOM2"],allied["BOTTOM"])]+=1
        if winning_team==200:
            lane_matchups_wins[(enemy["BOTTOM"],allied["BOTTOM2"])]+=1
            lane_matchups_wins[(enemy["BOTTOM2"],allied["BOTTOM"])]+=1

        return lane_matchups, lane_matchups_wins

    else:
        pass

def total_and_wins_for_lane_matchup2(iterable_games_data):
    """
    Calls and aggregates results of lane_matchups() over
    iterable collection of games data.
    Returns two counter dicts
    """
    lane_total_vs=Counter()
    lane_wins_vs=Counter()

    for game in iterable_games_data:
        try:
            lane_matchup, lane_matchup_wins = lane_matchups2(game)
            lane_total_vs+=lane_matchup
            lane_wins_vs+=lane_matchup_wins
        except:
            pass

    return lane_total_vs,lane_wins_vs



total, wins = total_and_wins_for_lane_matchup2(coll.find())
pickle.dump( total, open( "total_lane.p", "wb" ) )
pickle.dump( wins, open( "wins_lane.p", "wb" ) )
