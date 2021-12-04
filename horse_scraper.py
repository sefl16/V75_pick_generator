from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager            #Automatically use the right version for the driver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC #test
from selenium.webdriver.support.ui import WebDriverWait #test



from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import csv
from datetime import datetime, timedelta, date
import pendulum                                                      #For getting saturdays
import os

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-extensions')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--disable-setuid-sandbox")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("disable-infobars")
options.add_argument("--remote-debugging-port=9231")
driver = webdriver.Chrome(options=options, executable_path="/usr/local/bin/chromedriver")
#driver = webdriver.Chrome(ChromeDriverManager().install())

#-------------------------------------------------------------------------------------------------------------------------


def get_horses():

    #print(pendulum.now().current() .strftime('20%y-%m-%d'))
    #saturday = pendulum.now().next(pendulum.SATURDAY).strftime('20%y-%m-%d')
    #saturday = "2021-04-10"
    if date.today().weekday() != 5:
        saturday = pendulum.now().next(pendulum.SATURDAY).strftime('20%y-%m-%d')
        # print(saturday + " 1st loop")
    else:
        saturday = date.today().strftime('20%y-%m-%d')

        # print(saturday + " 2nd loop")

    uri = "https://www.atg.se/spel/" + saturday + "/V75/"                           #Source to ATG race                    
    print("Getting horses from: " + uri)
    file_name = "../horse_csv/v75_" + saturday + '.csv'
    race_list = []
    counter = 0
    race_nr = 1
    bool = False

    positionL = []
    horseL = []
    kuskL = []
    oddsL = []
    earning_per_startL = []
    raceL = []

    horse_tables = []                                                            #List used for getting all the tables with different races


    ###For some reason the scraper fails to load the correct content of the URI so have to redo the process until it can find the horse tables###
    while bool == False:
        if not horse_tables:
            driver.get(uri)

            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')                        #For getting source info from website
            horse_tables = soup.find_all('table', class_= "game-table")
        else:
            bool = True

    id="onetrust-accept-btn-handler"
    #driver.execute_script("arguments[0].click();", WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Godkänn alla cookies']"))))
    #driver.execute_script("arguments[0].click();", WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='campaign-close-button']")))) #För att stänga äckliga kampanjen
    #button = driver.find_element(By.XPATH, '//button[text()="Anpassa"]')        #Dynamically interact with website to get more stats on horses
    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Anpassa']"))).click()
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Anpassa']")))) #Needed for finding button
    # print(button)
    #sleep(5)
    #button.click()
    sleep(5)
    checkbox = driver.find_element(By.XPATH, '//input[@data-test-id="checkbox-earningsPerStart"]')
    if(checkbox.is_selected() == False):
        driver.execute_script("arguments[0].click();", checkbox)
    #driver.find_element(By.XPATH, '//button[text()="Spara"]').click()
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Spara']"))))

    content = driver.page_source                                        #Have to re-do the process because have been interacting with site buttons
    soup = BeautifulSoup(content, 'html.parser')                        #For getting source info from website
    #print(soup)
    horse_tables = soup.find_all('table', class_= "game-table")



    #---------------For getting all horses, positions, kusks and odds----------------#
    for horse_table in horse_tables:
        position = 1
        horses = horse_table.find_all('tr', attrs={'class':'startlist__row css-1n0u8es'})
        for horse in horses:
            horse_name = horse.find('td', attrs={'class':'horse-col'})
            horse_name = horse_name.find('span', attrs={'class':'horse-box'})
            horse_name = horse_name.find('div', attrs={'class':'name-container'})
            horse_name = horse_name.find('span', attrs={'class':'horse-name css-1h5vlcx-horseview-styles--horseName'}).get_text()       #To get the horse names

            kusk =  horse.find('td', attrs={'class':'driver-col'}).get_text()                       #Get kusk name
            bet = horse.find('td', attrs={'class':'betDistribution-col'}).get_text()                #Get the current odds
            bet = bet.replace('%', '')                                                              #Remove % from string
            earning_per_start = horse.find('td', attrs={'class':'earningsPerStart-col'}).get_text()
            earning_per_start = earning_per_start.replace(' ', '')

            this_dic = {
            "Position": str(position),
            "Horse": horse_name,
            "Kusk": kusk,
            "Odds": bet,
            "Race": "V75-" + str(race_nr)
            }                                                                   #Not really needed but maybe change to dictionary of lists instead of many lists, looks beeter?
            #race_list.append(this_dic)

            positionL.append(str(position))
            horseL.append(horse_name)
            kuskL.append(kusk)
            oddsL.append(bet)
            earning_per_startL.append(earning_per_start)
            raceL.append("V75-" + str(race_nr))
            position = position + 1
            #print(horseL)
            counter = counter + 1


        race_nr = race_nr + 1

    location = ""
    tempDistanceL = []
    distanceL = []
    tempTypeOfTrack = []
    typeOfTrackL = []
    track_info = soup.find_all('div', class_= "race-combined-info")
    for track in track_info:
        location = track.find('div', attrs={'class':'slanted race-track-name'})
        location = location.find('span', attrs={'class':'track-name text-wrapper'}).get_text()
        track_distance = track.find('div', attrs={'class':'slanted race-distance-start-method'})
        track_distance = track_distance.find('span', attrs={'class':'text-wrapper'}).get_text()

        if '1640m' in track_distance:                                           #Seperate distance and track type from the string
            tempDistanceL.append('1640m')
        elif '2100m' in track_distance:
            tempDistanceL.append('2100m')
        elif '2140m' in track_distance:
            tempDistanceL.append('2140m')
        elif '2640m' in track_distance:
            tempDistanceL.append('2640m')
        elif '3140m' in track_distance:
            tempDistanceL.append('3140m')
        else:
            tempDistanceL.append('Unknown')
        if 'autostart' in track_distance:
            tempTypeOfTrack.append('autostart')
        elif 'voltstart' in track_distance:
            tempTypeOfTrack.append('voltstart')





    for race in raceL:                                                          #Super ulgy solution to get the list same len(required for .csv) and with right values
        if race == "V75-1":
            distanceL.append(tempDistanceL[0])
            typeOfTrackL.append(tempTypeOfTrack[0])
        elif race == "V75-2":
            distanceL.append(tempDistanceL[1])
            typeOfTrackL.append(tempTypeOfTrack[1])
        elif race == "V75-3":
            distanceL.append(tempDistanceL[2])
            typeOfTrackL.append(tempTypeOfTrack[2])
        elif race == "V75-4":
            distanceL.append(tempDistanceL[3])
            typeOfTrackL.append(tempTypeOfTrack[3])
        elif race == "V75-5":
            distanceL.append(tempDistanceL[4])
            typeOfTrackL.append(tempTypeOfTrack[4])
        elif race == "V75-6":
            distanceL.append(tempDistanceL[5])
            typeOfTrackL.append(tempTypeOfTrack[5])
        elif race == "V75-7":
            distanceL.append(tempDistanceL[6])
            typeOfTrackL.append(tempTypeOfTrack[6])






    if os.path.exists(file_name):   #Remove the file if it already exists.
        os.remove(file_name)
    df = pd.DataFrame({'Position':positionL,'Horse':horseL,'Kusk':kuskL,'Odds%':oddsL,'Earning per start':earning_per_startL,'Race':raceL, 'Type of track':typeOfTrackL, 'Distance':distanceL, 'Location':location})    # 'Type of track':distanceL,
    df.to_csv(file_name, index=False, encoding='utf-8')                                #Savve the values to a .csv



    os.system("/home/seuz/Projects/Trav_tips/killChromeDriver.sh")                  #Temp solution to kill the chrome process since close does not work!?
    #print(result)
    # driver.stop_client()
    # driver.close()
    # driver.quit()

    return file_name            #Return filename of the CSV so it can be used in other functions
