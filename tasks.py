#Selenium bot to sign up for gym slots
#tasks.py holds the methods which are called in the menu in main.py

#imports
from selenium import webdriver  #lets me open up the web browser
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from prettytable import PrettyTable

#to get the day of the week
from datetime import datetime


# <editor-fold desc="Log-in Info">
#hidden log-in info (change to user entered input if posting on github)
username = ""  #changed
password = ""
#cold folding
# </editor-fold>
# #for other users inputting their own log in info
username = input("Enter USC username: ")
password = input("Enter USC password: ")

#url for gym booking website
url = "https://myrecsports.usc.edu/"

#before the program officially starts
print("Loading...")
print("Enjoy some random cat pictures while you wait for information to be gathered :)")

# for gathering all the info at the start (change to headless browser)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('headless')  #should make it headless
options.add_argument('window-size=1200x600')
s = Service('C:/webdrivers/chromedriver.exe')
invisBrowser = webdriver.Chrome(service=s, options=options)
invisBrowser.get(url)
invisBrowser.implicitly_wait(10)  # put once at the beginning and holds for all operations

#function to display the menu and get user input
def getMenuInput(validReminder):
    if validReminder:
        print("\nPlease make a valid selection:")
    else:
        print("\nPlease make a selection:")
    print("\ta) Show availability for all time slots")
    print("\tb) Show availability of time slots for a specific gym")
    print("\tc) Show availability of time slots on a specific day")
    print("\td) Check how many slots are available for a certain time slot")
    print("\te) Sign up for a specific time slot")
    print("\tf) Quit")
    menuChoice = input("> ")
    menuChoice = menuChoice.lower().strip()  # so they can choose upper or lower case and add a space or some
    return menuChoice

# function to get user input (gym, day, time) + error checking it
def getAllInputs(infoList, gymStop, dayStop):
    userInput = [] #creating empty list to hold multiple return values
    if not dayStop:
        userInput.append(getGymInput(infoList))
        gymIndex = {"Village": 0, "Lyon": 1}   #also creating a map from the gym string to an index (for the info list)
        userInput.append(gymIndex[userInput[0]])
    if gymStop:
        return userInput[1]
    weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]  # list for finding dotw
    dayToday = datetime.today().weekday()  # returns a # corresponding to the day of the week
    day = getDayInput(infoList, weekDays, dayToday)
    userInput.append(day)  #have to split the lines up bc the index may not be consistent cause of if stmnts
    userInput.append(weekDays[(dayToday+int(day)-1)%7])
    if dayStop:
        return userInput
    userInput.append(getTimeInput(infoList, userInput, gymIndex, weekDays, dayToday))
    return userInput

def getGymInput(infoList):
    gymLoc = input("Which gym would you like to make an appt for (Village/Lyon)? ")
    gymLoc = gymLoc.capitalize()  #so it's not case sensitive
    # error checking input
    while gymLoc != "Village" and gymLoc != "Lyon":
        gymLoc = input("Please choose either Village or Lyon: ")
        gymLoc = gymLoc.capitalize()
    return gymLoc

def getDayInput(infoList, weekDays, dayToday):
    day1 = weekDays[dayToday]
    day2 = weekDays[(dayToday + 1) % 7]
    day3 = weekDays[(dayToday + 2) % 7]
    print("What day would you like to sign up for?")
    print("\t1) " + day1)
    print("\t2) " + day2)
    print("\t3) " + day3)
    day = input("> ")
    # error-checking for a valid # (1, 2, or 3)
    while day != "1" and day != "2" and day != "3":
        day = input("Please make a valid selection (1, 2, or 3): ")
    return day

def getTimeInput(infoList, userInput, gymIndex, weekDays, dayToday):
    dayList = infoList[gymIndex[userInput[0]]][int(userInput[2])-1]  #navigating to the right day list based on user input
    if len(dayList) == 0:
        print("Sorry, there are no available time slots for " + weekDays[(dayToday+int(userInput[2])-1)%7] + " :(")
        return 0  #return an empty list

    print("What time slot would you like to sign up for?")  # give menu options here too
    #iterate through the day list
    count = 0
    for list in dayList:
        print("\t" + str(count+1) + ")", list[1])  #CHANGE THIS TO REFLECT NEW LIST ORDERING
        count += 1

    time = input("> ")
    while int(time) > count or int(time) < 1:
        time = input("Please choose a valid time slot: ")
    return time

def setup(catBrowser):
    catBrowser.get('https://cataas.com/cat')  #random cat website
    catBrowser.maximize_window()
    backgroundInstantiator(catBrowser)
    return getGymInfo(catBrowser)

#opens a headless (invisible) chrome browser and goes to the village booking page
def backgroundInstantiator(catBrowser):
    #navigate to the village info first (same way as in makeAppt)
    invisBrowser.find_element(By.CLASS_NAME, 'img-responsive').click()  # reservations
    invisBrowser.find_element(By.CLASS_NAME, 'inherit-link').click()  # track for logging in
    catBrowser.refresh()   #new cat!
    invisBrowser.find_element(By.XPATH,'//*[@id="divLoginOptions"]/div[2]/div[2]/div/button').click()  # click login button
    invisBrowser.find_element(By.ID, 'username').send_keys(username)
    invisBrowser.find_element(By.ID, 'password').send_keys(password)
    catBrowser.refresh()
    invisBrowser.find_element(By.NAME, '_eventId_proceed').click()  # login
    #Using a try block to handle the 2FA pop up that may occur
    try:
        invisBrowser.find_element(By.XPATH, '//*[@id="page-wrapper"]/div/div[1]/div/div[3]/p/a').click()
    except:
        pass #if it's not there just move on
    invisBrowser.get_screenshot_as_file("preVillage.png")
    invisBrowser.find_element(By.PARTIAL_LINK_TEXT, "Village").click()  # village first

#function that gets all the reservation booking elements, parses the info and puts it in lists
def getGymInfo(catBrowser):
    catBrowser.refresh()
    #starting at village page gather info
    bookingList = []   #starting with the big, main empty list
    villageList = [] #and then we have an empty village list
    lyonList = []

    #Start with monday, get list of all booking elements
    addDayList(villageList)
    #Now navigate to 2nd day and repeat
    invisBrowser.find_element(By.XPATH, '//*[@id="divBookingDateSelector"]/div[2]/div[2]/button[2]').click()
    addDayList(villageList)
    #And same for the 3rd day
    invisBrowser.find_element(By.XPATH, '//*[@id="divBookingDateSelector"]/div[2]/div[2]/button[3]').click()
    addDayList(villageList)

    #So now the village list should have 3 lists of info for each of the 3 days
    bookingList.append(villageList)
    catBrowser.refresh()

    #and must do the same for lyon center (navigate there first)
    invisBrowser.find_element(By.CLASS_NAME, 'hamburger').click()
    invisBrowser.find_element(By.CLASS_NAME, 'sidebarlinktext').click()
    invisBrowser.find_element(By.PARTIAL_LINK_TEXT, 'Lyon').click()

    #and now collect info like above
    addDayList(lyonList)
    #day 2
    invisBrowser.find_element(By.XPATH, '//*[@id="divBookingDateSelector"]/div[2]/div[2]/button[2]').click()
    addDayList(lyonList)
    #day 3
    invisBrowser.find_element(By.XPATH, '//*[@id="divBookingDateSelector"]/div[2]/div[2]/button[3]').click()
    addDayList(lyonList)

    bookingList.append(lyonList)
    catBrowser.refresh()
    invisBrowser.quit()

    return bookingList

def addDayList(gymList):
    parentEl = invisBrowser.find_element(By.ID, 'divBookingSlots')
    emptyCheck = parentEl.find_elements(By.CSS_SELECTOR, '*')
    if len(emptyCheck) == 1:
        gymList.append([])  # appending empty list if no booking elements
    else:
        elList = parentEl.find_elements(By.CLASS_NAME, 'booking-slot-item')  # list of all the booking elements
        # loop through all the elements and put info in lists
        dayList = []
        for el in elList:
            # store the full text in a string ->convert to list ->append the list
            avaTimeSlotList = el.text.split('\n')
            if len(avaTimeSlotList) == 4:
                avaTimeSlotList.pop(1)  # edge case where you've already booked one of the slots
            dayList.append(avaTimeSlotList)  # has the availability, time, and # of slots
        gymList.append(dayList)

def printDayTable(infoList, dayInput):
    print("\n               The Village Gym:", dayInput[1])  #using spaces since \t is not consistent with cmd line output
    printTable(infoList, 0, int(dayInput[0])-1)
    print("\n               Lyon Center Gym:", dayInput[1])
    printTable(infoList, 1, int(dayInput[0])-1)

def printGymTable(infoList, gymIndex):
    if gymIndex:
        print("\nLyon Center Gym:", end="")  #don't want a new line at the end for consistent formating
    else:
        print("\nThe Village Gym:", end="")
    #Now print the 3 days with the 3 tables
    weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dayToday = datetime.today().weekday()
    for i in range(3):
        print("\n                       " + weekDays[(dayToday+i)%7])
        printTable(infoList, gymIndex, i)

def printAllTable(infoList):
    #Loop through both gyms and call printGymTable on both
    for gymIndex in range(2):
        printGymTable(infoList, gymIndex)

def printTable(infoList, gymIndex, dayIndex):
    table = PrettyTable(
        field_names = ["Time Slot", "Number of Slots", "Availability"]
    )
    #Now need to loop through the slots for that particular day and report the text and availability
    dayList = infoList[gymIndex][dayIndex]
    if len(dayList) == 0:
        table.add_row(["No Available Times", "-", "-"])
    else:
        for list in dayList:
            table.add_row([list[1], list[2], list[0].strip()])
    print(table)

#function to open a visible broswer and run bot on given user cmnds (takes in a list containing user inputs and the driver)
def makeAppt(userInput, browser):
    browser.get(url)
    browser.maximize_window()  #fullscreen is better

    #logging in and going to the login page
    browser.implicitly_wait(10)   #put once at the beginning and holds for all operations
    browser.find_element(By.CLASS_NAME, 'img-responsive').click()  #reservations
    browser.find_element(By.CLASS_NAME, 'inherit-link').click()    #track for logging in
    browser.find_element(By.XPATH, '//*[@id="divLoginOptions"]/div[2]/div[2]/div/button').click() #find the login button

    #using keys to login
    browser.find_element(By.ID, 'username').send_keys(username)
    browser.find_element(By.ID, 'password').send_keys(password)
    browser.find_element(By.NAME, '_eventId_proceed').click()  #login

    # Using a try block to handle the 2FA pop up that may occur
    try:
        browser.find_element(By.XPATH, '//*[@id="page-wrapper"]/div/div[1]/div/div[3]/p/a').click()
    except:
        pass  # if it's not there just move on
    browser.find_element(By.PARTIAL_LINK_TEXT, userInput[0]).click() # goes to whichever gym the user enters

    #choose day
    browser.find_element(By.XPATH, '//*[@id="divBookingDateSelector"]/div[2]/div[2]/button['+userInput[2]+']').click()
    #choose time slot
    timeSlot = browser.find_element(By.CSS_SELECTOR, 'div[data-slot-number="'+userInput[4]+'"]')
    avaText = timeSlot.find_element(By.CSS_SELECTOR, "div[class='booking-slot-item'] > span").text
    timeText = timeSlot.find_element(By.CSS_SELECTOR, "div[class='booking-slot-item'] > p > strong").text
    if avaText == "No spots available":
        print("Sorry, there are no available time slots for " + timeText + " :(")
    elif "Book Now" in timeSlot.text:
        browser.find_element(By.XPATH, '//*[@id="divBookingSlots"]/div/div['+userInput[4]+']/div/button').click() #make the reservation
    elif "Unavailable" in timeSlot.text:
        print("The", timeText, "time slot is not available because you have already signed up for another slot that day")
    elif "Booked" in timeSlot.text:
        print("You have already booked this time slot!")
    else:
        print("The", timeText, "time slot is not available yet")
        openText = timeSlot.find_element(By.CSS_SELECTOR, "div[class='booking-slot-item'] > div > span").text
        openText = "o" + openText[1:]  #makes the message lowercase
        print("The time slot", openText)