from fileManager import *

#Waits;
#Friend's profile wait;
"""profileMin = 1 #Minimum profile-to-hatchery navigation time;
profileMax = 4 #Maximum ^;

#Hatchery;
hatchMin = 3 #Minimum hatchery navigation time;
hatchMax = 6 #Maximum ^;

#Egg Search;
searchMin = 1 #Minimum search for eggs cooldown;
searchMax = 4 #Maximum ^;

#Click "Turn egg" wait;
clickTurnMin = 0.4 #Minimum click "Turn egg" button cooldown;
clickTurnMax = 0.9 #Maximum ^;

#"Found credit" prompt click "Ok";
creditMin = 2 #Minimum click "Ok" after finding credit button cooldown;
creditMax = 4 #Maximum ^;

#Click "Next" button;
nextMin = 0.2 #Minimum click "Next" after turning egg button cooldown;
nextMax = 0.7 #Maximum ^;"""

def SaveOptions(settings, array, file, window):
    reader = open(file, "r")
    lines = reader.readlines()
    options = open(file, "w+")

    options.write(lines[0]) #Writing down the collected credits thus far
    i = 0

    for setting in settings:
        array[i] = setting
        options.write(str(setting) + "\n")

    options.close()
    window.destroy()

def LoadOptions(file):
    reader = open(file, "r")
    return reader.readlines()

turnSettings = LoadOptions(optionsFile)
"""Turn Settings:
        0: Credits collected
        1-2: Profile
        3-4: Hatchery
        5-6: Egg Search
        7-8: Turn Button Click
        9-10: Found credit Ok click
        11-12: Next button 
        13-14: Feed cooldown"""