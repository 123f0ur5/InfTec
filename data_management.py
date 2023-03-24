import json
from scrapper import get_odds

data = {"live_games" : "live_games.json",
         "highlighted_games" : "highlighted_games.json"}

dct_destination = {"home" : "casa",
                   "away" : "fora",
                   "draw" : "empate"}

write_data = {"eventos" : []}

for key, item in data.items():
    with open(item, "r") as f:
        data[key] = json.loads(f.read())

for games in data.values():
    for game in games:
        game_id = game["id"]
        tmp_dct = {}
        for item in game["participants"]:
            alignment, name, *_ = zip(item.values())
            tmp_dct["casa" if alignment[0] == "home" else "fora"] = name[0]
        tmp_dct["odds"] = {}
        odds = json.loads(get_odds(game_id))
        for odd in odds:
            if odd["matchupId"] == game_id:
                if odd["key"] == "s;0;m":
                    for value in odd["prices"]:
                        destination, price = value.values()
                        if price >= 0:
                            price = round(price / 100 + 1, 3)
                        else:
                            price = round(100 / abs(price) + 1, 3)

                        
                        tmp_dct["odds"][dct_destination[destination]] = price


        write_data["eventos"].append(tmp_dct)

        print(f"{tmp_dct['casa']} x {tmp_dct['fora']} registrado")

print(write_data)

with open("resultado.json", "w") as f:
    f.write(json.dumps(write_data, indent = 3))