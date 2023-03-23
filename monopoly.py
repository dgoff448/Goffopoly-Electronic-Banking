#!/usr/bin/env python3

# Next line disables pylint warnings about bottle.request.params:
# pylint: disable=E1135,E1136
Name = 'NotWorking'
money = 420420
from os import name
import re
from flask import Flask, send_from_directory, request, render_template
import os.path
from pygame import mixer

from werkzeug.datastructures import ImmutableHeadersMixin


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

app = Flask(__name__)

class Player():
    def __init__(self, Name, money):
        self.Name = Name
        self.money = money
        with open('players/' + Name + '.txt', 'w') as f:
            f.write(str(self.money))
        with open('players/roster.txt', 'a') as f:
            f.write(str(self.Name + '\n'))


class payPlayerButtons():
    def __init__(self):
        self.buttons = ""
        file = open('players/roster.txt', 'r')
        lines = file.readlines()

        for line in lines:
            player = line.strip()
            self.buttons = self.buttons + f"""
            <input type='submit' name='action' value='{player}' style="font-size: 32px;  height: 100px;  width: 300px" /><br><br>"""  

class playerAccounts():
    def __init__(self):
        self.accounts = ""
        file = open('players/roster.txt', 'r')
        lines = file.readlines()

        for line in lines:
            player = line.strip()
            moneyFile = open(f'players/{player}.txt')
            money = moneyFile.readline()
            self.accounts = self.accounts + f"""
            <p style='font-size:300%;'>{player}: ${money}</p>"""  




def PayMoney(receiver, amount, name):
    with open("players/" + receiver + ".txt", 'r') as f:
        recMoney = int(f.readline().strip())
    newRecMoney = recMoney + amount

    with open("players/" + receiver + ".txt", 'w') as f:
        f.write(str(newRecMoney))

    with open("players/" + name + ".txt", 'r') as f:
        recMoney = int(f.readline().strip())
    newSenderMoney = recMoney - amount

    with open("players/" + name + ".txt", 'w') as f:
        f.write(str(newSenderMoney))

    
    with open("transactionLogs.txt", "a") as f:
        f.write(name + " payed " + receiver + " $" + str(amount) + ".\n")

    return newSenderMoney

def passGo(name, money):
    with open("players/" + name + ".txt", 'r') as f:
        Money = int(f.readline().strip())
    newMoney = Money + 200

    with open("players/" + name + ".txt", 'w') as f:
        f.write(str(newMoney))

    with open("transactionLogs.txt", "a") as f:
        f.write(name + " collected $200 while passing Go.\n")
    return

def freeParking(name):
    with open("players/Free Parking.txt", 'r') as f:
        FreeMoney = int(f.readline().strip())
    with open("players/Free Parking.txt", 'w') as f:
        f.write(str(0))

    with open("players/" + name + ".txt", 'r') as f:
        Money = int(f.readline().strip())
    newMoney = Money + FreeMoney
    with open("players/" + name + ".txt", 'w') as f:
        f.write(str(newMoney))
    
    with open("transactionLogs.txt", "a") as f:
        f.write(name + " collected $" + str(FreeMoney) + " from Free Parking.\n")
    return

def bail(name):
    with open("players/" + name + ".txt", 'r') as f:
        Money = int(f.readline().strip())
    newMoney = Money - 50
    with open("players/" + name + ".txt", 'w') as f:
        f.write(str(newMoney))

    with open("players/Free Parking.txt", 'r') as f:
        FreeMoney = int(f.readline().strip())
    with open("players/Free Parking.txt", 'w') as f:
        f.write(str(FreeMoney + 50))

    with open("transactionLogs.txt", "a") as f:
        f.write(name + " payed a $50 bail.\n")

def Refresh(name):
    with open("players/" + name + ".txt", 'r') as f:
        money = int(f.readline().strip())
    return money

def playMusic():
    mixer.init()
    mixer.music.load('sounds/kerching.mp3')
    mixer.music.play()
    return

def freeParkMusic():
    mixer.init()
    mixer.music.load('sounds/freeParking (2).mp3')
    mixer.music.play()
    return

def passGoMusic():
    mixer.init()
    mixer.music.load('sounds/passGo.mp3')
    mixer.music.play()
    return

def bailMusic():
    mixer.init()
    mixer.music.load('sounds/bail.mp3')
    mixer.music.play()
    return


@app.route('/<path:filename>')
def send_static(filename):
    if filename.endswith('.py'):
        return "You may not have that file."

    return send_from_directory(dir_path, filename)

@app.route('/')
def index():
    """Home page."""
    return render_template("title.html")

game = None


@app.route('/play')
def play():
    file = open('players/roster.txt', 'r')
    lines = file.readlines()
    """Gameplay page request handler."""
    action = request.args["action"]

    if action == "Ready Up":
        Name = str(request.args["Name"])
        if not (Name.isalpha() or Name == "%Bank%"):
            return render_template("title.html")
        elif ("Bank" in Name or "bank" in Name) and Name != "%Bank%":
            return render_template("title.html")
        elif Name == "%Bank%":                    # special instructions for the Bank
            player = Player("Bank", 100000000)
            Name = "Bank"
            return render_template("bank.html").format(Name, player.money)
        else:
            player = Player(Name, 1500)
            return render_template("game.html").format(Name, player.money)
    elif action == "test":
        # return TEST_JS_HTML
        return render_template("test.html")
    elif action == "Pay Money":
        info = str(request.args["info"])
        splitInfo = info.split(":")
        Name = splitInfo[0]
        money = Refresh(Name)
        buttons = payPlayerButtons()
        return render_template("pay.html").format(Name, money, buttons.buttons)
    elif action == "Pay":
        info = str(request.args['info'])
        splitInfo = info.split(":")
        Name = splitInfo[0]
        money = Refresh(Name)
        receiver = splitInfo[2]

        amount = int((str(request.args['Amount'])).strip())
        newMoney = PayMoney(receiver, amount, Name)
        playMusic()
        if Name == "Bank":
            return render_template("bank.html").format(Name, newMoney)
        else:
            return render_template("game.html").format(Name, newMoney)
    elif action == "Refresh" or action == "Back":
        info = str(request.args['info'])
        splitInfo = info.split(":")
        Name = splitInfo[0]
        money = Refresh(Name)
        if Name == "Bank":
            return render_template("bank.html").format(Name, money)
        else:
            return render_template("game.html").format(Name, money)
    elif action == "Pass Go":
        info = str(request.args['info'])
        splitInfo = info.split(":")
        Name = splitInfo[0]
        money = Refresh(Name)
        passGo(Name, money)
        passGoMusic()
        money = Refresh(Name)
        return render_template("game.html").format(Name, money)
    elif action == "Collect Free Parking Pot":
        info = str(request.args['info'])
        splitInfo = info.split(":")
        Name = splitInfo[0]
        freeParking(Name)
        freeParkMusic()
        money = Refresh(Name)
        return render_template("game.html").format(Name, money)
    elif action == "Bail":
        info = str(request.args['info'])
        splitInfo = info.split(":")
        Name = splitInfo[0]
        bail(Name)
        bailMusic()
        money = Refresh(Name)
        return render_template("game.html").format(Name, money)
    elif (action + "\n") in lines:
        info = str(request.args['info'])
        splitInfo = info.split(":")
        Name = splitInfo[0]
        money = Refresh(Name)
        return render_template("pay2.html").format(Name, money, action)

    elif action == "Player Accounts":
        info = str(request.args['info'])
        splitInfo = info.split(":")
        Name = splitInfo[0]
        money = Refresh(Name)
        acnt = playerAccounts()
        return render_template("accounts.html").format(Name, money, acnt.accounts)




# Boilerplate bootstrapping logic for running as a standalone program
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
    # app.run(host="127.0.0.1", port=3000, debug=True)