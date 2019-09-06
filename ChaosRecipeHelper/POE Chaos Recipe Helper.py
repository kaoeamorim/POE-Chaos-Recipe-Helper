import tkinter
import requests
import json
from time import sleep, time

sleep
window = tkinter.Tk()
window.title("PoE Chaos Recipe Helper")

timeCount = 0
isCancel = False
callsCount = 0
tabsToCheck = {}


itemClasses = ('1h or Shield', '2h or Bow', 'Helmet', 'Chest','Gloves','Boots', 'Belt', 'Amulet', 'Ring')
weapons1h = ('dagger','claw','onesword','wand','shield','oneaxe', 'onemace')
weapons2h = ('twomace', 'twoaxe', 'twosword', 'bow', 'staff')

  
def populate(itemList, weapons1h, weapons2h):

    global timeCount

    global isCancel

    global callsCount

    global tabsToCheck

    isCancel = False
    stuffs.cancelButton.configure(state='normal')

    infos = {"POESESSID":{'POESESSID':stuffs.sessID.get()},'ACCOUNT':stuffs.accountName.get(),'CHARACTER':stuffs.characterName.get(),'LEAGUE':stuffs.plg.get(), 'REALM':stuffs.realm.get()}

    itemList = {k:0 for k in itemList}

    try:

        if 'tabNames' not in globals():

            callsCount += 1

            global tabNames

            tabNames = requests.get("https://www.pathofexile.com/character-window/get-stash-items?accountName=" + infos['ACCOUNT'] + "&tabIndex=" + str(0) + "&league=" + infos['LEAGUE'] + '&tabs=1', cookies = infos['POESESSID'])

            tabNames = json.loads(tabNames.text)

            tabsToCheck = {tabnum for tabnum in range(0,tabNames['numTabs'])}


            if "error" in tabNames or len(tabNames) <= 1:

                stuffs.statusText.configure(state='normal')
                stuffs.statusText.delete(0,'end')
                stuffs.statusText.insert(0,f"Error received the from API. Check if all the information is correct")
                stuffs.statusText.configure(state='disabled')

                if tabNames['error']['code'] == 3:

                    stuffs.statusText.configure(state='normal')
                    stuffs.statusText.delete(0,'end')
                    stuffs.statusText.insert(0,f"Time out. Too many requests. Hopefully for only 60 seconds.")
                    stuffs.statusText.configure(state='disabled')

                del tabNames
                return itemList

        tab = 0

        while tab <= max(tabsToCheck):

            if tab not in tabsToCheck:

                tab = tab + 1

                continue

            if isCancel == True:

                stuffs.statusText.configure(state='normal')
                stuffs.statusText.delete(0,'end')
                stuffs.statusText.insert(0,f"Operation aborted.")
                stuffs.statusText.configure(state='disabled')
                stuffs.updateButton.configure(state='normal')


                return itemList

            if callsCount >= 45:

                stuffs.statusText.configure(state='normal')
                stuffs.statusText.delete(0,'end')
                stuffs.statusText.insert(0,f"Waiting to avoid timeout. Resuming in {70 - abs(int(time() - timeCount))} seconds.")
                stuffs.statusText.configure(state='disabled')

                window.update()

                sleep(1)

                window.update()


                if abs(int(time() - timeCount)) >= 70:

                    timeCount = time()

                    callsCount = 0

                continue


            callsCount += 1

            resp = requests.get("https://www.pathofexile.com/character-window/get-stash-items?accountName=" + infos['ACCOUNT'] + "&tabIndex=" + str(tab) + "&league=" + infos['LEAGUE'], cookies = infos['POESESSID'])

            resp = json.loads(resp.text)

            if "error" in resp or len(resp) <= 1:

                stuffs.statusText.configure(state='normal')
                stuffs.statusText.delete(0,'end')
                stuffs.statusText.insert(0,f"Error received the from API. Check if all the information is correct")
                stuffs.statusText.configure(state='disabled')

                print(resp['error']['message'])

                if resp['error']['code'] == 3:

                    stuffs.statusText.configure(state='normal')
                    stuffs.statusText.delete(0,'end')
                    stuffs.statusText.insert(0,f"Time out. Too many requests. Hopefully for only 60 seconds.")
                    stuffs.statusText.configure(state='disabled')


                return itemList

            tabsToCheck.remove(tab)

            stuffs.statusText.configure(state='normal')
            stuffs.statusText.delete(0,'end')
            stuffs.statusText.insert(0,f"Getting tab \'{tabNames['tabs'][tab]['n']}\'")
            stuffs.statusText.configure(state='disabled')

            window.update()

            for x in range(0,len(resp["items"])):

                for key in resp['items'][x]['category']:
                    category = key

                if category in ('armour','weapons','accessories') and resp["items"][x]["identified"] == False and resp['items'][x]['ilvl'] >= 60:

                    if resp['items'][x]['category'][category][0] in weapons1h:

                        try:
                            itemList['1h or Shield'] += 1
                        except:
                            itemList['1h or Shield'] = 1

                        tabsToCheck.add(tab)

                    elif resp['items'][x]['category'][category][0] in weapons2h:

                        try:
                            itemList['2h or Bow'] += 1
                        except:
                            itemList['2h or Bow'] = 1
                        
                        tabsToCheck.add(tab)


                    elif resp['items'][x]['category'][category][0] != 'quiver':

                        try:
                            itemList[resp['items'][x]['category'][category][0].capitalize()] += 1
                        except:
                            itemList[resp['items'][x]['category'][category][0].capitalize()] = 1
                        tabsToCheck.add(tab)

            tab = tab + 1


        stuffs.statusText.configure(state='normal')
        stuffs.statusText.delete(0,'end')
        stuffs.statusText.insert(0,f"Getting {infos['CHARACTER']}\'s inventory")
        stuffs.statusText.configure(state='disabled')

        window.update()

        sleep(0.3)

        callsCount += 1

        req = requests.get("https://www.pathofexile.com/character-window/get-items?accountName=" + infos['ACCOUNT'] + "&character=" + infos['CHARACTER'], cookies = infos['POESESSID'])

        resp = json.loads(req.text)


        for x in range(0,len(resp["items"])):

            for key in resp['items'][x]['category']:
                category = key

            if category in ('armour','weapons','accessories') and resp["items"][x]["identified"] == False and resp["items"][x]["inventoryId"] == 'MainInventory' and resp['items'][x]['ilvl'] >= 60:

                if resp['items'][x]['category'][category][0] in weapons1h:

                    try:
                        itemList['1h or Shield'] += 1
                    except:
                        itemList['1h or Shield'] = 1

                elif resp['items'][x]['category'][category][0] in weapons2h:

                    try:
                        itemList['2h or Bow'] += 1
                    except:
                        itemList['2h or Bow'] = 1

                elif resp['items'][x]['category'][category][0] != 'quiver':

                    try:
                        itemList[resp['items'][x]['category'][category][0].capitalize()] += 1
                    except:
                        itemList[resp['items'][x]['category'][category][0].capitalize()] = 1

        stuffs.statusText.configure(state='normal')
        stuffs.statusText.delete(0,'end')
        stuffs.statusText.insert(0,'All done.')
        stuffs.statusText.configure(state='disabled')

        n = []


        for key in itemList:

            if key == 'Ring' and key not in ('1h or Shield', '2h or Bow'):
                n.append(itemList[key]//2)

            elif key not in ('1h or Shield', '2h or Bow'):

                n.append(itemList[key])

        n.append(itemList['1h or Shield']//2 + itemList['2h or Bow'])

        stuffs.totalSets.configure(state='normal')
        stuffs.totalSets.delete(0,'end')
        stuffs.totalSets.insert(0, min(n))
        stuffs.totalSets.configure(state='disabled')

    except:

        stuffs.statusText.configure(state='normal')
        stuffs.statusText.delete(0,'end')
        stuffs.statusText.insert(0,'There was some sort of error. Please recheck all information.')
        stuffs.statusText.configure(state='disabled')

        timeCount = 0

    return itemList


class itemClass():

    nextline = 2

    def __init__(self, item):

        self.item = tkinter.Label(window,text = item)

        self.emptySpace = tkinter.Label(window, text=" ")

        self.qty = tkinter.Entry(window, width = 3)
        self.qty.insert(0,itemDict[item])
        self.qty.configure(state='disabled')

        self.line = itemClass.nextline
        itemClass.nextline += 1

    def show(self):

        self.emptySpace.grid(column = 2, row = self.line)
        self.qty.grid(column = 3, row = self.line)
        self.item.grid(column = 4, row = self.line)

    def update(self,num):

        self.qty.configure(state='normal')

        self.qty.delete(0,'end')
        self.qty.insert(0,num)
        self.qty.configure(state='disabled')

class otherStuff():

    line = 2

    def __init__(self):

        self.plg = tkinter.StringVar(window)
        self.plg.set('League')

        self.realm = tkinter.StringVar(window)
        self.realm.set('pc')

        leagues = self.getLeagues()

        self.updateButton = tkinter.Button(window,text = "Check tabs", command = updateValues, width = 10, justify = 'center')

        self.forceCheck = tkinter.Button(window, text = "Recheck All", command = forceCheckAll, width = 10, justify = 'center')

        self.cancelButton = tkinter.Button(window, text = 'Cancel', command = cancelUpdate, width = 10, justify = 'center')

        self.statusText = tkinter.Entry(window, width = 60)

        self.totalSets = tkinter.Entry(window,width = 3)

        self.totalSetsText = tkinter.Label(window, text = 'Total Sets')

        self.sessID = tkinter.Entry(window, show="*", width = 20)
        self.sessIDText = tkinter.Label(window, text="POESESSID")

        self.accountName = tkinter.Entry(window, width = 20)
        self.accountNameText = tkinter.Label(window, text='Account Name')

        self.characterName = tkinter.Entry(window, width = 20)
        self.characterNameText = tkinter.Label(window, text = 'Character Name')

        self.playerLeague = tkinter.OptionMenu(window, self.plg, *leagues)
        self.playerLeagueText = tkinter.Label(window, text = 'Player League:')

        self.playerRealm = tkinter.OptionMenu(window, self.realm, 'pc', 'xbox', 'sony' )
        self.playerRealmText = tkinter.Label(window, text = 'Player Realm:')



    def show(self):

        self.updateButton.grid(column = 5, row = self.line)

        self.forceCheck.grid(column = 5, row = self.line+1)

        self.cancelButton.grid(column =5, row = self.line+2)
        self.cancelButton.configure(state = 'disabled')

        self.statusText.grid(column = 6, row = self.line + 2)
        self.statusText.configure(state='disabled')

        self.totalSets.grid(column = 3, row = self.line + 13)
        self.totalSets.config(state='disabled')

        self.totalSetsText.grid(column = 4, row = self.line + 13)

        self.sessID.grid(column = 6, row = self.line + 4)
        self.sessIDText.grid( column = 5, row = self.line + 4)

        self.accountName.grid(column = 6, row = self.line + 5)
        self.accountNameText.grid(column = 5, row = self.line + 5)

        self.characterName.grid(column = 6, row = self.line + 6)
        self.characterNameText.grid(column = 5, row = self.line + 6)

        self.playerLeague.grid(column = 6, row = self.line + 7)
        self.playerLeagueText.grid(column = 5, row = self.line + 7)

        self.playerRealm.grid(column = 6, row = self.line + 8)
        self.playerRealmText.grid(column = 5, row = self.line + 8)

    def getLeagues(self):

        leagues = []

        leagueList = requests.get('https://www.pathofexile.com/api/leagues?type=main&realm=pc&compat=1')

        leagueList = json.loads(leagueList.text)

        for league in range(0,len(leagueList)):
            leagues.append(leagueList[league]['id'])

        return leagues


def updateValues():

    global timeCount

    if timeCount == 0 or abs(int(time() - timeCount)) >= 70:

        timeCount = time()

    stuffs.sessID.configure(state = 'disabled')
    stuffs.accountName.configure(state='disabled')
    stuffs.characterName.configure(state='disabled')
    stuffs.playerLeague.configure(state='disabled')
    stuffs.updateButton.configure(state='disabled')



    itemDict = populate(itemClasses,weapons1h,weapons2h)

    for key in itemDict:
        items[key].update(itemDict[key])

    stuffs.sessID.configure(state = 'normal')
    stuffs.accountName.configure(state='normal')
    stuffs.characterName.configure(state='normal')
    stuffs.playerLeague.configure(state='normal')
    stuffs.updateButton.configure(state='normal')

def forceCheckAll():

    del tabNames

    updateValues()

def cancelUpdate():

    global isCancel
    isCancel = True

    window.update()

    stuffs.cancelButton.configure(state='disabled')






def initialize():

    for key in itemClasses:

        items[key] = itemClass(key)

def makeRows():

    for key in items:

        items[key].show()

    stuffs.show()

itemDict = {key:0 for key in itemClasses}

items = {}

stuffs = otherStuff()

initialize()

makeRows()

window.mainloop()