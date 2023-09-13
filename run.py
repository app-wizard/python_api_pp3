import gspread
import requests
import os
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('pp3sheet')

API_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = open("./api.key", "r").read()
city = "DUBLIN"


def get_weather(city):
    """
    The function receives weather data from openweathermap 
    and outputs it to the terminal
    """
    url = API_URL+"q="+city+',&APPID='+API_KEY
    response = requests.get(url).json()
    temp = round(response['main']['temp'] - 273.15)
    humidity = response['main']['humidity']
    descr = response['weather'][0]['description']

    clear()
    print("_______________________________________________________")
    print(f"Hi there! The weather in {city} today is fantastic!:")
    print(f"Temperature: {temp}°C  *  Humidity: {humidity}%  * {descr} ")
    print("_______________________________________________________")


def clear():
    """
    The function clears the terminal window
    """
    os.system('clear')


def new_city(answer):
    """
    The function outputs the weather for the city passed in the parameters
    """
    if answer == "Y":
        print("Enter Your City:")
        newcity = input().upper()
        try:
            get_weather(newcity)

        except:
            clear()
            print(
                f"Something went wrong, maybe just a typo in the name of the {newcity}, try again:")
            print("Do you want to change the city Y/N?")
            resp = input().upper()
            new_city(resp)

    elif answer == "N":
        pass
    else:
        print('The answer is accepted only yes -"Y" or no- "N", please enter Your answer again:')
        resp = input().upper()
        new_city(resp)


def salary():
    """
    The function checks the entered number for a value from 100 to 10000000
    """
    while True:
        try:
            salary_input = int(
                input("Enter a number from 100 to 10000000: \n"))
            if 100 <= salary_input <= 10000000:
                break
            else:
                print(
                    "The input takes a number in the range from 100 to 10000000. Try again.")
        except ValueError:
            print("You didn't enter a number. Try again.")

def hours():
    """
    The function checks the entered number for a value from 100 to 10000000
    """
    while True:
        try:
            hours_input = int(
                input("Enter a number from 16 to 48: \n"))
            if 16 <= hours_input <= 48:
                break
            else:
                print(
                    "Enter a number in the range from 16 to 48. Try again.")
        except ValueError:
            print("You didn't enter a number. Try again.")

def main():
    """
    Run all program functions
    """
    get_weather(city)
    print("Do you want to change the city Y/N? \n")
    resp = input().upper()
    new_city(resp)

    print("On such a beautiful day, it will be wonderful to set salary goals for yourself!")
    print("Enter the desired gross nominal salary for 2024:")
    salary()
    print("What is your intended weekly working hours, with a minimum of 16 hours and a maximum of 48 hours?")
    hours()

main()
