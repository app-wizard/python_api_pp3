import gspread
import requests
import os
from google.oauth2.service_account import Credentials
from colorama import init, Fore, Back, Style

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('pp3sheet')
WORK_SHEET = SHEET.worksheet("pay_sheet")
API_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = open("./api.key", "r").read()
city = "DUBLIN"


def get_weather(city):
    """
    The function receives weather data from openweathermap and outputs it to the terminal
    """
    url = API_URL+"q="+city+',&APPID='+API_KEY
    response = requests.get(url).json()
    temp = round(response['main']['temp'] - 273.15)
    humidity = response['main']['humidity']
    descr = response['weather'][0]['description']

    clear()
    print("_______________________________________________________")
    print(Fore.CYAN + f"Hi there! The weather in {city} today is fantastic!: ")
    print(
        f"Temperature: {temp}°C  *  Humidity: {humidity}%  * {descr} " + Fore.RESET)
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
                input("from 100 to 10000000: \n"))
            if 100 <= salary_input <= 10000000:
                WORK_SHEET.update_acell('B4', salary_input)
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
                input("from 16 to 48: \n"))
            if 16 <= hours_input <= 48:
                WORK_SHEET.update_acell('B2', hours_input)
                break
            else:
                print(
                    "Enter a number in the range from 16 to 48. Try again.")
        except ValueError:
            print("You didn't enter a number. Try again.")


def tax_calculator():
    cut_off_point = int(WORK_SHEET.acell('B15').value)
    yearly_salary = int(WORK_SHEET.acell('B4').value)

    if yearly_salary <= cut_off_point:
        tax = yearly_salary * 0.2
    else:
        tax = cut_off_point * 0.2 + (yearly_salary-cut_off_point) * 0.4

    WORK_SHEET.update_acell('B16', tax)
    print("Taxes are calculated !")
    clear()


def mood_calculator():
    """
    Сounting on how optimistic your salary expectations
    """
    after_tax_hourly_salary = float(WORK_SHEET.acell('C9').value)
    if after_tax_hourly_salary <= 14:
        print(Fore.CYAN + "Wages below 14 euros per hour - apparently, you are a Pessimist" + Fore.RESET)
    elif after_tax_hourly_salary <= 35:
        print(Fore.CYAN + "Wages below 14-35 euros  per hour  - apparently you are a Realist" + Fore.RESET)
    else:
        print(Fore.CYAN + "Wages is more than 35 euros per hour - apparently, you are an Optimist" + Fore.RESET)


def salary_calculator():
    """
    Сalculate the daily weekly annual and hourly wage rates
    """
    hours_per_week = int(WORK_SHEET.acell('B2').value)
    yearly_salary = int(WORK_SHEET.acell('B4').value)
    tax = int(WORK_SHEET.acell('B16').value)
    print(
        f"Yearly salary Gross {yearly_salary:.0f}€  *  Work hours per week: {hours_per_week}")
    print("************************************************************")
    after_tax_salary = yearly_salary - tax
    WORK_SHEET.update_acell('C4', after_tax_salary)
    print(Fore.GREEN +
          f"Your Yearly salary after tax: {after_tax_salary:.0f} €")

    monthly_salary = round(yearly_salary / 12, 2)
    WORK_SHEET.update_acell('B5', monthly_salary)
    after_tax_monthly_salary = round(after_tax_salary / 12, 2)
    WORK_SHEET.update_acell('C5', after_tax_monthly_salary)
    print(f"Your Monthly salary after tax: {after_tax_monthly_salary:.0f} €")

    beweekly_salary = round(yearly_salary / 26, 2)
    WORK_SHEET.update_acell('B6', beweekly_salary)
    after_tax_beweekly_salary = round(after_tax_salary / 26, 2)
    WORK_SHEET.update_acell('C6', after_tax_beweekly_salary)
    print(Fore.GREEN +
          f"Your Biweekly salary after tax: {after_tax_beweekly_salary:.0f} €")

    weekly_salary = round(yearly_salary / 52, 2)
    WORK_SHEET.update_acell('B7', weekly_salary)
    after_tax_weekly_salary = round(after_tax_salary / 52, 2)
    WORK_SHEET.update_acell('C7', after_tax_weekly_salary)
    print(f"Your Weekly salary after tax: {after_tax_weekly_salary:.0f} €")

    daily_salary = round(yearly_salary / 250, 2)
    WORK_SHEET.update_acell('B8', daily_salary)
    after_tax_daily_salary = round(after_tax_salary / 250, 2)
    WORK_SHEET.update_acell('C8', after_tax_daily_salary)
    print(f"Your Daily salary after tax: {after_tax_daily_salary:.0f} €")

    hourly_salary = round(weekly_salary / hours_per_week, 2)
    WORK_SHEET.update_acell('B9', hourly_salary)
    after_tax_hourly_salary = round(
        after_tax_weekly_salary / hours_per_week, 2)
    WORK_SHEET.update_acell('C9', after_tax_hourly_salary)
    print(
        f"Your Hourly salary after tax: {after_tax_hourly_salary:.0f} €" + Fore.RESET)


def main():
    """
    Run all program functions
    """
    clear()
    get_weather(city)
    print("Do you want to change the city Y/N?")
    resp = input().upper()
    new_city(resp)
    print(Fore.CYAN + "On such a beautiful day, it will be wonderful to set salary goals for yourself!")
    print("Enter the desired gross nominal salary for 2024" + Fore.RESET)
    salary()
    print(Fore.CYAN + "What is your intended weekly working hours?" + Fore.RESET)
    hours()
    tax_calculator()
    salary_calculator()
    mood_calculator()
    print("************************************************************")
    print(Fore.GREEN + "A detailed calculation can be found in the Google table at:" + Fore.RESET)
    print("https://docs.google.com/spreadsheets/d/1OgR1vfutXLjA3ovPVGmPvRmwxdp7pBJh-PtBvjiMQKs/edit#gid=0")
    print(Fore.GREEN + """
 /\_/\                                             /\_/\  
( o.o ) Thank you for using our salary calculator ( o.o ) 
 > ^ <                                             > ^ <
""" + Fore.RESET)


main()