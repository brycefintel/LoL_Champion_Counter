# LoLCounter.us

### What it is:
Website that suggests which League of Legends champion you should play based on revealed enemy and friendly champions chosen in the pre-game lobby.
League of Legends has 138 unique champions, each with unique strengths and weaknesses.
Picking a champion that works well with allies strengths and exploits enemy weaknesses is a vital part of a successful strategy.
LoLCounter.us helps you make this choice based on data drawn from past matches.

### Methodology:
Starting with 1,000 seed gameIDs, I used the Riot Games v3 API to get playerlists for each of these games.  Using these 10,000 playerIDs, I collected the gameIDs for the most recent 20 games played by each player.  I then used this list of gameIDs to download ~200,000 game data objects onto a MongoDB server I set up.

Parsing the game data for team champion composition, lane information, and victory flags, I was able to create a series of victory probabilities for every champion matchup.
I calculated the directional win rates for each champion in conjunction with each other champion in three different situations:

Allied:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;% X wins with Y on team
    
Adversarial:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;% X wins with Y on enemy team
    
Lane Matchup:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;% X wins when Y is enemy laner 

My model runs as a class object which takes the state of a League of Legends draft as input.  On instantiation a list of  victory probabillites for each champion is created.  For every champion decision passed to the model, the model queries the appropriate victory probabillity resource and updates the projected win rate of each champion available to be picked.


A quantitative approach:
There exist sites that rank the counter-pick options that perform well against each champion.  These recommendations are determined by users voting, and are not updated with each patch.  I would like to base my recommendations purely on demonstrated game data.  Sites exist which do something similar, and are great tools for understanding the interplay between various champions.  I would like to take it a step further and create a more “in the moment” tool which tells you what to play given the current situation rather than simply educating the user.

By tailoring the recommender to each match, I am able to draw out the synergistic impact of friendly team compositions on win percentage as well as interact with the whole of the enemy team instead of just the laning opponent.


Data:
Riot Games API.  Riot makes match data for all relevant games played freely available through their API.


Next steps:
I need to obtain a Riot API production key in order to acquire larger numbers of games in a timely fashion.  My production pipeline is set up to run on any number of entries in my MongoDB server.  With faster API access I would like to re-collect my dataset from the new patch with the release of each patch.  This would allow LoLCounter.us to provide more accurate timely results, as well as give insight into the ever evolving champion meta.
