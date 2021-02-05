from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests
import time
import numpy as np


# Create your views here.
#######################################################################
# Declaration of the variables

data_all = {}
colour_code1 = ""
context = {}
all_data = []
url2 = ""
rain_info = {}
city_name = ""
clothing_choice = ""


#######################################################################
# Functions for the various functionalities


# Function for recalculating the wind direction
def wind_direction(winddegree):
    # Replacing winddegree (number) to actual direction
    if 340 < winddegree < 361 or 0 <= winddegree < 20:
        winddirection = "N"
    elif 20 <= winddegree < 70:
        winddirection = "NO"
    elif 70 <= winddegree < 110:
        winddirection = "O"
    elif 110 <= winddegree < 160:
        winddirection = "ZO"
    elif 160 <= winddegree < 200:
        winddirection = "Z"
    elif 200 <= winddegree < 250:
        winddirection = "ZW"
    elif 250 <= winddegree < 291:
        winddirection = "W"
    else:
        winddirection = "NW"
    return winddirection


# Function for translating the time
def time_translate(time):
    part = time.split()
    day_week, month, day_number = part[0], part[1], part[2]
    time_hms, year = part[3], part[4]

    if day_week == "Mon":
        day_week = "Maandag"
    elif day_week == "Tue":
        day_week = "Dinsdag"
    elif day_week == "Wed":
        day_week = "Woensdag"
    elif day_week == "Thu":
        day_week = "Donderdag"
    elif day_week == "Fri":
        day_week = "Vrijdag"
    elif day_week == "Sat":
        day_week = "Zaterdag"
    elif day_week == "Sun":
        day_week = "Zondag"

    if month == "Jan":
        month = "januari"
    elif month == "Feb":
        month = "februari"
    elif month == "Mar":
        month = "maart"
    elif month == "Apr":
        month = "april"
    elif month == "Mai":
        month = "mei"
    elif month == "Jun":
        month = "juni"
    elif month == "Jul":
        month = "juli"
    elif month == "Aug":
        month = "augustus"
    elif month == "Sep":
        month = "september"
    elif month == "Oct":
        month = "oktober"
    elif month == "Nov":
        month = "november"
    elif month == "Dec":
        month = "december"

    return day_week + " " + day_number + " " + month + " " + year


# Function for isolating the hours from the time data
def hour_translate(time):
    part = time.split()
    day_week, month, day_number = part[0], part[1], part[2]
    time_hms, year = part[3], part[4]

    part2 = part[3].split(":", 3)
    hours = part2[0]
    return hours


# Functions for the various weather advices
def clothing_advice(current_temperature1):
    global clothing_choice
    if current_temperature1 >= 25:
        clothing_choice = "Het is mooi weer, trek lichte kleding aan"
    elif 20 < current_temperature1 < 25:
        clothing_choice = "Het is lekker weer vandaag, trek iets korts aan"
    elif 18 < current_temperature1 <= 20:
        clothing_choice = "Het is wat kouder weer, trek een lange broek met korte mouwen aan."
    elif 15 < current_temperature1 <= 18:
        clothing_choice = "Het is een middelmatige temperatuur, trek wat dikkere kleding aan."
    elif 5 < current_temperature1 <= 15:
        clothing_choice = "Het is koud, trek warme kleding aan."
    elif 0 < current_temperature1 <= 5:
        clothing_choice = "Het vriest bijna, trek warme kleding aan en doe misschien handschoenen aan."
    elif -10 < current_temperature1 < 0:
        clothing_choice = "Het vriest, trek dikke kleding aan en doe een muts op als je naar buiten gaat."
    return clothing_choice


def wearables_advice(circumstance):
    if circumstance == "sneeuw":
        wearables_choice = "Het sneeuwt, trek sneeuwschoenen aan."
    elif circumstance == "regen en sneeuw":
        wearables_choice = "Het kan gaan regen of sneeuwen, neem een paraplu mee."
    elif circumstance == "regen":
        wearables_choice = "Het gaat regenen, neem een paraplu mee om droog te blijven."
    elif circumstance == "matige regen" or "lichte regen":
        wearables_choice = "Het kan mogelijk een beetje gaan regenen, neem een paraplu mee."
    else:
        wearables_choice = "Het is mooi weer er is geen reden om een accessoire mee te nemen."
    return wearables_choice


def sunscreen_advice(uvi):
    if 0 <= uvi <= 2:
        sunscreen_choice = "Er is vrijwel geen zon, je hoeft je niet in te smeren."
    elif 2 < uvi <= 4:
        sunscreen_choice = "De zonsterkte is zwak, als je lang buiten bent kan je jezelf met een lage factor insmeren."
    elif 4 < uvi <= 6:
        sunscreen_choice = "De zon is van matige sterkte. Je huid verbrandt gemakkelijk, dus smeer je in."
    elif 6 < uvi <= 8:
        sunscreen_choice = "De zon is sterk deze dag. Je huid verbrandt makkelijk, dus smeer je goed in."
    elif uvi > 8:
        sunscreen_choice = "De zonsterkte is zeer hoog, smeer je met een hoge zonnebrandsfactor in."
    return sunscreen_choice


def outdoor_sport_advice(temperature, windspeed):
    if temperature < 0 or windspeed > 30 or temperature > 35:
        outdoor_sport_number = 1
    elif (0 < temperature <= 10 and 20 < windspeed <= 30) or (30 < temperature <= 35 and 20 < windspeed <= 30):
        outdoor_sport_number = 2
    elif (0 < temperature <= 10 and 10 < windspeed <= 20) or (30 < temperature <= 35 and 0 < windspeed <= 10):
        outdoor_sport_number = 3
    elif (30 < temperature <= 35) and (10 < windspeed <= 20):
        outdoor_sport_number = 4
    elif (0 < temperature <= 10 and 0 < windspeed <= 10) or 25 < temperature <= 30 and 20 < windspeed <= 30:
        outdoor_sport_number = 5
    elif (25 < temperature <= 30) and (0 < windspeed <= 20):
        outdoor_sport_number = 6
    elif (10 < temperature <= 20) and (0 < windspeed <= 20):
        outdoor_sport_number = 7
    elif (10 < temperature <= 20) and (20 < windspeed <= 30):
        outdoor_sport_number = 8
    elif (20 < temperature <= 25) and (10 < windspeed <= 30):
        outdoor_sport_number = 9
    elif (20 < temperature <= 25) and (0 < windspeed <= 10):
        outdoor_sport_number = 10
    else:
        outdoor_sport_number = "Geen cijfer beschikbaar"
    return outdoor_sport_number


def beach_advice(temperature, windspeed):
    if temperature <= 0 or windspeed > 30 or 45 < temperature:
        beach_number = 1
    elif (0 < temperature <= 10 and 20 < windspeed <= 30) or (40 < temperature <= 45 and 20 < windspeed <= 30):
        beach_number = 2
    elif (0 < temperature <= 10 and 10 < windspeed <= 20) or (40 < temperature <= 45 and 0 < windspeed <= 10):
        beach_number = 3
    elif (0 < temperature <= 10 and 0 < windspeed <= 10) or (40 < temperature <= 45 and 10 < windspeed <= 20):
        beach_number = 4
    elif 10 < temperature <= 20:
        beach_number = 5
    elif (20 < temperature <= 25 and 0 < windspeed <= 30) or (30 < temperature <= 40 and 20 < windspeed <= 30):
        beach_number = 6
    elif 25 < temperature <= 30 and 20 < windspeed <= 30:
        beach_number = 7
    elif 25 < temperature <= 30 and 0 < windspeed <= 20:
        beach_number = 8
    elif 30 < temperature <= 35 and 0 < windspeed <= 10:
        beach_number = 9
    elif 30 < temperature <= 35 and 10 < windspeed <= 20:
        beach_number = 10
    else:
        beach_number = "Geen cijfer beschikbaar"
    return beach_number


def winter_sport_advice(temperature, current_circumstance):
    if temperature >= 5:
        winter_sport_number = 1
    elif 0 < temperature < 5 and current_circumstance == "dichte mist":
        winter_sport_number = 2
    elif 3 < temperature < 5:
        winter_sport_number = 3
    elif 0 < temperature <= 3 and current_circumstance == "lichte mist":
        winter_sport_number = 4
    elif -25 < temperature <= -15 and (current_circumstance == "lichte mist" or "dichte mist"):
        winter_sport_number = 5
    elif -25 < temperature <= -15:
        winter_sport_number = 6
    elif 0 < temperature <= 3:
        winter_sport_number = 7
    elif -3 < temperature <= 0:
        winter_sport_number = 8
    elif -10 < temperature <= -7:
        winter_sport_number = 9
    elif -7 < temperature <= -3:
        winter_sport_number = 10
    else:
        winter_sport_number = "Geen cijfer beschikbaar"
    return winter_sport_number


# Function for the decleration of the colour code of the location
def colour_code(windspeed):
    # Ask data again
    global colour_code1
    res = requests.get(url2)
    data = res.json()

    # Paramaters for colour code declaration
    daily_maximum_temperature = data["daily"][0]["temp"]["max"]
    hourly_feels_like = data["hourly"][0]["feels_like"]
    visibility = data["hourly"][0]["visibility"]

    # Requirements for the different colour codes
    if windspeed < 75 or daily_maximum_temperature < 35 or hourly_feels_like > -15 or visibility > 200:
        colour_code1 = "Groen"
    elif 75 <= windspeed <= 100 or daily_maximum_temperature > 35 or hourly_feels_like < -15 or visibility < 200:
        colour_code1 = "Geel"
    elif hourly_feels_like < -20 or visibility < 10:
        colour_code1 = "Oranje"
    return colour_code1


#######################################################################
# Functions for the various pages


# Function for the home page
def pag1(request):
    # Returning the render of the right html file.
    return render(request, 'Weather_application/Index.html')


# Function for the current_weather page
def get_current_weather(request):
    global data_all
    # If a place is given inside the html form
    if request.method == 'POST':
        city_name = request.POST["city_name"]
        # city_name = city_form(request.POST)

        # Making sure the program doesn't crash when an invalid place name is given
        try:
            # API key, between the {} in the url will come the city name with the format function
            url1 = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'
            # url1 = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'.format(city_name)

            # Check whether the request got through
            # Ask the data from the Openweathermap website (is in an Json file)
            res = requests.get(url1)
            data1 = res.json()

            # Ask coordinates
            latitude = data1["coord"]["lat"]
            longitude = data1["coord"]["lon"]

            global url2
            url2 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'.format(
                latitude, longitude)

            # Ask whether the request got trough.
            res = requests.get(url2)
            data2 = res.json()

            # Display the relevant information
            current_time_offset = data2["timezone_offset"]
            global current_time
            current_time = time_translate(time.ctime(data2["current"]["dt"] - current_time_offset))
            current_temperature = data2["current"]["temp"]
            current_humidity = data2["current"]["humidity"]
            current_circumstance = data2["current"]["weather"][0]["description"]
            current_uvi = data2["current"]["uvi"]
            current_winddegree = data2["current"]["wind_deg"]
            current_icon = data2["current"]["weather"][0]["icon"]

            # Replacing windspeed from m/s to km/u
            current_windspeed = round(data2["current"]["wind_speed"] * 3.6, 2)

            # Code for the colourcode
            code = colour_code(current_windspeed)

            # Advice for outdoor sporting
            outdoor_sport = outdoor_sport_advice(current_temperature, current_windspeed)

            # Advice for going to the beach
            beach = beach_advice(current_temperature, current_windspeed)

            # Clothing advice for the user for this day
            clothing = clothing_advice(current_temperature)

            # Advice for which wearables you should take with you if you go outside
            wearables = wearables_advice(current_circumstance)

            # Advice for sunscreen usage based on the uv-index
            sunscreen = sunscreen_advice(current_uvi)

            # Advice for wintersport base on the temperature and the circumstance
            wintersport = winter_sport_advice(current_temperature, current_circumstance)


            # Call the function to get a generalised winddirection
            current_winddirection = wind_direction(current_winddegree)

            # Dictionary for all the data
            data_all = {
                "current_time": current_time,
                'current_temperature': current_temperature,
                'current_humidity': current_humidity,
                'current_circumstance': current_circumstance,
                'current_uvi': current_uvi,
                'current_winddirection': current_winddirection,
                'current_windspeed': current_windspeed,
                'current_clothing_advice': clothing,
                'current_wearables_advice': wearables,
                'current_sunscreen_advice': sunscreen,
                'current_colour_code': code,
                'current_icon': current_icon,
                'current_outdoor_sport_advice': outdoor_sport,
                'current_beach_advice': beach,
                'current_wintersport_advice': wintersport,
            }

        # Other part of the error prevention
        except KeyError:
            # If there's a key error, data_all is an empty array
            data_all = {}


# Function for the filled in city current weather path
def filled_in_current_weather(request):
    get_current_weather(request)
    # Leading the user to a page not found page when an invalid place name is given
    # By checking whether the dictionary is true (it has a value).
    if data_all:
        return render(request, 'Weather_application/current_weather_city.html', data_all)
    else:
        return HttpResponseRedirect('not_found/')


# Function for the weather forecast path
def forecast(request):
    # Returning the render of the right html file
    return render(request, 'Weather_application/forecast.html')


# Function for the weather forecast path with city name
def get_weather_forecast(request):
    global all_data
    global context

    # If a place is given inside the html form
    if request.method == 'POST':
        city_name = request.POST["city_name"]

        # Making sure the program doesn't crash when an invalid place name is given
        try:
            # API key, between the {} in the url will come the city name with the format function
            url1 = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'

            # Check whether the request got through
            # Ask the data from the Openweathermap website (is in an Json file)
            res = requests.get(url1)
            data1 = res.json()

            # Ask coordinates
            latitude = data1["coord"]["lat"]
            longitude = data1["coord"]["lon"]

            url2 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'.format(
                latitude, longitude)

            # Ask whether the request got trough.
            res = requests.get(url2)
            data = res.json()

            # Taking the time offset in account
            time_offset = data["timezone_offset"]

            # Dictionary for the data for all the days in an array
            all_data = [
                {
                    'day': time_translate(time.ctime(data["daily"][0]["dt"] + time_offset)),
                    'forecast_temperature': round((data["daily"][0]["temp"]["min"] + data["daily"][0]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][0]["humidity"],
                    'forecast_circumstance':  data["daily"][0]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][0]["uvi"],
                    'forecast_winddegree': data["daily"][0]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][0]["wind_speed"] * 3.6, 2),
                    'forecast_icon': data["daily"][0]["weather"][0]["icon"],
                    'forecast_clothing_advice': '',
                    'forecast_sunscreen_advice': '',
                    'forecast_wearables_advice': '',
                    'forecast_outdoor_sport_advice': '',
                    'forecast_beach_advice': '',
                },
                {
                    'day': time_translate(time.ctime(data["daily"][1]["dt"] + time_offset)),
                    'forecast_temperature': round((data["daily"][1]["temp"]["min"] + data["daily"][1]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][1]["humidity"],
                    'forecast_circumstance': data["daily"][1]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][1]["uvi"],
                    'forecast_winddegree': data["daily"][1]["wind_deg"],
                    'forecast_windspeed': round(data["daily"][1]["wind_speed"] * 3.6, 2),
                    'forecast_icon': data["daily"][1]["weather"][0]["icon"],
                    'forecast_clothing_advice': '',
                    'forecast_sunscreen_advice': '',
                    'forecast_wearables_advice': '',
                    'forecast_outdoor_sport_advice': '',
                    'forecast_beach_advice': '',
                },
                {
                    'day': time_translate(time.ctime(data["daily"][2]["dt"] + time_offset)),
                    'forecast_temperature': round((data["daily"][2]["temp"]["min"] + data["daily"][2]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][2]["humidity"],
                    'forecast_circumstance':  data["daily"][2]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][2]["uvi"],
                    'forecast_winddegree': data["daily"][2]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][2]["wind_speed"] * 3.6, 2),
                    'forecast_icon': data["daily"][2]["weather"][0]["icon"],
                    'forecast_clothing_advice': '',
                    'forecast_sunscreen_advice': '',
                    'forecast_wearables_advice': '',
                    'forecast_outdoor_sport_advice': '',
                    'forecast_beach_advice': '',
                },
                {
                    'day': time_translate(time.ctime(data["daily"][3]["dt"] + time_offset)),
                    'forecast_temperature': round((data["daily"][3]["temp"]["min"] + data["daily"][3]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][3]["humidity"],
                    'forecast_circumstance':  data["daily"][3]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][3]["uvi"],
                    'forecast_winddegree': data["daily"][3]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][3]["wind_speed"] * 3.6, 2),
                    'forecast_icon': data["daily"][3]["weather"][0]["icon"],
                    'forecast_clothing_advice': '',
                    'forecast_sunscreen_advice': '',
                    'forecast_wearables_advice': '',
                    'forecast_outdoor_sport_advice': '',
                    'forecast_beach_advice': '',
                },
                {
                    'day': time_translate(time.ctime(data["daily"][4]["dt"] + time_offset)),
                    'forecast_temperature': round((data["daily"][4]["temp"]["min"] + data["daily"][4]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][4]["humidity"],
                    'forecast_circumstance':  data["daily"][4]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][4]["uvi"],
                    'forecast_winddegree': data["daily"][4]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][4]["wind_speed"] * 3.6, 2),
                    'forecast_icon': data["daily"][4]["weather"][0]["icon"],
                    'forecast_clothing_advice': '',
                    'forecast_sunscreen_advice': '',
                    'forecast_wearables_advice': '',
                    'forecast_outdoor_sport_advice': '',
                    'forecast_beach_advice': '',
                },
                {
                    'day': time_translate(time.ctime(data["daily"][5]["dt"] + time_offset)),
                    'forecast_temperature': round((data["daily"][5]["temp"]["min"] + data["daily"][5]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][5]["humidity"],
                    'forecast_circumstance':  data["daily"][5]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][5]["uvi"],
                    'forecast_winddegree': data["daily"][5]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][5]["wind_speed"] * 3.6, 2),
                    'forecast_icon': data["daily"][5]["weather"][0]["icon"],
                    'forecast_clothing_advice': '',
                    'forecast_sunscreen_advice': '',
                    'forecast_wearables_advice': '',
                    'forecast_outdoor_sport_advice': '',
                    'forecast_beach_advice': '',
                },
                {
                    'day': time_translate(time.ctime(data["daily"][6]["dt"] + time_offset)),
                    'forecast_temperature': round((data["daily"][6]["temp"]["min"] + data["daily"][6]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][6]["humidity"],
                    'forecast_circumstance':  data["daily"][6]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][6]["uvi"],
                    'forecast_winddegree': data["daily"][6]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][6]["wind_speed"] * 3.6, 2),
                    'forecast_icon': data["daily"][6]["weather"][0]["icon"],
                    'forecast_clothing_advice': '',
                    'forecast_sunscreen_advice': '',
                    'forecast_wearables_advice': '',
                    'forecast_outdoor_sport_advice': '',
                    'forecast_beach_advice': '',
                },
                {
                    'day': time_translate(time.ctime(data["daily"][7]["dt"] + time_offset)),
                    'forecast_temperature': round((data["daily"][7]["temp"]["min"] + data["daily"][7]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][7]["humidity"],
                    'forecast_circumstance':  data["daily"][7]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][7]["uvi"],
                    'forecast_winddegree': data["daily"][7]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][7]["wind_speed"] * 3.6, 2),
                    'forecast_icon': data["daily"][7]["weather"][0]["icon"],
                    'forecast_clothing_advice': '',
                    'forecast_sunscreen_advice': '',
                    'forecast_wearables_advice': '',
                    'forecast_outdoor_sport_advice': '',
                    'forecast_beach_advice': '',
                }
            ]

            # For-loop in which the winddegree gets converted from a number into a real direction
            # The clothing advice, the sunscreen advice and the wearables advice.
            # The i gives the placement in the all_data array.
            # These empty keys get replaced by the outcome of the various functions
            for i in range(0, len(all_data)):
                all_data[i]['forecast_winddegree'] = wind_direction(all_data[i]['forecast_winddegree'])
                all_data[i]['forecast_clothing_advice'] = clothing_advice(all_data[i]['forecast_temperature'])
                all_data[i]['forecast_sunscreen_advice'] = sunscreen_advice(all_data[i]['forecast_uvi'])
                all_data[i]['forecast_wearables_advice'] = wearables_advice(all_data[i]['forecast_circumstance'])
                all_data[i]['forecast_outdoor_sport_advice'] = outdoor_sport_advice(all_data[i]['forecast_temperature'], all_data[i]['forecast_windspeed'])
                all_data[i]['forecast_beach_advice'] = beach_advice(all_data[i]['forecast_temperature'], all_data[i]['forecast_windspeed'])
                all_data[i]['forecast_wintersport_advice'] = winter_sport_advice(all_data[i]['forecast_temperature'], all_data[i]['forecast_circumstance'])

        # Other part of the error prevention
        except KeyError:
            # If there's a key error, all_data is an empty array
            all_data = []

    # Put the array all_data in a dictionary named context, so that django can render it to the html file.
    context = {'all_data': all_data}
    return context


# Function to render the information to the html file
def filled_in_weather_forecast(request):
    get_weather_forecast(request)
    # Leading the user to a page not found page when an invalid place name is given
    # By checking whether the dictionary is true (it has a value).
    if all_data:
        return render(request, 'Weather_application/forecast_weather_city.html', context)
    else:
        return HttpResponseRedirect('not_found/')


# Function for the data from the rain path
def rain(request):
    return render(request, 'Weather_application/rain.html')


def get_rain(request):
    global rain_info, city_name
    # If a place is given inside the html form
    if request.method == 'POST':
        city_name = request.POST["city_name"]

        # Making sure the program doesn't crash when an invalid place name is given
        try:
            # API key, between the {} in the url will come the city name with the format function
            url1 = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'

            # Check whether the request got through
            # Ask the data from the Openweathermap website (is in an Json file)
            res = requests.get(url1)
            data1 = res.json()

            # Ask coordinates
            latitude = data1["coord"]["lat"]
            longitude = data1["coord"]["lon"]

            url2 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'.format(
                latitude, longitude)

            # Ask whether the request got trough.
            res = requests.get(url2)
            data = res.json()

            # Empty array that will be filled with information in the for-loop
            rain_data = []

            # For loop to check whether there's rain coming and and returning 0 if there isn't
            for i in range(0, 24, 2):
                if data["hourly"][i]["weather"][0]["main"] == "Rain":
                    hour_rain = data["hourly"][i]["rain"]["1h"]
                else:
                    hour_rain = 0
                rain_data.append(hour_rain)

            # Determine with the numpy sum function what the accumulated rain is, to display a corresponding icon.
            total_rain = np.sum(rain_data)
            if total_rain <= 0:
                rain_image = "https://lh3.googleusercontent.com/5lIq2xDFlMftwteLDBlH1nfcpd2TMbkf9285uutq6cc15Oh5CYats7EuXdOj6SvYJL50lCYE-_t5WxLZrtC19JTaRBWQ6Foz4mcOGiFcIVRkpjyUUyAV61icNNwe9yhQRySDwaSq1HFaVtOoKaI3UVm26aOZkTPeWGIUIaSHLVElBtJ41Xp2eDOigoQxNWKUR61nhIMVhX2g6PUaepZ-NmcKmH6YDDvSBiA0o-EYtA0GrejsHHKZB7TUdDdaJiJKyG5LCfNsrRHquZuND3QjUA2GupjumMR5yUN98lVWp08921-ZJcq4CGNdXRRE_K9fkITtZulOLZ82AeLvzNEEjv1LG-xCsNtY1Fwc5WVDTnJu4RYXTjltCWMflp1up3I2PE3WYdTox73IGAyqFSpppwHKW6Dmj_-XYj7qfD_CLHsW_jglr_eJUUw7zkqlVK1vdlFR0R12xGRdD2hSngFfYnzJYRTGVjOmsZYgYpqrJqgd3QgCb2CAT9uqRF0KpUZavel-hfIWTSUtNKGcPcZylPloak3Ugw1nX90Ehng2agVHNDyj63vlk_eFaELX6XWYrpJnsWfXT6FkT62Ml1nHSO3SAFSJA6JyxSElTv7lrgtbHqoXLZ1gO_Nh2jLX9mTsTbg0or2MWAVkVywmfGqTwUduvH0d4w0QamdwrzgOULmSJ2oQCxcsBNlJpeFK=w186-h114-no?authuser=0"
            elif 0 < total_rain <= 3:
                rain_image = "https://lh3.googleusercontent.com/RcvjzjZW1qD22c-sJHKnaTVF2NKDpBowl9reXJ91GEQM6bIVTmOCT7aQampwqJhtnAB8MCfRm2K8kLWQ_pE0CvKl8RlStge7fBafLfd8ffnDHLir72yHRDjnMh8Hyg3QwIpA6kD2Rl1gRZLaNAhU1G9QghfODRijQtAlSQD5vLVmC852lGXIozRCmQkR1_XRmBHJUhQQsRJtM-vED7_9PrOqL9hL_X8HXxNy4iAlFb-cuGEhqjUlOsujp0jMCLB8ZdmSnH_uYU8QERKvRRITRJ1dnk8McBhWsRhiGWtEVBjc5vv37SIfXVxL8lSwUxbpMjNYGeO3uqXTZTD1xpZ4_P8H7mxQRceM5ibYDD02OZMMxtV6vGgfHiCfIfrBQk0ykkVAt6pQ2iyzH66SHqYUlCHaSAey6x6dQH9KnF7haiuPnaSu5xLJl3U_MugZlGga-gwV2LGSqzKSq_rM6t4ttfuONicVT_uYF1u1zch1lEGvdHBRaBw_D3fwqZeLLttEiU0qwxiKb409Mi6Fh0RQxWJ-sCXiCL4FTtdVA4xByFPVi_xYBRUTocPfBvZx81NB55aIIoTv2l27712nfuOkqABG0WwlfAFNhnQPEw_tqspbcVghDVr55mN28iq1uMwyvLnweNJWeowePFg3-0Idg_DuMocRAOyS0UTy_hYkxP_kp1fJEl2_r4H_GwoJ=w175-h168-no?authuser=0"
            elif 3 < total_rain <= 6:
                rain_image = "https://lh3.googleusercontent.com/JMjENuaaIAIa26VBzBZmEEiGk3zsNKCclUjug4XBGrVjLb42zokYYyGSoMeZnJVIP5-inbDjU8RclcO4TLPqrVnKIkFbnVSiEza7bimTJmK-8tJVSW2dlRQ4Wwg0kC0NOjEDwCEu-gpLy_EvOgB4r3VCGhsFkpml1Zu24TUFfafi5VFP6etEWyrOPL63NrkfvHti21rTjAr3GRzSySeRxYPoNJVP4ynvpYEEBALCuxNjhZFSXcqUwxwzYi13Kw7trFLZ4n0Wm3Fo0OL9TRecRXs6ZrSXp9lH-b3OgQeqmzwQcTArO0LlpHQnGmzQzwKvNqF2N6eMi5O17EESeF96b3KrMY5jzRz9c0iFx-B2QZ5EBJyctp16k_zqYrVT-Ro-LregERGN-9tuZhMb95MzPp-_gMkC5yKmeMyuc4YRqoAcmseH59Vo19FwlNqGArZQHrjf00zCW1cdiehaVuNsXSQu9ptpXqrAODcE3_eyczdo-h5jBS_BWEw1ZZ6X0FdJ2xGzrd60aVjc82ithg15w4na10RwRW6yoFeLuAsG0SM8ayzMTx948w1-mOlLND9eXzshbVmJhj-_mUoZzrSwGfhnJzvwpwyU0yLWdY_quL9w-BPV9kD9hVO45f9eO7RpgxSCpCNnnZOLDY9atd9VlJM_3NYZUjvSMbvDb1tBCiefuiS1f6Zil5u9vHsN=w141-h138-no?authuser=0"
            else:
                rain_image = "https://lh3.googleusercontent.com/_KF7kudBnl6uDeSVJAXhXkgER6ctCpzjhJrFZVwYGhnYb_DuRb6BJw_NqxSDnJRm_feslWI45vl7DIUjPKo-vQRzRTAhM_2B26zxHHjmSbaztlZ1EdAMTgM7LuXFrP_wdbA5i-LLTZBk7gV-IPsFurVhc3ZunJMPBPTeaR0OjFsh5-c-9_xHl9NSuizwNZhlOCw5Z1ze3v67y8ZMd2V9KBLhLTAyyvGghwkZPYjGJu76A4ztJx3B7vHDpJR7q5t0aahyjAMqFkjbAHjHBQDSwg_7sIHjWPl7Dk-aMDOtQwVGveEcb5n5evWvx5x4eoYI8oibe8ir5zJHcaC8F40pgRfw1rD537Ky2K1hK3OIbMFlSBr_L4R-YToyPqWlHliohpyrGyhH-l1yHib6Ge2RxZo8-nqEnX1aYA0vsexWYocWNFQzLDQ5KDeDg2IsDAO9bZIPozjOsaFHM902eiYbaehmqHuAhjeFcMeiH7GusRQ8SNQI2rojj0pOifoJI3uXAO3WaawflKZxZteJ4WYN1AuGkwdnlgQdBOyZGqCMdRhiRqaOJTT85ReBlrKNRDWzIyR6VMjC19WPGYEr7rXhZPkeIEuCgJSldmiFdUn6eyW0P6jBgsTn1BYQhjsTzWYVM3QWlBNpEJE5DtWNdnSYkHjyCHC8whdUXYCqjn2trjR21EXHvntG1SbV5xzR=w144-h150-no?authuser=0"

            # Dictionary for the graph
            rain_info = {
                "name_place": city_name,
                "first_hour_time": hour_translate(time.ctime(data["hourly"][0]["dt"] + 3600)),
                "third_hour_time": hour_translate(time.ctime(data["hourly"][2]["dt"] + 3600)),
                "fifth_hour_time": hour_translate(time.ctime(data["hourly"][4]["dt"] + 3600)),
                "seventh_hour_time": hour_translate(time.ctime(data["hourly"][6]["dt"] + 3600)),
                "ninth_hour_time": hour_translate(time.ctime(data["hourly"][8]["dt"] + 3600)),
                "eleventh_hour_time": hour_translate(time.ctime(data["hourly"][10]["dt"] + 3600)),
                "thirteenth_hour_time": hour_translate(time.ctime(data["hourly"][12]["dt"] + 3600)),
                "fifteenth_hour_time": hour_translate(time.ctime(data["hourly"][14]["dt"] + 3600)),
                "seventeenth_hour_time": hour_translate(time.ctime(data["hourly"][16]["dt"] + 3600)),
                "nineteenth_hour_time": hour_translate(time.ctime(data["hourly"][18]["dt"] + 3600)),
                "twenty_first_hour_time": hour_translate(time.ctime(data["hourly"][20]["dt"] + 3600)),
                "twenty_third_hour_time": hour_translate(time.ctime(data["hourly"][22]["dt"] + 3600)),

                'first_hour_rain': rain_data[0],
                'third_hour_rain': rain_data[1],
                'fifth_hour_rain': rain_data[2],
                'seventh_hour_rain': rain_data[3],
                'ninth_hour_rain': rain_data[4],
                'eleventh_hour_rain': rain_data[5],
                'thirteenth_hour_rain': rain_data[6],
                'fifteenth_hour_rain': rain_data[7],
                'seventeenth_hour_rain': rain_data[8],
                'nineteenth_hour_rain': rain_data[9],
                'twenty_first_hour_rain': rain_data[10],
                'twenty_third_hour_rain': rain_data[11],

                "rain_image": rain_image,
            }

        except KeyError:
            # If there's a key error, all_data is an empty array
            rain_info = {}

    return rain_info


# Function for the filled in rain path
def filled_in_rain(request):
    get_rain(request)
    # Leading the user to a page not found page when an invalid place name is given
    # By checking whether the dictionary is true (it has a value).
    if rain_info:
        return render(request, 'Weather_application/rain_city.html', rain_info)
    else:
        return HttpResponseRedirect('not_found/')


# Function for the page not found path
def page_not_found(request):
    return render(request, 'Weather_application/Place_not_found.html')
