#main.py holds the main function with the menu

#imports
import tasks
from selenium import webdriver  #lets me open up the web browser
from selenium.webdriver.chrome.service import Service

#main function that contains the menu and while loop
def main():
    #opening up cat website
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    s = Service('C:/webdrivers/chromedriver.exe')
    catBrowser = webdriver.Chrome(service=s, options=options)
    infoList = tasks.setup(catBrowser)  # gathers all the info and returns it in infoList
    catBrowser.quit()
    print("\nWelcome to the USC gym scheduling helper!")

    validReminder = False   #only true when the user needs to be reminded to input a valid selection
    browserOpen = False #so i can properly close the browser
    menuChoice = tasks.getMenuInput(validReminder)

    while menuChoice != "f":   #don't enter the loop if they choose to quit
        #branching and calling tasks.methods depending on what they choose
        if menuChoice == "a":
            #print all the info for all 3 days of both gyms
            tasks.printAllTable(infoList)
        elif menuChoice == "b":
            #print all the info of all 3 days of a certain gym
            gymIndex = tasks.getAllInputs(infoList, gymStop=True, dayStop=False) #contains the gym name and index
            tasks.printGymTable(infoList, gymIndex)
        elif menuChoice == "c":
            #print all the info of a certain day of a certain gym
            dayInput = tasks.getAllInputs(infoList, gymStop=False, dayStop=True)  #contains the day index and name
            tasks.printDayTable(infoList, dayInput)
        elif menuChoice == "d":
            #display the num of slots available for a certain time slot
            userInput = tasks.getAllInputs(infoList, gymStop=False, dayStop=False)
            if userInput[4] != 0:
                slotList = infoList[userInput[1]][int(userInput[2])-1][int(userInput[4])-1]
                if "Book Now" in slotList[0]:
                    print("This time slot is available to book!")
                elif "Opens" in slotList[0]:
                    print("This time slot is currently not available")
                    bOpen = slotList[0][:1].lower() + slotList[0][1:] # making first letter lower case
                    print("Booking", bOpen)
                elif "Booked" in slotList[0]:
                    print("You have already booked this time slot!")
                elif slotList[2] == "No spots available":
                    print("This time slot is filled up :(")
                else:
                    print("You cannot sign up for this slot because you're signed up for another the same day")
                print("There are " + slotList[2][:1].lower() + slotList[2][1:])

        elif menuChoice == "e":
            #sign up for a specific time slot (if possible)
            userInput = tasks.getAllInputs(infoList, gymStop=False, dayStop=False)
            if userInput[4] != 0:
                options = webdriver.ChromeOptions()
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                s = Service('C:/webdrivers/chromedriver.exe')
                browser = webdriver.Chrome(service=s, options=options)  #doing it here cause I don't want it to close with then end of the func call
                tasks.makeAppt(userInput, browser)
                browserOpen = True
        else:
            print("That selection is not valid")
            validReminder = True
        menuChoice = tasks.getMenuInput(validReminder)
        if browserOpen:
            browser.quit()
        validReminder = False  #reset it back to false
        browserOpen = False

#running the main function
main()