import tkinter
import requests
import json
from tkinter import messagebox
from os.path import exists
from os import fsync
from ast import literal_eval

window = tkinter.Tk()
window.title("PoE Simple Chaos Recipe Helper")


itemClasses = ('1h, 2h or Shield', 'Helmet', 'Chest','Gloves','Boots', 'Belt', 'Amulet', 'Ring')
weaponTypes = ('dagger','claw','onesword','wand','shield','oneaxe','staff','twomace','twoaxe','twosword','bow')


  
def populate(itemList, weaponTypes):
    poesessid = {"POESESSID":'754a6b913eb8f1cfd26e45375ab28119'}

    itemList = {k:0 for k in itemList}

    #itemList = {'1h, 2h or Shield':0, 'Helmet':0, 'Chest':0, 'Gloves':0, 'Boots':0, 'Belt':0,'Amulet':0,'Ring':0}

    for tab in range(0,12):
        print(f"getting tab {tab}")
        req = requests.get("https://www.pathofexile.com/character-window/get-stash-items?accountName=Garulf161&tabIndex= " + str(tab) + "&league=Legion", cookies=poesessid)

        resp = json.loads(req.text)


        for x in range(0,len(resp["items"])):

            for key in resp['items'][x]['category']:
                category = key

            if category in ('armour','weapons','accessories') and resp["items"][x]["identified"] == False:
            
                #print("Unidentified ",end="")
                #print(f"{resp['items'][x]['category'][category][0]} in tab {tab}")

                #statusText.

                if resp['items'][x]['category'][category][0] in weaponTypes:
                       
                    try:
                        itemList['1h, 2h or Shield'] += 1
                    except:
                        itemList['1h, 2h or Shield'] = 1

                elif resp['items'][x]['category'][category][0] != 'quiver':

                    try:
                        itemList[resp['items'][x]['category'][category][0].capitalize()] += 1
                    except:
                        itemList[resp['items'][x]['category'][category][0].capitalize()] = 1

    return itemList
        

class itemClass():

    nextline = 2

    def __init__(self, item):

        self.item = tkinter.Label(window,text = item)

        #self.buttonUp = tkinter.Button(window, text="/\\", command = self.inc)
        #self.buttonDown = tkinter.Button(window, text="\\/", command = self.dec)

        self.emptySpace = tkinter.Label(window, text=" ")

        self.qty = tkinter.Entry(window, width = 3,)
        self.qty.insert(0,itemDict[item])
        self.qty.configure(state='disabled')

        self.line = itemClass.nextline
        itemClass.nextline += 1

    def inc(self):

        self.qty.configure(state='normal')

        num = int(self.qty.get()) + 1

        self.qty.delete(0,'end')
        self.qty.insert(0,num)
        itemDict[self.item.cget("text")] = num
        self.qty.configure(state='disabled')

    def dec(self):

        self.qty.configure(state='normal')

        num = int(self.qty.get()) - 1

        if num < 0:
            num = 0

        self.qty.delete(0,'end')
        self.qty.insert(0,num)
        itemDict[self.item.cget("text")] = num
        self.qty.configure(state='disabled')

    def show(self):

        #self.buttonUp.grid(column = 0,row = self.line)
        #self.buttonDown.grid(column = 1, row = self.line)
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

        self.updateButton = tkinter.Button(window,text = "Updoot", command = updateValues)        

        self.statusText = tkinter.Entry(window, width = 20)
        

    def show(self):

        self.updateButton.grid(column = 6, row = self.line)
        self.statusText.grid(column = 6, row = self.line + 1)
        self.statusText.configure(state='disabled')

def decAll():

    isZero = False

    for key in itemClasses:

        if int(items[key].qty.get()) == 0:

            isZero = True

    if isZero == False:

        for key in itemClasses:

            items[key].dec()

def incAll():       

    for key in itemClasses:

        items[key].inc()

def updateValues():
    
    itemDict = populate(itemClasses,weaponTypes)

    for key in itemDict:
        items[key].update(itemDict[key])



def initialize():

    for key in itemClasses:

        items[key] = itemClass(key)

def makeRows():

    for key in items:

        items[key].show()

    stuffs.show()

def reset():
        
    if messagebox.askyesno("","You really want to reset?", parent=window):

        for key in itemClasses:

            items[key].qty.configure(state='normal')

            items[key].qty.delete(0,'end')
            items[key].qty.insert(0,0)
            itemDict[items[key].item.cget("text")] = 0
            items[key].qty.configure(state='disabled')


itemDict = {key:0 for key in itemClasses}

#decAllButton = tkinter.Button(window, text = "\\/ All", command = decAll)
#incAllButton = tkinter.Button(window, text = "/\\ All", command = incAll)



#incAllButton.grid(column = 0, row = 13)
#decAllButton.grid(column = 1, row = 13)

#resetButton = tkinter.Button(window, text = "Reset", command = reset)
#resetButton.grid(column = 3, row = 13)



items = {}

stuffs = otherStuff()

initialize()

makeRows()

window.mainloop()