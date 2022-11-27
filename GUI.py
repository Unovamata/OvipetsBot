import tkinter
from tkinter import *
import fileManager
from eggTurnerBot import *
from main import *
from optionsBot import *

def LoginScreen():
    root.title("Ovipets Log-in Credentials")
    frame = Frame(root)
    frame.pack()

    #Frame title;
    loginFrame = LabelFrame(frame, text="Ovipets Login Credentials:")
    loginFrame.grid(row = 0, column = 0, pady=20)

    #Username
    usernameLabel = Label(loginFrame, text="Ovipets Email:")
    usernameInput = Entry(loginFrame, width=40)
    usernameLabel.grid(row=0, column=0, pady=20, padx=20)
    usernameInput.grid(row = 0, column = 1, pady=(10, 0), padx=20)

    #Password
    passwordLabel = Label(loginFrame, text="Ovipets Password:")
    passwordInput = Entry(loginFrame,  show="*", width=40)
    passwordLabel.grid(row=1, column=0, pady=20, padx=20)
    passwordInput.grid(row=1, column=1, pady=(10, 0), padx=20)

    # Confirm and delete credentials
    confirm = Button(loginFrame, text="Confirm", command=lambda t="":Confirm(usernameInput.get(), passwordInput.get(), frame))
    confirm.grid(row=2, column=1, pady=(0, 10), padx=10)
    remove = Button(loginFrame, text="Delete credentials file", command=lambda t="":Delete())
    remove.grid(row=2, column=0, pady=(0, 10), padx=10)

    notePassword1 = Label(text="This program will not steal your credentials!")
    notePassword2 = Label(text="We need this information to log the bot in your account.")
    notePassword3 = Label(text="You will need to enter this information once, unless you change it later on.")
    notePassword1.pack()
    notePassword2.pack()
    notePassword3.pack()

    #if(confirm)

def Confirm(email, password, window):
    if(email != "" and password != ""):
        account = open(accountFile, "w+")
        account.write(email + "\n")
        account.write(password)
        MainMenuGUI(username)
        fileManager.email = email
        fileManager.password = password
        window.destroy()
        print(email + "\n" + password)
    else: Popup("Email or password not valid")

def Delete():
    if (os.path.isfile(accountFile)):
        account = open(accountFile, "r")
        account.close()
        os.remove(accountFile)
        Popup("File removed! Please, enter your credentials again.")
    else: Popup("The file does not exists...")

def MainMenuGUI(username):
    mainMenu = Toplevel(root)
    CalculateDimensions(450, 300, mainMenu)
    root.withdraw()
    mainMenu.title("Ovipets Automation Tool")

    #Calling the bot;
    #EggTurnerBotStart()

    #Frames;
    frame = tkinter.Frame(mainMenu)
    frame.pack()

    # Frame title;
    botsFrame = LabelFrame(frame, text="Welcome " + username + "!")
    botsFrame.grid(row=0, column=0, pady=20)

    # Opening Submenus
    eggTurnerButton = Button(botsFrame, text="Auto Egg Turner Bot", command=lambda t="":EggTurnerGUI())
    eggTurnerButton.grid(row=0, column=0, pady=15, padx=10)
    autoFeeder = Button(botsFrame, text="Auto Feeder Bot", command=lambda t="":AutoFeederGUI())
    autoFeeder.grid(row=0, column=1, pady=15, padx=10)
    autoBreeder = Button(botsFrame, text="Auto Pet Breeder")
    autoBreeder.grid(row=1, column=0, pady=15, padx=10)
    autoHatcher = Button(botsFrame, text="Auto Hatcher Bot", command=lambda t="" : EggHatcherGUI())
    autoHatcher.grid(row=1, column=1, pady=15, padx=10)
    autoSelfEggTurner = Button(botsFrame, text="Self Egg Turner Bot")
    autoSelfEggTurner.grid(row=2, column=0, pady=15, padx=10)
    autoFavorite = Button(botsFrame, text="Auto Friend Favorite")
    autoFavorite.grid(row=2, column=1, pady=15, padx=10)
    quitProgram = Button(botsFrame, text="Quit Program", command= lambda:CloseProgram())
    quitProgram.grid(row=3, column=0, pady=15, padx=10)

def CloseProgram():
    root.destroy()
    driver.close()

def EggTurnerGUI():

    eggTurner = Toplevel(root)
    eggTurner.title("Ovipets Credit Farmer")
    width = 620
    window = width / 2
    CalculateDimensions(width, 600, eggTurner)
    root.withdraw()

    # Adding friends;
    descriptionLabel = Label(eggTurner, text="Add friends and Favorite them to turn their eggs, then press the Refresh Friends button!", font='Helvetica 9 bold', pady=15)
    descriptionLabel.pack()

    #Credits gotten;
    creditsGotten = Label(eggTurner, text="Total Credits Obtained: " + str(creditsFound))
    creditsGotten.pack()

    # Frames;
    # Toolbar
    toolbar = Frame(eggTurner, height=40)
    toolbar.pack(side="top", fill="x")
    toolbar.columnconfigure(0, weight=1)
    eggFrame = LabelFrame(toolbar, text="Add one friend to turn their eggs with (+)")
    eggFrame.grid(row=0, column=0, pady=10)

    # Secondary;
    #Textbox containers;
    main = PanedWindow(eggTurner)
    leftFrame = Frame(main, width=window / 2)
    rigthFrame = Frame(main, width=window / 2)
    main.add(leftFrame)
    main.add(rigthFrame)
    leftFrame.columnconfigure(0, weight=1)
    rigthFrame.columnconfigure(0, weight=1)

    #Bottom Panels
    bottomPanel = PanedWindow(main, width=window)
    main.add(bottomPanel)

    buttonsLeft = Frame(bottomPanel, width=window/2, height=30)
    buttonsRight = Frame(bottomPanel, width=window/2)
    bottomPanel.add(buttonsLeft)
    bottomPanel.add(buttonsRight)
    bottomPanel.pack(side="bottom", fill="both")
    main.pack(side="top", fill="both", expand=True)

    #Console
    consoleFrame = LabelFrame(rigthFrame, text="Console Output:")
    consoleFrame.grid(row=1, column=0, pady=0, padx=(0, 30))
    consoleScrollbar = Scrollbar(consoleFrame)
    consoleScrollbar.grid(row=0, column=1, pady=0, padx=0, ipady=65)
    console = Text(consoleFrame, width=38, height=13, yscrollcommand=consoleScrollbar.set, font='Helvetica 8')
    console.tag_config(b, foreground="blue", font=("Helvetica", "8", "bold")) #Comment
    console.tag_config(g, foreground="green", font=("Helvetica", "8", "bold")) #Success
    console.tag_config(r, foreground="red") #Warning
    console.tag_config(bl, foreground="black") #Normal;
    console.tag_config(c, foreground="black", background="yellow")  # Credit Obtained;
    consoleScrollbar.config(command=console.yview)
    console.grid(row=0, column=0, pady=20, padx=10)

    # Friends list frame
    friendsFrame = LabelFrame(leftFrame, text="Friend List:")
    friendsFrame.grid(row=0, column=0, pady=0, padx=40)
    hatcheriesScrollbar = Scrollbar(friendsFrame)
    hatcheriesScrollbar.grid(row=0, column=0, pady=0, ipady=65)
    hatcheries = Listbox(friendsFrame, width=30, height=12, yscrollcommand=hatcheriesScrollbar.set, font='Helvetica 8')
    hatcheries.grid(row=0, column=1, pady=20, padx=(0, 15))
    hatcheriesScrollbar.config(command=hatcheries.yview)
    LoadFriends(hatcheries, console)

    # Selecting friends;
    friendsButtons = LabelFrame(buttonsLeft, text="Friend List Commands:")
    friendsButtons.grid(row=1, column=0, pady=0, padx=40)
    buttonEraseFriend = Button(friendsButtons, text="X", command=lambda t="": DeleteFriends(hatcheries), state= DISABLED)
    buttonEraseFriend.grid(row=0, column=0, pady=20, padx=5)
    buttonRemoveQueueFriend = Button(friendsButtons, text="-", command=lambda t="":RemoveFromHatcheries(hatcheries))
    buttonRemoveQueueFriend.grid(row=0, column=1, pady=20, padx=(0, 5))
    buttonRandomizeFriend = Button(friendsButtons, text="Randomize", command=lambda t="": RandomizeFriends(hatcheries, console))
    buttonRandomizeFriend.grid(row=0, column=2, pady=20, padx=(0, 5))
    clearFriendList = Button(friendsButtons, text="Clear", command=lambda t="": EmptyFriendsList(hatcheries, console))
    clearFriendList.grid(row=0, column=3, pady=20, padx=(0, 5))
    clearFriendList = Button(friendsButtons, text="Load", command=lambda t="": LoadFriends(hatcheries, console))
    clearFriendList.grid(row=0, column=4, pady=20, padx=(0, 5))

    friendLabel = Label(eggFrame, text="Friend's Profile URL:")
    friendInput = Entry(eggFrame, width=40)
    friendAdd = Button(eggFrame, text="+", command=lambda t="":FriendAddUpdate(friendInput.get(), hatcheries, console))
    friendLabel.grid(row=0, column=0, pady=20, padx=20)
    friendInput.grid(row=0, column=1, pady=20, padx=20)
    friendAdd.grid(row=0, column=2, pady=20, padx=20)

    # Bot options
    botButtons = Frame(eggTurner, height=40)
    botButtons.pack(side=BOTTOM, fill=X)
    botButtons.columnconfigure(0, weight=1)
    frameButtons = LabelFrame(botButtons, text="Bot parameters")
    frameButtons.grid(row=0, column=0, pady=10)

    startBot = Button(frameButtons, text="Start Bot", command=lambda t="":BotStart(console, creditsGotten, 0))
    startBot.grid(row=0, column=1, padx=10, pady=10)
    stopBot = Button(frameButtons, text="Stop Bot", command=lambda t="":StopBot(console))
    stopBot.grid(row=0, column=2, padx=10, pady=10)
    refreshFriends = Button(frameButtons, text="Refresh Friends", command=lambda t="": RefreshFriends(console, hatcheries))
    refreshFriends.grid(row=0, column=3, padx=10, pady=10)
    optionsBot = Button(frameButtons, text="Bot Options", command=lambda t="": OptionsEggTurnerGUI(console))
    optionsBot.grid(row=0, column=4, padx=10, pady=10)

def OptionsEggTurnerGUI(console):
    optionsEgg = Toplevel(root)
    optionsEgg.title("Options Egg Turner")
    ysep = 10
    length = 240
    resolution = 0.01

    width = 620
    window = width / 2
    CalculateDimensions(width, 620, optionsEgg)

    # Descriptions;
    descriptionLabel = Label(optionsEgg,
                             text="Configure the auto egg turner's wait times using the sliders below!",
                             font='Helvetica 9 bold')
    descriptionLabel.grid(row=0, column=0, pady=(10, 5), padx=20)
    creditsGotten = Label(optionsEgg, text="Be sure not to put everything to the minimum as that may lead to a ban...")
    creditsGotten.grid(row=1, column=0, pady=(5, ysep), padx=20)

    #Comment Window
    frameButtons = LabelFrame(optionsEgg, text="Bot Options")
    frameButtons.grid(row=2, column=0, pady=0, padx=20)

    #Divided frame;
    main = PanedWindow(frameButtons)
    leftFrame = Frame(main, width=window / 2)#, bg="white")
    rigthFrame = Frame(main, width=window / 2)#, bg="black")
    main.add(leftFrame)
    main.add(rigthFrame)

    #Profiles;
    profMin = Scale(leftFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=0.5, to=3, length=length,
                    label="Profile wait time (Minimum):")
    profMin.grid(row=0, column=0, pady=ysep, padx=20)
    profMax = Scale(leftFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=4, to=10, length=length,
                    label="Profile wait time (Maximum):")
    profMax.grid(row=1, column=0, pady=ysep, padx=20)

    #Hatcheries
    hatcheMin = Scale(leftFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=2, to=4, length=length,
                    label="Hatchery wait time (Minimum):")
    hatcheMin.grid(row=2, column=0, pady=ysep, padx=20)
    hatcheMax = Scale(leftFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=5, to=10, length=length,
                    label="Hatchery wait time (Maximum):")
    hatcheMax.grid(row=3, column=0, pady=ysep, padx=20)

    # Search Eggs
    searchEggsMin = Scale(leftFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=0.5, to=2, length=length,
                     label="Go to turnable egg's page (Minimum):")
    searchEggsMin.grid(row=4, column=0, pady=ysep, padx=20)
    searchEggsMax = Scale(leftFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=3, to=10, length=length,
                     label="Go to turnable egg's page (Maximum):")
    searchEggsMax.grid(row=5, column=0, pady=ysep, padx=20)

    # Click Turn Egg;
    turnButtonMin = Scale(rigthFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=0.2, to=0.5, length=length,
                    label="Click 'Turn Egg' wait (Minimum):")
    turnButtonMin.grid(row=0, column=0, pady=ysep, padx=20)
    turnButtonMax = Scale(rigthFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=0.6, to=1, length=length,
                    label="Click 'Turn Egg' wait (Maximum):")
    turnButtonMax.grid(row=1, column=0, pady=ysep, padx=20)

    # Found a credit click
    creditOkMin = Scale(rigthFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=0.5, to=4, length=length,
                      label="Found a credit 'Ok' click (Minimum):")
    creditOkMin.grid(row=2, column=0, pady=ysep, padx=20)
    creditOkMax = Scale(rigthFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=5, to=10, length=length,
                      label="Found a credit 'Ok' click (Maximum):")
    creditOkMax.grid(row=3, column=0, pady=ysep, padx=20)

    # Next egg
    nextEggMin = Scale(rigthFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=0.2, to=0.5, length=length,
                          label="Next egg click wait (Minimum):")
    nextEggMin.grid(row=4, column=0, pady=ysep, padx=20)
    nextEggMax = Scale(rigthFrame, repeatdelay=5, resolution=resolution, orient=HORIZONTAL, from_=0.5, to=1, length=length,
                          label="Next egg click wait (Maximum):")
    nextEggMax.grid(row=5, column=0, pady=ysep, padx=20)

    main.pack(fill="both")

    sliders = [profMin, profMax, hatcheMin, hatcheMax, searchEggsMin,
                searchEggsMax, turnButtonMin, turnButtonMax, creditOkMin,
                creditOkMax, nextEggMin, nextEggMax]
    InjectToSliders(sliders, LoadOptions(optionsFile), 1)

    # Save options;
    saveOptions = Button(optionsEgg, text="Save Options", command=lambda t="": SaveOptions(ExtractFromSliders(sliders), turnSettings, optionsFile, optionsEgg))
    saveOptions.grid(row=4, column=0, pady=ysep, padx=30)

def ExtractFromSliders(sliders):
    data = []
    for slider in sliders:
        data.append(slider.get())
    return data

def InjectToSliders(sliders, data, startFrom):
    i = startFrom
    for slider in sliders:
        try:
            slider.set(data[i])
            i += 1
        except: break;

def EggHatcherGUI():
    eggTurner = Toplevel(root)
    eggTurner.title("Ovipets Auto Egg Hatcher")
    width = 400
    window = width / 2
    CalculateDimensions(width, 400, eggTurner)
    root.withdraw()

    # Adding friends;
    descriptionLabel = Label(eggTurner,
                             text="Hatch Eggs Automatically!",
                             font='Helvetica 9 bold', pady=15)
    descriptionLabel.pack()

    # Frames;
    # Secondary;
    # Textbox containers;
    main = PanedWindow(eggTurner)

    # Console
    consoleFrame = LabelFrame(eggTurner, text="Console Output:")
    consoleFrame.pack()
    consoleScrollbar = Scrollbar(consoleFrame)
    consoleScrollbar.grid(row=0, column=1, pady=0, padx=0, ipady=65)
    console = Text(consoleFrame, width=38, height=13, yscrollcommand=consoleScrollbar.set, font='Helvetica 8')
    console.tag_config(b, foreground="blue", font=("Helvetica", "8", "bold"))  # Comment
    console.tag_config(g, foreground="green", font=("Helvetica", "8", "bold"))  # Success
    console.tag_config(r, foreground="red")  # Warning
    console.tag_config(bl, foreground="black")  # Normal;
    console.tag_config(c, foreground="black", background="yellow")  # Credit Obtained;
    consoleScrollbar.config(command=console.yview)
    console.grid(row=0, column=0, pady=30, padx=10)

    # Bot options
    botButtons = Frame(eggTurner, height=40)
    botButtons.pack(side=BOTTOM, fill=X)
    botButtons.columnconfigure(0, weight=1)
    frameButtons = LabelFrame(botButtons, text="Bot parameters:")
    frameButtons.grid(row=0, column=0, pady=10)

    startBot = Button(frameButtons, text="Start Bot", command=lambda t="": BotStart(console, None, 1))
    startBot.grid(row=0, column=1, padx=10, pady=10)
    stopBot = Button(frameButtons, text="Stop Bot", command=lambda t="": StopBot(console))
    stopBot.grid(row=0, column=2, padx=10, pady=10)

def AutoFeederGUI():
    feeder = Toplevel(root)
    feeder.title("Ovipets Auto Feeder")
    width = 400
    window = width / 2
    CalculateDimensions(width, 400, feeder)
    root.withdraw()

    # Adding friends;
    descriptionLabel = Label(feeder,
                             text="Feed Pets Automatically!",
                             font='Helvetica 9 bold', pady=15)
    descriptionLabel.pack()

    # Frames;
    # Secondary;
    # Textbox containers;
    main = PanedWindow(feeder)

    # Console
    consoleFrame = LabelFrame(feeder, text="Console Output:")
    consoleFrame.pack()
    consoleScrollbar = Scrollbar(consoleFrame)
    consoleScrollbar.grid(row=0, column=1, pady=0, padx=0, ipady=65)
    console = Text(consoleFrame, width=38, height=13, yscrollcommand=consoleScrollbar.set, font='Helvetica 8')
    console.tag_config(b, foreground="blue", font=("Helvetica", "8", "bold"))  # Comment
    console.tag_config(g, foreground="green", font=("Helvetica", "8", "bold"))  # Success
    console.tag_config(r, foreground="red")  # Warning
    console.tag_config(bl, foreground="black")  # Normal;
    console.tag_config(c, foreground="black", background="yellow")  # Credit Obtained;
    consoleScrollbar.config(command=console.yview)
    console.grid(row=0, column=0, pady=30, padx=10)

    # Bot options
    botButtons = Frame(feeder, height=40)
    botButtons.pack(side=BOTTOM, fill=X)
    botButtons.columnconfigure(0, weight=1)
    frameButtons = LabelFrame(botButtons, text="Bot parameters:")
    frameButtons.grid(row=0, column=0, pady=10)

    startBot = Button(frameButtons, text="Start Bot", command=lambda t="": FeederStart(console))
    startBot.grid(row=0, column=1, padx=10, pady=10)
    stopBot = Button(frameButtons, text="Stop Bot", command=lambda t="": StopBot(console))
    stopBot.grid(row=0, column=2, padx=10, pady=10)
    optionsBot = Button(frameButtons, text="Bot Options", command=lambda t="": OptionsEggTurnerGUI(console))
    optionsBot.grid(row=0, column=4, padx=10, pady=10)


#Init GUI
root = Tk()

#Screens;
CalculateDimensions(450, 300, root)
if(login == bool(1)):
    MainMenuGUI(username)
else: LoginScreen()

#Update the program;
root.mainloop()