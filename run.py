import gspread
import requests 
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
    print("_______________________________________________________")
    url = API_URL+"q="+city+',&APPID='+API_KEY
    print(f"Welcome today we have wonderful weather! In {city}:")
    response = requests.get(url).json()
    temp = round(response['main']['temp'] - 273.15)
    humidity = response['main']['humidity']
    descr = response['weather'][0]['description']
    print(f"Temperature: {temp}°C  *  Humidity: {humidity}%  * {descr} ")

def new_city(answer):
    if answer == "Y":
        print("Enter Your City:")
        newcity = input().upper()
        get_weather(newcity)
    elif answer =="N":
            print("OK Let's go!")
    else:
        print('The answer is accepted only yes -"Y" or no- "N", please enter your answer again: \n')
        resp = input().upper()
        new_city(resp)

def main():
    """
    Run all program functions
    """
    get_weather(city)
    print("_______________________________________________________")
    print("Do you want to change the city Y/N? \n")
    resp = input().upper()
    new_city(resp)

main()
