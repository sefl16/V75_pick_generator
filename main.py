import horse_scraper
import brain
import argparse

parser = argparse.ArgumentParser()
parser.parse_args()





file_name = horse_scraper.get_horses()
my_horses = brain.random_pick_generator(3, 400)
horse_pick_order = brain.rate_my_horse(file_name, my_horses)


print("The winning picks for the race are: \n")
for horse_picks in horse_pick_order:
    pos = horse_picks['Position']
    horse = horse_picks['Horse']
    kusk = horse_picks['Kusk']
    odds = horse_picks['Odds%']
    race = horse_picks['Race']
    #print("Pos: " + pos + "\tHäst: " + horse + "\t\tKusk: " + kusk + "\t\tOdds: " + odds + "%" + "\t\tRace: " + race + "\n")
    print("Race: " + race + "\t\tPos: " + pos + "\t\tHäst: " + horse + "\t\tKusk: " + kusk + "\t\tOdds: " + odds + "%")


print (my_horses)
