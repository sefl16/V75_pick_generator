import horse_scraper
import brain
import argparse
import sys


example_text = '''Example of use: python3 main.py -S 3 -M 400'''

#------------------------HANDLING ALL INPUT OF ARGUMENTS-------------------------
parser = argparse.ArgumentParser(description="Pick generator for V75\nmain –S <The number of Spikar> -M <The ammount of money>",
                                 epilog=example_text,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("-S", "--nr_of_spikar", type=int, help="Specify the number of spikar that the system will use")
parser.add_argument("-M", "--ammount_of_money", type=int, help="Specify the ammount of money the system will pick horses to bet on")

if len(sys.argv) < 2:
    print("For help use -h flag")
    sys.exit(1)

args = parser.parse_args()

#----------------------------WHEN HELP IS TRIGGERED, THE CHROMEDRIVER AINT KILLED, NEED TO BE FIXED-----------

file_name = horse_scraper.get_horses()
my_horses = brain.random_pick_generator(args.nr_of_spikar, args.ammount_of_money)
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
