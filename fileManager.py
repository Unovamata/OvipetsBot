from datetime import datetime
import os
from tkinter import *

#Memory
creditsFound = 0
creditsFoundThisSession = 0

#Console text types / tags;
b = "C" #Comment / Blue
g = "S" #Success / Green
r = "W" #Warning / Red
bl = "N" #Normal / Black
c = "Cr" #Credit Obtained / Yellow background;

# Directory
currentDirectory = os.path.realpath('.')
friendsFile = currentDirectory + "/" + "Friends List.txt"
accountFile = currentDirectory + "/" + "Account.txt"
optionsFile = currentDirectory + "/" + "TurnerOptions.txt"
HATCHERY = "https://ovipets.com/#!/?src=pets&sub=hatchery&usr="
PROFILE = "https://ovipets.com/#!/?usr="
CUSTOMPROFILE = "https://ovipets.com/#!/"
MAINPAGE = "https://ovipets.com/"
MYHATCHERY = "https://ovipets.com/#!/?src=pets&sub=hatchery"
MYPETS = "https://ovipets.com/#!/?src=pets&sub=overview"

# Account credentials;
email = ""
password = ""
username = ""

#Account file; It triggers login;
if (os.path.isfile(accountFile)):
    account = open(accountFile, "r")
    email = account.readline()
    password = account.readline()
    login = bool(1)
else:
    login = bool(0)

if (os.path.isfile(optionsFile)):
    opt = open(optionsFile, "r")
    creditsFound = int(opt.readline())
    opt.close()
else:
    opt = open(optionsFile, "w+")
    opt.write("0\n")
    opt.close()

friendsList = []

if (os.path.isfile(friendsFile)):
    opt = open(friendsFile, "r", encoding="utf-8")
    friendsList = opt.readlines()
    opt.close()
else:
    opt = open(friendsFile, "w+")
    opt.close()

#Add a friend to the friend file;
def AddFriend(string):
    #If it founds the file
    if (os.path.isfile(friendsFile)): #Adding into the file;
        friends = open(friendsFile, "a", encoding="utf-8")
        friends.write(string+"\n")
    else: #Creating the file from zero;
        friends = open(friendsFile, "w+", encoding="utf-8")
        friends.write(string+"\n")

#Create the hatchery url;
def FactorHatcheryString(string):return HATCHERY + string

#Create the hatchery url;
def FactorProfileString(string): return PROFILE + string

def FactorURL(string):
    string = string.replace('https://ovipets.com/#!/?src=pets&sub=hatchery&usr=', '')
    string = string.replace('https://ovipets.com/#!/', '')
    string = string.replace('?usr=', '')
    string = string + ":Friend"
    return string

#Create a specific file if it's null;
def CreateFileIfNull(route):
    if (os.path.isfile(route)): return bool(0)
    else:
        f = open(route, "w+")
        return bool(1)

#GUI write friend status;
def WriteFriend(profile, hatcheries, console):
    if(profile == ""):
        Popup("The profile can not be blank")
        return 0

    #Checking if the link is a hatchery;
    if("https://ovipets.com" in profile):
        hatcheries.insert(END, FactorURL(profile))
        DrawConsoleText(console, "New friend added!", g)
    else: Popup("The URL entered is not a valid Ovipets URL")

#Loading friends from file;
def LoadFriends(hatcheries, console):
    if(CreateFileIfNull(friendsFile) == bool(1)): return 0

    hatcheries.delete(0, END)
    with open(friendsFile, encoding="utf-8") as f:
        for line in f:
            hatcheries.insert(END, line)
    DrawConsoleText(console, "Friends loaded!", g)


def Popup(message):
    popup = Toplevel()
    popup.title("Alert")
    CalculateDimensions(400, 100, popup)

    frame = Frame(popup)

    popupMessage = Label(frame, text=message, pady=20).pack()
    popupButton = Button(frame, text="Ok", command=lambda t="":popup.destroy()).pack()
    frame.pack(expand=True)

def CalculateDimensions(width, height, window):
    w = width #Width;
    h = height #Height;
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()

    #Calculating the screen's position
    x = (screenWidth / 2) - w / 2
    y = (screenHeight / 2) - h / 2
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

def DrawConsoleText(console, text, tag):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    console.insert(END, "[" + current_time + "]: " + text + "\n", tag)

def UpdateCreditOption():
    read = open(optionsFile, "r")
    lines = read.readlines()
    opt = open(optionsFile, "w")
    lines[0] = str(creditsFound + creditsFoundThisSession) + "\n"
    for line in lines:
        opt.write(line)
    opt.close()