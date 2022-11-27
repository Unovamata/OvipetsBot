import threading, selenium
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from optionsBot import *
import fileManager
from fileManager import *
import eggTurnerBot
from GUI import *
import random
import time
from playsound import playsound

#Options;
i = 0
canRun = bool(0)
options = Options()
options.add_experimental_option("detach", True) #Keep if completed
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#Humanizing the search;
loginBottom = 1
loginCeilling = 6
parallel_thread = threading.Thread()
HATCHERIES = None

def LogIn(console):
    driver.get(MAINPAGE)  # Go to log-in;

    try:
        driver.find_element(By.XPATH, '//*[@id="login_signup"]').click()
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH, '//*[@name="Email"]').send_keys(email)
        driver.find_element(By.XPATH, '//*[@name="Password"]').send_keys(password)
        driver.find_element(By.XPATH, "//button[@class='ui-button ui-corner-all ui-widget']").click()
        DrawConsoleText(console, "Logged in!", g)
        time.sleep(SleepRandom(loginBottom, loginCeilling))
    except:
        DrawConsoleText(console, "Navigating to the Ovipets Homepage", b)

def BotStart(console, creditsGotten, type):
    currentFriend = 0 #Resetting the friend index;
    DrawConsoleText(console, "Bot started! Please wait...", g)
    LogIn(console)

    #Setup the browser;
    eggTurnerBot.i = 0
    match type:
        case 0: #Credit Farmer;
            parallel_thread = threading.Thread(target=EggTurnerBotGetUser, args=(console, creditsGotten,), daemon=True)
            parallel_thread.start()
        case 1: #Egg Hatcher
            threading.Thread(target=AutoEggHatcher, args=(console,), daemon=True).start()

    # driver.maximize_window()

#Humanizing the search;
currentFriend = 0

def EggTurnerBotGetUser(console, creditsGottenLabel):
    #Navigating to the page of a random friend;
    eggTurnerBot.currentFriend = 0
    driver.get(GetFriendProfile(console))
    time.sleep(SleepRandom(loginBottom, loginCeilling))

    # Getting friend's hatchery;
    driver.get(GetFriendHatchery(console))
    tv = 0 #Turn variable
    while(eggTurnerBot.currentFriend <= len(friendsList) - 1 and i == 0):
        tv = 0
        #Extracting an egg link;
        time.sleep(SleepRandom(turnSettings[5], turnSettings[6]))
        elements = driver.find_elements(By.XPATH,'//*[@id="hatchery"]//child::li//*[@title="Turn Egg"]/../../a[@href]')
        time.sleep(SleepRandom(turnSettings[3], turnSettings[4]))  # Navigating to hatchery and waiting;

        links = [elem.get_attribute('href') for elem in elements]
        eggs = len(links)


        #Go to the egg link, if not, go to a friend's hatchery
        if(eggs > 0):
            if(eggs == 1): DrawConsoleText(console, "Found 1 Turnable egg!", g)
            if (eggs > 1): DrawConsoleText(console, "Found " + str(eggs) + " Turnable eggs!", g)
            driver.get(links[0]) #If eggs are turnable, go there
            DrawConsoleText(console, "Egg selected...", g)
            #Turning eggs;

            while(tv < 1):
                if(eggs == 0): tv = 1
                time.sleep(SleepRandom(turnSettings[7], turnSettings[8]))
                #If "Turn Egg" is found, then turn it and continue;
                try:
                    try:
                        driver.find_element(By.XPATH, '//span[text()="Turn Egg"]/..').click()
                    except:
                        del links[0]
                        DrawConsoleText(console, "Can not turn egg...\nReturning to the hatchery...", r)
                        driver.get(GetFriendHatchery(console))
                        time.sleep(SleepRandom(turnSettings[5], turnSettings[6]))

                    # Collecting credits;
                    try:
                        creditPopup = driver.find_element(By.XPATH, '//button[text()="Ok"]')
                        DrawConsoleText(console, "CREDIT FOUND!!", c)
                        fileManager.creditsFoundThisSession += 1
                        creditsGottenLabel.config(text="Total Credits Obtained: " + str(fileManager.creditsFound)
                                                       + " + " + str(fileManager.creditsFoundThisSession),
                                                  fg="green", font='Helvetica 9 bold')
                        UpdateCreditOption()
                        playsound(currentDirectory + '/sounds/CreditFound.wav')
                        time.sleep(SleepRandom(turnSettings[9], turnSettings[10]))
                        creditPopup.click()

                    except: print()

                    # Checking on the next egg;
                    driver.find_element(By.XPATH, '//*[@title="Next"]').click()
                    time.sleep(SleepRandom(turnSettings[11], turnSettings[12]))
                except: #If not, go back to hatchery;
                    #DrawConsoleText(console, "No turnable eggs found...\nReturning to the hatchery...", r)
                    del links[:]
                    tv = 1
        else:
            DrawConsoleText(console, "Found 0 Turnable eggs...", g)
            DrawConsoleText(console, "No turnable eggs were found...\nSwitching profiles...", r)
            eggTurnerBot.currentFriend += 1

            driver.get(MAINPAGE)  # Returning to profile
            time.sleep(SleepRandom(loginBottom, loginCeilling))  # Navigating to hatchery and waiting;
            try:
                driver.get(GetFriendProfile(console)) #If not, search another friend;
                # Getting friend's hatchery;
                time.sleep(SleepRandom(loginBottom, loginCeilling))  # Navigating to hatchery and waiting;
                driver.get(GetFriendHatchery(console))
                del links[:]
                time.sleep(SleepRandom(turnSettings[3], turnSettings[4]))
            except: print("")
    if(fileManager.creditsFoundThisSession == 1): DrawConsoleText(console, "Bot stopped, you got " + str(fileManager.creditsFoundThisSession) + " credit!", g)
    else: DrawConsoleText(console, "Bot stopped, you got " + str(fileManager.creditsFoundThisSession) + " credits!", g)

    playsound(currentDirectory + '/sounds/TaskFinished.wav')

def GetFriendHatchery(console):
    user = eggTurnerBot.friendLines[currentFriend].split(":")
    id = user[0]
    name = user[1]
    DrawConsoleText(console, "Navigating to " + name.strip("\n") +"'s" + " hatchery!", b)
    return FactorHatcheryString(id)

def GetFriendProfile(console):
    user = eggTurnerBot.friendLines[currentFriend].split(":")
    id = user[0]
    name = user[1]
    DrawConsoleText(console, "Navigating to " + name.strip("\n") +"'s" + " profile!", b)
    return FactorProfileString(id)

def StopBot(console):
    if(eggTurnerBot.i == 0):
        DrawConsoleText(console, "Stopping execution... Please wait until you hear the termination sound...", r)
        eggTurnerBot.i = 1
        eggTurnerBot.currentFriend = 0

def SleepRandom(floor, ceilling):
    r = round(random.uniform(float(floor), float(ceilling)), 2)
    string = "Sleeping for " + str(r) + " seconds"
    #DrawConsoleText(CONSOLE, string, bl)
    return r

#Humanizing the search;
refreshBottom = 0.5
refreshCeilling = 2

#Return the player ID
def FactorIdString(string):
    string = string[23:]
    string = string.replace('?usr=', '')
    return string

def RefreshFriends(console, hatcheries):
    DrawConsoleText(console, "Refreshing Friends!", g)
    StopBot(console)
    LogIn(console)  # If not logged in, then, log in;

    #try:
    SleepRandom(refreshBottom, refreshCeilling)
    try:
        driver.find_element(By.XPATH, "//span[text()='Friends']/..").click()
    except:
        Delete()
    SleepRandom(refreshBottom, refreshCeilling)
    #driver.find_element(By.XPATH, "//span[contains(text(),'Favourites (')]/../..").click()

    #Extracting the profile link;
    favorited = driver.find_elements(By.XPATH, "//div[@class='ui-fieldset-body']/fieldset/div/ul/li/a[@href]")
    friendsLinks = [links.get_attribute("href") for links in favorited]
    favoritedNames = driver.find_elements(By.XPATH, "//div[@class='ui-fieldset-body']/fieldset/div/ul/li/a/img[@title]")
    friendsNames = [names.get_attribute("title") for names in favoritedNames]

    count = 0
    file = open(friendsFile, "w") #Resetting the friends file;
    file.truncate()
    file.close()

    #Extracting the links and the ids;
    for links in friendsLinks:
        AddFriend(FactorIdString(links) + ":" + friendsNames[count])
        count += 1

    eggTurnerBot.friendLines = open(friendsFile, "r", encoding="utf-8").readlines()
    eggTurnerBot.currentFriend = 0
    hatcheries.delete(0, END)

    # Reloading the random friends;
    LoadFriends(hatcheries, console)

def RandomizeFriends(hatcheries, console):
    eggTurnerBot.friendLines = list(hatcheries.get(0, END)) #Loading any custom friends the user has too;
    random.shuffle(eggTurnerBot.friendLines)
    hatcheries.delete(0, END)
    DrawConsoleText(console, "Randomized friends!", g)

    #Reloading the random friends;
    for line in eggTurnerBot.friendLines:
        hatcheries.insert(END, line)

def EmptyFriendsList(hatcheries, console):
    hatcheries.delete(0, END)
    del friendsList[:]
    DrawConsoleText(console, "Cleared the current hatcheries to check!", g)

def FriendAddUpdate(profile, hatcheries, console):
    WriteFriend(profile, hatcheries, console)
    del eggTurnerBot.friendsList[:]
    eggTurnerBot.friendLines = list(hatcheries.get(0, END))  # Loading any custom friends the user has too;

#Delete friends from the program;
def DeleteFriends(hatcheries):
    index = -1
    try:
        selectedValue = str(hatcheries.curselection())
        selection = selectedValue.strip("(,)")
        hatcheries.delete(ANCHOR)
        index = int(selection)

        #Rewritting friends file;
        with open(friendsFile, encoding="utf-8") as file:
            lines = file.readlines()
            #Deleting the selected index
            del lines[index]

            with open(friendsFile, "w", encoding="utf-8") as file:
                for line in lines: file.write(line)
    except:
        if(index == -1): Popup("Can not delete an unselected friend")
        elif(index > hatcheries.size() - 1): print("")

    del eggTurnerBot.friendLines[:]
    eggTurnerBot.friendLines = list(hatcheries.get(0, END))  # Loading any custom friends the user has too;

#Delete friends from the queue;
def RemoveFromHatcheries(hatcheries):
    index = -1
    try:
        selectedValue = str(hatcheries.curselection())
        selection = selectedValue.strip("(,)")
        hatcheries.delete(ANCHOR)
        index = int(selection)
    except:
        if(index == -1): print("")
        elif(index > hatcheries.size() - 1): print("")

    del eggTurnerBot.friendLines[:]
    eggTurnerBot.friendLines = list(hatcheries.get(0, END))  # Loading any custom friends the user has too;

######################################################################################

def AutoEggHatcher(console):
    hatchString = '//*[@id="hatchery"]//child::li//*[@title="Hatch Egg"]/../../a[@href]'
    time.sleep(SleepRandom(loginBottom, loginCeilling))

    # Getting friend's hatchery;
    driver.get(MYHATCHERY)
    DrawConsoleText(console, "Navigating to your hatchery!", b)
    delay = 5

    while(True):
        if(i == 1): break

        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, hatchString)))
            elements = driver.find_elements(By.XPATH, hatchString)
            links = [elem.get_attribute('href') for elem in elements]
            eggs = len(links)

            #Navigating to egg page;
            driver.get(links[0])  # If eggs are turnable, go there
            DrawConsoleText(console, "Egg selected...", g)

            #Clicking the hatch egg button;
            species = driver.find_element(By.XPATH, '//div[@class="value"]/p').text
            time.sleep(SleepRandom(turnSettings[7], turnSettings[8]))
            driver.find_element(By.XPATH, '//span[text()="Hatch Egg"]/..').click()
            DrawConsoleText(console, species + " egg hatched!", g)
            time.sleep(SleepRandom(turnSettings[7], turnSettings[8]))
            DrawConsoleText(console, "Returning to the hatchery...", b)
            driver.get(MYHATCHERY)
            time.sleep(SleepRandom(turnSettings[3], turnSettings[4]))
        except TimeoutException:  # There are no eggs to hatch;
            break

    DrawConsoleText(console, "Bot stopped!", g)
    playsound(currentDirectory + '/sounds/TaskFinished.wav')

######################################################################################

def FeederStart(console):
    LogIn(console)
    parallel_thread = threading.Thread(target=FeederBotLogic, args=(console,), daemon=True).start()


currentTab = 0

def FeederBotLogic(console):
    # Navigating to my pet page;
    currentTab = 0
    petsFed = 0
    driver.get(MYPETS)
    DrawConsoleText(console, "Navigating to your pets page", b)

    #Loading all the leading in memory;
    DrawConsoleText(console, "Loading 'Leading Pets', please wait...", b)
    while True:
        try:
            tabs = driver.find_elements(By.XPATH, "//ul[@role]//a")  # Finding the tabs;
            if (currentTab >= len(tabs)): break
            tabs[currentTab].click()
            currentTab += 1
            time.sleep(SleepRandom(0.5, 1))
        except: #If there are no pets in tab;
            currentTab += 1

    #Finding the first pets per tab;
    leadingPets = driver.find_elements(By.XPATH, "//ul[@class='ui-sortable']/li[1]//a/img/..")
    time.sleep(SleepRandom(loginBottom, loginCeilling))
    petsLinks = [links.get_attribute('href') for links in leadingPets]
    currentTab = 0
    DrawConsoleText(console, "Leading pets loaded!", g)

    while True:
        #Navigating through the tabs;
        tabsFound = driver.find_elements(By.XPATH, "//ul[@role]//a") # Finding the tabs;
        if(currentTab >= len(tabsFound)): break
        tabsFound[currentTab].click()
        DrawConsoleText(console, "Feeding pets in '" + tabsFound[currentTab].text + "' tab...", b)
        time.sleep(SleepRandom(0.5, 1)) #Tab click wait;

        #Visitting the first pet of any tab;
        firstPet = petsLinks[currentTab]
        driver.get(firstPet)  # Go to the first pet page to feed them
        time.sleep(SleepRandom(0.6, 3))

        #Variables;
        isLead = True #Is it the first time the program goes to the first pet page?

        while(True):
            #Extracting the pet name;
            """try:
                petName = driver.find_element(By.XPATH, "//span[@class='ui-section-title']").text
            except: petName = "Pet"""

            try: #If the pet can be fed;
                time.sleep(SleepRandom(0.4, 0.8))
                driver.find_element(By.XPATH, "//span[.='Feed']/..").click()
                #DrawConsoleText(console, petName + " Fed!", g)
                petsFed += 1
                time.sleep(SleepRandom(0.2, 0.5))
            except: print("") #DrawConsoleText(console, "Pet already fed...", r)

            #Telling the program it is the first time the first pet is seen;
            time.sleep(SleepRandom(0.3, 0.6))

            # Next pet;
            time.sleep(SleepRandom(turnSettings[11], turnSettings[12]))
            driver.find_element(By.XPATH, '//*[@title="Next"]/.').click()

            # Breaking out of the loop;
            if (isLead):
                isLead = False
            else:
                if (driver.current_url == firstPet + "&next=1"):
                    DrawConsoleText(console, "All pets in the current tab were fed!", g)
                    DrawConsoleText(console, "Navigating to the next tab...", b)

                    driver.get(MYPETS)
                    currentTab += 1
                    time.sleep(SleepRandom(0.8, 2))
                    break

    DrawConsoleText(console, "Bot stopped!", g)
    if(petsFed == 1): DrawConsoleText(console, "1 pet fed!", g)
    else: DrawConsoleText(console, str(petsFed) + " pets fed!", g)
    playsound(currentDirectory + '/sounds/TaskFinished.wav')

    #Clicking the tabs;
    #print(tabsFound)