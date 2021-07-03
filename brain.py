from random import seed
from random import randint
from random import shuffle
import csv
import operator


def random_pick_generator(nr_of_spikar, stakes):
    min_range = stakes *0.97
    max_range = stakes *1.25
    row_price = 0.5
    if nr_of_spikar == 2:
        temp = 0.5
        bool = False
        nr_of_picks_list = []

        while bool == False:
            if min_range <= temp <= max_range:              #Find accepted stake
                print("value accepted: " + str(temp))
                bool = True
            else:
                temp = 0.5
                nr_of_picks_list.clear()
                for i in range(5):                          #Random number of horses for other races
                    value = randint(2,8)
                    temp = temp * value
                    nr_of_picks_list.append(value)
        nr_of_picks_list.append(1)                         #Spikar
        nr_of_picks_list.append(1)                         #Spikar

        shuffle(nr_of_picks_list)                           #Randomize where all picks goes for each race
        #print(nr_of_picks_list)

        return nr_of_picks_list

    if nr_of_spikar == 3:
        temp = 0.5
        bool = False
        nr_of_picks_list = []

        while bool == False:
            if min_range <= temp <= max_range:
                print("value accepted: " + str(temp))
                bool = True
            else:
                temp = 0.5
                nr_of_picks_list.clear()
                for i in range(4):                          #Random number of horses for other races
                    value = randint(2,8)
                    temp = temp * value
                    nr_of_picks_list.append(value)
        nr_of_picks_list.append(1)                         #Spikar
        nr_of_picks_list.append(1)                         #Spikar
        nr_of_picks_list.append(1)                         #Spikar

        shuffle(nr_of_picks_list)                           #Randomize where all picks goes for each race
        #print(nr_of_picks_list)

        return nr_of_picks_list


def rate_my_horse(file_name, horse_pick_list):


    median_earning = []
    count_horses = []


    v75_list = []
    v75_list_1 = []
    v75_list_2 = []
    v75_list_3 = []
    v75_list_4 = []
    v75_list_5 = []
    v75_list_6 = []
    v75_list_7 = []
    sort_horse_picks = []

    input_file = csv.DictReader(open(file_name))

    for row in input_file:                                      #Get a list(1) of dictionaries(2) for each race(1) and horse(2)
        row["Pick rating"] = 0                                  #The rating for which the horse is likely to win/picked
        if row.get("Race") == "V75-1":
            v75_list_1.append(row)
        if row.get("Race") == "V75-2":
            v75_list_2.append(row)
        if row.get("Race") == "V75-3":
            v75_list_3.append(row)
        if row.get("Race") == "V75-4":
            v75_list_4.append(row)
        if row.get("Race") == "V75-5":
            v75_list_5.append(row)
        if row.get("Race") == "V75-6":
            v75_list_6.append(row)
        if row.get("Race") == "V75-7":
            v75_list_7.append(row)

    v75_list.append(v75_list_1)                             #Get right structure: List(v75_all_races) of Lists(for each race) of dictionaries(for each horse)
    v75_list.append(v75_list_2)
    v75_list.append(v75_list_3)
    v75_list.append(v75_list_4)
    v75_list.append(v75_list_5)
    v75_list.append(v75_list_6)
    v75_list.append(v75_list_7)

    #Logic for picking the horses ("The brain" o.O)

    temp_median_earning = 0
    temp_count_horses = 0
    for race in v75_list:           #Loop to + all earnings from horses to calculate mean
        temp_median_earning = 0
        temp_count_horses = 0
        for horse in race:
            temp_median_earning = temp_median_earning + int(horse["Earning per start"])
            temp_count_horses = temp_count_horses + 1
        median_earning.append(temp_median_earning)
        count_horses.append(temp_count_horses)

    temp = 0
    for earning in median_earning:              #Calculate the mean
        # if earning == 0:
        #     continue
        earning = earning / count_horses[temp]
        median_earning[temp] = earning
        temp = temp + 1


    for race in v75_list:
        for horse in race:
            rating = 0

            #Rating based on earngins
            if horse["Race"] == "V75-1" and int(horse["Earning per start"]) >= (median_earning[0] * 1.2):
                rating = rating + 2
            if horse["Race"] == "V75-1" and int(horse["Earning per start"]) <= (median_earning[0] * 1.2) and int(horse["Earning per start"]) >= median_earning[0]:
                rating = rating + 1
            if horse["Race"] == "V75-2" and int(horse["Earning per start"]) >= (median_earning[1] * 1.2):
                rating = rating + 2
            if horse["Race"] == "V75-2" and int(horse["Earning per start"]) <= (median_earning[1] * 1.2) and int(horse["Earning per start"]) >= median_earning[1]:
                rating = rating + 1
            if horse["Race"] == "V75-3" and int(horse["Earning per start"]) >= (median_earning[2] * 1.2):
                rating = rating + 2
            if horse["Race"] == "V75-3" and int(horse["Earning per start"]) <= (median_earning[2] * 1.2) and int(horse["Earning per start"]) >= median_earning[2]:
                rating = rating + 1
            if horse["Race"] == "V75-4" and int(horse["Earning per start"]) >= (median_earning[3] * 1.2):
                rating = rating + 2
            if horse["Race"] == "V75-4" and int(horse["Earning per start"]) <= (median_earning[3] * 1.2) and int(horse["Earning per start"]) >= median_earning[3]:
                rating = rating + 1
            if horse["Race"] == "V75-5" and int(horse["Earning per start"]) >= (median_earning[4] * 1.2):
                rating = rating + 2
            if horse["Race"] == "V75-5" and int(horse["Earning per start"]) <= (median_earning[4] * 1.2) and int(horse["Earning per start"]) >= median_earning[4]:
                rating = rating + 1
            if horse["Race"] == "V75-6" and int(horse["Earning per start"]) >= (median_earning[5] * 1.2):
                rating = rating + 2
            if horse["Race"] == "V75-6" and int(horse["Earning per start"]) <= (median_earning[5] * 1.2) and int(horse["Earning per start"]) >= median_earning[5]:
                rating = rating + 1
            if horse["Race"] == "V75-7" and int(horse["Earning per start"]) >= (median_earning[6] * 1.2):
                rating = rating + 2
            if horse["Race"] == "V75-7" and int(horse["Earning per start"]) <= (median_earning[6] * 1.2) and int(horse["Earning per start"]) >= median_earning[6]:
                rating = rating + 1


            #Statistics based on placement for each distance between two year: 2019-2020
            if horse["Type of track"] == 'autostart':
                if horse["Distance"] == '1640m' or horse["Distance"] == '1609m':
                    if horse["Position"] == '4' or horse["Position"] == '5':
                        rating = rating + 2
                    if horse["Position"] == '1' or horse["Position"] == '2' or horse["Position"] == '3':
                        rating = rating + 1
                    if horse["Position"] == '6':
                        rating = rating + 0.7
                    if horse["Position"] == '12':
                        rating = rating - 1
                if horse["Distance"] == '2140m' or horse["Distance"] == '2100m':
                    if horse["Position"] == '4' or horse["Position"] == '5':
                        rating = rating + 2
                    if horse["Position"] == '1' or horse["Position"] == '2' or horse["Position"] == '3' or horse["Position"] == '6':
                        rating = rating + 1
                    if horse["Position"] == '12':
                        rating = rating - 0.5
                if horse["Distance"] == '2640m' or horse["Distance"] == '2609m':
                    if horse["Position"] == '4' or horse["Position"] == '5':
                        rating = rating + 2
                    if horse["Position"] == '2' or horse["Position"] == '3' or horse["Position"] == '6':
                        rating = rating + 1
                    if horse["Position"] == '1':
                        rating = rating + 0.7
                    if horse["Position"] == '7' or horse["Position"] == '8' or horse["Position"] == '9':
                        rating = rating + 0.3
                    if horse["Position"] == '12':
                        rating = rating - 0.5
                if horse["Distance"] == '3140m':
                    if horse["Position"] == '1' or horse["Position"] == '2' or horse["Position"] == '3' or horse["Position"] == '4' or horse["Position"] == '5' or horse["Position"] == '6':   #Less statistics on
                        rating = rating + 1
                    if horse["Position"] == '7' or horse["Position"] == '8' or horse["Position"] == '9':
                        rating = rating + 0.3

            if horse["Type of track"] == 'voltstart':
                if horse["Distance"] == '1640m' or horse["Distance"] == '1609m':
                    if horse["Position"] == '1':
                        rating = rating + 2
                    if horse["Position"] == '2' or horse["Position"] == '3':
                        rating = rating + 1
                    if horse["Position"] == '6' or horse["Position"] == '7':
                        rating = rating + 0.7
                    if horse["Position"] == '12' or horse["Position"] == '13' or horse["Position"] == '14' or horse["Position"] == '15':
                        rating = rating - 1
                if horse["Distance"] == '2140m' or horse["Distance"] == '2640m':        #Same for both distances
                    if horse["Position"] == '1':
                        rating = rating + 2
                    if horse["Position"] == '2' or horse["Position"] == '3':
                        rating = rating + 1
                    if horse["Position"] == '6':
                        rating = rating + 0.8
                    if horse["Position"] == '7':
                        rating = rating + 0.7
                    if horse["Position"] == '4' or horse["Position"] == '5':
                        rating = rating + 0.5
                    if horse["Position"] == '12' or horse["Position"] == '13' or horse["Position"] == '14' or horse["Position"] == '15':
                        rating = rating - 0.7
                if horse["Distance"] == '3140m':
                    if horse["Position"] == '1':
                        rating = rating + 2
                    if horse["Position"] == '2' or horse["Position"] == '3':
                        rating = rating + 1
                    if horse["Position"] == '6':
                        rating = rating + 0.7
                    if horse["Position"] == '4':
                        rating = rating + 0.5
                    if horse["Position"] == '5':
                        rating = rating + 0.3
                    if horse["Position"] == '7' or horse["Position"] == '8' or horse["Position"] == '9':
                        rating = rating + 0.2
                    if horse["Position"] == '12' or horse["Position"] == '13' or horse["Position"] == '14' or horse["Position"] == '15':
                        rating = rating - 0.3

            #Rating based on the current odds
            if int(horse["Odds%"]) >= 50:
                rating = rating + 5
            if int(horse["Odds%"]) >= 35 and int(horse["Odds%"]) < 50:
                rating = rating + 4
            if int(horse["Odds%"]) >= 25 and int(horse["Odds%"]) < 35:
                rating = rating + 3
            if int(horse["Odds%"]) >= 15 and int(horse["Odds%"]) < 25:
                rating = rating + 2
            if int(horse["Odds%"]) >= 9 and int(horse["Odds%"]) < 15:
                rating = rating + 1.5
            if int(horse["Odds%"]) >= 5 and int(horse["Odds%"]) < 9:
                rating = rating + 0.5
            if int(horse["Odds%"]) >= 2 and int(horse["Odds%"]) < 5:
                rating = rating + 0.2
            if int(horse["Odds%"]) == 1:
                rating = rating + 0.1
            #if int(horse["Odds%"]) < 2:            #Do nothing





            horse["Pick rating"] = str(rating)

        race.sort(key=operator.itemgetter('Pick rating'), reverse=True)


    # print(v75_list[4])
    # print("\n\n")
    # print(horse_pick_list)
    horses_to_pick = []


    for i in range(7):                                                  #Based on the random pick generator, pick the horses based on their sorted rating
        counter = 0
        for horse in v75_list[i]:
            horses_to_pick.append(horse)
            counter = counter + 1
            if counter == horse_pick_list[i]:
                break

    #print(horses_to_pick)

    return horses_to_pick





def calculate_stake(nr_of_spikar, stakes):

    print("test")
