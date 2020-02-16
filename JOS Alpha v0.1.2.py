from datetime import datetime
import requests
import json
import calendar

days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        ]

def get_weather(daysOpen = 0):

    day_list = days[0:daysOpen]


        #Call API for Austin weather
    w = requests.get('http://api.openweathermap.org/data/2.5/forecast?id=4671654&APPID=35473a0fbc6f1d073918940306dd643c')

        #parse for 'list' block
    data = w.json().get('list')

    week_list = []

        # Iterates through 'list' block.  Checks for times 9,12,15,18 which are shop hours
        # against the time found in each block.  For those times, the weather is added to
        #the list, then averaged at the end (after farenheiht conversion)
    for i in range(len(data)):
        
        date = datetime.strptime(data[i].get('dt_txt'), "%Y-%m-%d %H:%M:%S")
        # day of the week
        day = calendar.day_name[date.weekday()]
        
        hour = date.hour
        if str(day) in days:
            if hour in [9, 12, 15, 18]:
                week_list.append(data[i].get('main').get('temp_max'))
                print("Temperature for {} is {}.".format(day, data[i].get('main').get('temp_max')))

    week_avg = sum(week_list)
    week_avg /= len(week_list)

    # convert to farenheit
    return ((week_avg - 273.15) * (9/5)) + 32

def order_calculator(shop, coldBrew, daysOpen):

    x = get_weather(daysOpen)
    
    #RLM
    if shop == 1:
        
        y = (0.5144*x) - 24.259

    elif shop == 2:

        y = (0.2588*x) - 12.055
        
    elif shop == 3:
        pass
    elif shop == 4:
        pass

    cbToOrder = round(int(y-coldBrew))
    if cbToOrder == 0:
        cbToOrder += 5
    
    return cbToOrder

def main():

    shop = int(input("Which shop are you ordering for?\n\n1 = RLM \n2 = CS \n3 = GEO \n4 = ART\n\nShop Number: "))
    
    daysOpen = int(input("\n\nEnter the number of days we are open this week.\n\nDays Open: "))

    cb = int(input("\n\nEnter how many gallons of cold brew you have.\n\nCold Brew on-hand: "))
    
    order = order_calculator(shop,cb,daysOpen)
        
    print(("\n\nYou should order:\n\n{a:2d} gallons of cold brew.".format(a=order)))

    restart = input("\n\nRun again? Enter y/n: ")

    if restart == 'y':
        main()
    else:
        print("Thank you for using Jobago's Official Cold Brew Ordering Software.")
        pass
    
main()
