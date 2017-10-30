What it is:
Website that suggests which champion you should play based on revealed enemy and friendly champions chosen in the pre-game lobby.

I will analyze win rates for each champion based on a series of metrics.  Win rate, win rate vs lane opponent, win rate vs each champion of enemy team, win rate with each champion on friendly team.  These metrics would be taken from the LoL game data api, and would be divided along ranks (bronze, silver, gold, platinum, diamond,) in order to present recommendations most salient to the users personal circumstance.

Why it’s important:
There are 200 champions in league of legends, each with a unique set of skills.  Choosing the right champion to counter your lane opponent is an integral part of the meta-game strategy of each match.

My niche:
There exist sites that rank the counter-pick options that perform well against each champion.  These recommendations are determined by users voting, and are not updated with each patch.  I would like to base my recommendations purely on demonstrated game data.  Sites exist which do something similar, and are great tools for understanding the interplay between various champions.  I would like to take it a step further and create a more “in the moment” tool which tells you what to play given the current situation rather than simply educating the user.

By tailoring the recommender to each match, I am able to draw out the synergistic impact of friendly team compositions on win percentage as well as interact with the whole of the enemy team instead of just the laning opponent.

The system:
My model will be aggregating a series of win percentages.  This would be accomplished with a linear model having ~12 variables with each variable representing a two-champion matchup and each variable constant being drawn from the win rates associated with that matchup/combination.  I will run this model with each of the 200 champions available for play, and return the 5 champions which result in the highest logistic probability.

I will also build a classification model to predict victory probabilities based on the current state of the champion selection process at time of query.  This will be accomplished through vectorization of champion pick states combined with training the model with supervised learning.

Data:
LoL api.  I need to figure out if the api throttling applies to the data I need to collect.  There are various tiers of throttling based on the requested data, but there’s almost certainly ways to work within the system, although I may need to find a way to access the data from a static database rather than reactive api.

My goal would be on the order of 500,000 total data points.

Creating the website:
I have no idea.  Fairly simple input/output is required.

Dangers:
LoL win percentages are not widely variable.  I would be working with win rates from 45-55%.  Hopefully this is combated by a large enough data set.

There is no way to insure a player plays in their assigned lane.  This would interfere with the validity of the fairly important “lane matchup” variable.  This should be offset by the comparison to every enemy champion, as well as by the random nature of such lane swaps.
