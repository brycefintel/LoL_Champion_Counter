from flask import Flask, render_template, request, jsonify
import pickle
from collections import defaultdict
from collections import Counter
from scipy.special import logit, expit

app = Flask(__name__)

class recommender(object):
    def __init__(self,a1=None,a2=None,a3=None,a4=None,a5=None,
                 e1=None,e2=None,e3=None,e4=None,e5=None,
                 enemy_laner1=None,enemy_laner2=None):
        #self.a1=a1, self.a2=a2, self.a3=a3, self.a4=a4, self.a5=a5
        #self.e1=e1, self.e2=e2, self.e3=e3, self.e4=e4, self.e5=e5
        self.enemy_laners=[champid for champid in [enemy_laner1,enemy_laner2] if (champid != None and champid != '')]
        #self.enemy_laners=[int(champid) for champid in self.enemy_laners]
        self.allies=[champid for champid in [a1,a2,a3,a4,a5] if champid != None]
        self.enemies=[champid for champid in [e1,e2,e3,e4,e5] if champid != None]
        pickle_path="/home/bryce/galvanize/class/capstone/"
        self.champion_dict = pickle.load(open(pickle_path+"picklejar/champion_dict.p","rb"))
        self.matchup_win_percent = pickle.load(open(pickle_path+"picklejar/trimmed_matchup.p","rb"))
        self.synergy_win_percent = pickle.load(open(pickle_path+"picklejar/trimmed_synergy.p","rb"))
        self.flat_win_percent = pickle.load( open(  pickle_path+"picklejar/flat_win_percent.p", "rb" ) )
        self.lane_matchup= pickle.load( open( pickle_path+"picklejar/trimmed_lane.p", "rb" ) )
        self.predicted_winrates = {}
        self.update_events=0


    def load_base_winrate(self):
        for key in self.flat_win_percent:
            self.predicted_winrates[key]=logit(.5) #self.flat_win_percent[key]

###START
    def get_winrate_for_enemy(self,possible_pick,enemyid):
        #print self.enemies
        return self.matchup_win_percent[possible_pick,enemyid]
    def get_winrate_for_ally(self,possible_pick,allyid):
        return self.synergy_win_percent[possible_pick,allyid]
    def get_winrate_for_enemy_laner(self, possible_pick,lanerid):
        return self.lane_matchup[possible_pick,lanerid]


    def update_predicted_winrate_for_enemy(self,picked_champion):
        self.update_events+=1
        for champion in self.predicted_winrates.keys():
            if champion == picked_champion:
                pass
            else:
                self.predicted_winrates[champion] = self.predicted_winrates[champion] + logit(self.get_winrate_for_enemy(champion,picked_champion))

    def update_predicted_winrate_for_ally(self,picked_champion):
        self.update_events+=1
        for champion in self.predicted_winrates.keys():
            if champion == picked_champion:
                pass
            else:
                self.predicted_winrates[champion] = self.predicted_winrates[champion] + logit(self.get_winrate_for_ally(champion,picked_champion))

    def update_predicted_winrate_for_lane(self, picked_champion):
        self.update_events+=1
        for champion in self.predicted_winrates.keys():
            self.predicted_winrates[champion] = self.predicted_winrates[champion] + logit(self.get_winrate_for_enemy_laner(champion,picked_champion))
###END

    def top_picks(self):
        return sorted(self.predicted_winrates.items(), key=lambda(item): item[1][0], reverse=True)

    def champion_name_from_id(self,champion_number):
        return self.champion_dict["data"][str(champion_number)]["name"]

    def predict(self,n=5):
        top_n_picks=[]
        for pair in self.top_picks()[:n]:
            top_n_picks.append((self.champion_name_from_id(pair[0]), "%.2f" % expit(pair[1][0]/(self.update_events+1))))
        return top_n_picks

def run_and_predict(a1=None,a2=None,a3=None,a4=None,a5=None,
                 e1=None,e2=None,e3=None,e4=None,e5=None,
                 enemy_laner1=None,enemy_laner2=None):
    model=recommender(**locals())
    model.load_base_winrate()
    for champ in model.enemies:
        model.update_predicted_winrate_for_enemy(champ)
    for champ in model.allies:
        model.update_predicted_winrate_for_ally(champ)
    for champ in model.enemy_laners:
        model.update_predicted_winrate_for_lane(champ)
    return model.predict()



@app.route('/')
def index():
    return render_template('site2.html')

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    print data
    for key in data.keys():
        try:
            data[key]=int(data[key])
        except:
            data[key]=None
    print data

    predictions = run_and_predict(a1=data["a1"],a2=data["a2"],a3=data["a3"],a4=data["a4"],
                    e1=data["e1"],e2=data["e2"],e3=data["e3"],e4=data["e4"],e5=data["e5"],
                    enemy_laner1=data["el1"],enemy_laner2=data["el2"])
    #post_string=""
    #for x in predictions:
    #    post_string.append(str(x))
    # a1,a2,a3,a4,a5 = data["a1"], data["a2"], data["a3"], data["a4"], data["a5"]
    # e1,e2,e3,e4,e5 = data["e1"], data["e2"], data["e3"], data["e4"], data["e5"]
    return jsonify({"predictions":str(predictions)})



@app.route("/calculate2", methods=["POST"])
def calculate2():
    data= request.json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
