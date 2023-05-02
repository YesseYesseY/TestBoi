import requests
import json

version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
champs = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json").json()

champ_rates = requests.get("http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/championrates.json").json()["data"]

top = []
jgl = []
mid = []
adc = []
sup = []
non = []

for champ_key in champs["data"]:
    champ = champs["data"][champ_key]
    non.append(champ["name"])

    if champ_rates[champ["key"]]["TOP"]["playRate"] > 0.0:
        top.append(champ["name"])
    if champ_rates[champ["key"]]["JUNGLE"]["playRate"] > 0.0:
        jgl.append(champ["name"])
    if champ_rates[champ["key"]]["MIDDLE"]["playRate"] > 0.0:
        mid.append(champ["name"])
    if champ_rates[champ["key"]]["BOTTOM"]["playRate"] > 0.0:
        adc.append(champ["name"])
    if champ_rates[champ["key"]]["UTILITY"]["playRate"] > 0.0:
        sup.append(champ["name"])


with open("final.json", "w") as f:
    json.dump({
        "Top": top,
        "Jungle": jgl,
        "Mid": mid,
        "ADC": adc,
        "Support": sup,
        "None": non
    }, f, indent=4)