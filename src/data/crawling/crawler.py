import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time

ranks_name = ranker_name("https://pubg.dakgg.io/api/v1/ranks/steam/squad")
df_dakkg_info = ranker_play_info(5,220615)
df_final = set_dataframe(220614)

def ranker_name(url_name):
    ## ranker name crawling
    url = url_name
    result = requests.get(url)
    json_obj = result.text
    dict_obh = json.loads(json_obj)
    ranks = dict_obh["ranks"]
    ranks_name = []
    for i in range(99+1):
        print(i,"번째 ranker name crawling")
        ranks_name.append(ranks[i]["name"])
    return ranks_name

def ranker_play_info(get_each_ranker_num,save_csv_name):
    ## dak.gg
    dakgg_info = []
    for i in range(len(ranks_name)):
        print(f"rank {i} player crawling")
        seed = np.random.randint(100)
        np.random.seed(seed)
        a = np.random.randint(4)
        time.sleep(a)
        url1 = f"https://pubg.dakgg.io/api/v1/players/steam/{ranks_name[i]}/matches?page=1"
        result1 = requests.get(url1)
        json_obj1 = result1.text
        dict_obh1 = json.loads(json_obj1)
        matches = dict_obh1["matches"][0]
        participants = matches["participants"]
        count = 0
        try:
            for k in range(dict_obh1["meta"]["perPage"]):
                if dict_obh1["matches"][k]["participants"][0]["teamRank"] == 1:
                    count += 1
                    for j in range(len(participants)):
                        if dict_obh1["matches"][k]["participants"][j]["name"] == ranks_name[i]:
                            dakgg_info.append(dict_obh1["matches"][k]["participants"][j])
                if count==get_each_ranker_num:
                    break;
        except:
            pass
    df_dakgg_info = pd.DataFrame(data=dakgg_info)
    df_dakgg_info.to_csv(f"data/external/crawl_{save_csv_name}_raw.csv",index=False)
    return df_dakgg_info

def set_dataframe(save_csv_name):
    df_final = df_dakkg_info.drop(["id","teamId","teamRank","shard","deathType","playerId","name","killPlace"],axis=1)
    df_final.columns = ['teamTotal', 'DBNOs', 'assists', 'boosts', 'damageDealt',
           'headshotKills', 'heals', 'killPlace', 'killStreaks', 'kills',
           'longestKill', 'revives', 'rideDistance', 'roadKills',
           'swimDistance', 'teamKills', 'timeSurvived', 'vehicleDestroys',
           'walkDistance', 'weaponsAcquired', 'winPlace', 'mainWeapon']
    df_final.to_csv(f"data/external/crawl_{save_csv_name}_edit.csv", index=False)
    return df_final

""" op.gg
play_info = []
for j in ranks_name:
    seed = np.random.randint(100)
    np.random.seed(seed)
    a = np.random.randint(4)
    time.sleep(a)
    url = f"https://dak.gg/pubg/profile/steam/{j}"
    print(url)
    result = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    html = BeautifulSoup(result.text, 'html.parser')
    ul = html.select("ul.matches-detail__list")
    ul_0 = ul[0].text.replace("\n", "").replace("Damage", ",").replace("Kill (Headshot)", ",").replace("Assists",
                                                                                                       ",").replace(
        "DBNO", "").replace(" ", "")
    ul_1 = ul[1].text.replace("\n", "").replace(" ", "").replace("kmDistance", ",").replace("kmWalkDistance",
                                                                                            ",").replace(
        "kmRideDistance", "")
    ul_2 = ul[2].text.replace("\n", "").replace(" ", "").replace("Heals/Boosts", ",").replace("Revives", "")
    final_ul = ul_0 + "," + ul_1 + "," + ul_2
    play_info.append(final_ul.split(","))
"""