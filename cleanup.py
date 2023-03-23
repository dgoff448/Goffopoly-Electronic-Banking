import os

path = "players"
playerDir = os.listdir(path)

for p in playerDir:
    if p != "roster.txt" and p != "Free Parking.txt":
        os.remove(f"players/{p}")

with open("players/Free Parking.txt", 'w') as f:
    f.write("0")

with open("players/roster.txt", 'w') as f:
    f.write("Free Parking\n")

with open("transactionLogs.txt", 'w') as f:
    f.write("")