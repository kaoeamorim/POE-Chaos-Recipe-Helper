import requests
import json

poesessid = {"POESESSID":'754a6b913eb8f1cfd26e45375ab28119'}

itemList = {'1h, 2h or Shield':0, 'Helmet':0, 'Chest':0, 'Gloves':0, 'Boots':0, 'Belt':0,'Amulet':0,'Ring':0}

for tab in range(0,12):
    print(f"getting tab {tab}")
    req = requests.get("https://www.pathofexile.com/character-window/get-stash-items?accountName=Garulf161&tabIndex= " + str(tab) + "&league=Legion", cookies=poesessid)

    resp = json.loads(req.text)


    for x in range(0,len(resp["items"])):

        for key in resp['items'][x]['category']:
            category = key

        if category in ('armour','weapons','accessories') and resp["items"][x]["identified"] == False:
            
            print("Unidentified ",end="")
            print(f"{resp['items'][x]['category'][category][0]} in tab {tab}")

            if resp['items'][x]['category'][category][0] in ('dagger','claw','onesword','wand','shield','oneaxe','staff','twomace','twoaxe','twosword','bow'):
                itemList['1h, 2h or Shield'] += 1
            elif resp['items'][x]['category'][category][0] != 'quiver':
                try:
                    itemList[resp['items'][x]['category'][category][0].capitalize()] += 1
                except:
                    itemList[resp['items'][x]['category'][category][0].capitalize()] = 1

print(itemList)