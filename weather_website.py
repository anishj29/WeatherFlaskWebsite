# Import Statements
import json
import time
import urllib.request
from datetime import datetime, timezone
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps

hourly_images = []
daily_images = []
id_list = []
main_list = []

sunr = ''
suns = ''

month_to_short = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                  11: 'Nov', 12: 'Dec'}
date = datetime.today()

month = month_to_short[date.month]


def check_icon(id_tag):
    id_tag_str = str(id_tag)
    id_list.append(id_tag)

    if id_tag == 800:
        return 'static/icons/icon-2.svg'

    elif id_tag == 200 or id_tag == 201 or id_tag == 202 or id_tag == 230 or id_tag == 231 or id_tag == 232:
        return 'static/icons/icon-11.svg'

    elif id_tag == 210 or id_tag == 211 or id_tag == 212 or id_tag == 221:
        return 'static/icons/icon-12.svg'

    elif id_tag_str[0] == '3':
        return 'static/icons/icon-9.svg'

    elif id_tag == 500 or id_tag == 501 or id_tag == 502 or id_tag == 503 or id_tag == 504:
        return 'static/icons/icon-4.svg'

    elif id_tag == 511 or id_tag == 520 or id_tag == 521 or id_tag == 522 or id_tag == 531:
        return 'static/icons/icon-10.svg'

    elif id_tag_str[0] == '6':
        return 'static/icons/icon-13.svg '

    elif id_tag_str[0] == '7':
        return 'static/icons/icon-8.svg'

    elif id_tag == 801:
        return 'static/icons/icon-3.svg'

    elif id_tag == 802:
        return 'static/icons/icon-5.svg'

    elif id_tag == 803:
        return 'static/icons/icon-6.svg'

    elif id_tag == 803 or id_tag == 804:
        return 'static/icons/icon-6.svg'

    else:
        return 'error'


app = Flask(__name__)
GoogleMaps(app)


@app.route('/', methods=['POST', 'GET'])
def weather():
    global image
    if request.method == 'POST':
        city = request.form['city'].title()
    else:
        # for default name mathura
        city = 'Plainsboro'

    new_city = city

    if ' ' in city:
        new_city = city.replace(' ', '+')

    # your API key will come here
    api = '8a5edfd4d0e0f8953dbe82364cfc0b10'

    try:
        # source contain json data from api
        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + new_city + '&appid=' + api).read()

        # converting JSON data to a dictionary
        list_of_data = json.loads(source)

    except:
        return render_template('404.html')

    else:
        alert_source = urllib.request.urlopen('https://api.helios.earth/v1/alerts?lat=43.1563&lon=lat=33.5437&lon=-112.1155')
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "city_name": str(city),
            "main": list_of_data['weather'][0]['main'],
            "description": list_of_data['weather'][0]['description'],
            "coordinate": str(list_of_data['coord']['lon']) + ' '
                          + str(list_of_data['coord']['lat']),
            "temp": int(round(1.8 * (list_of_data['main']['temp'] - 273) + 32, 0)),
            "temp_min": int(round(1.8 * (list_of_data['main']['temp_min'] - 273) + 32, 0)),
            "temp_max": int(round(1.8 * (list_of_data['main']['temp_max'] - 273) + 32, 0)),
            "feels_like": int(round(1.8 * (list_of_data['main']['feels_like'] - 273) + 32, 0)),
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            "wind_speed": list_of_data['wind']['speed'],
            'id': list_of_data['weather'][0]['id'],
            'sunrise': list_of_data['sys']['sunrise'],
            'sunset': list_of_data['sys']['sunset'],
            'offset': list_of_data['timezone']
        }
        lat = str(list_of_data['coord']['lat'])
        lon = str(list_of_data['coord']['lon'])

        # Sunrise and Sunset
        sunrise_time = data['sunrise'] + data['offset']
        sunset_time = data['sunset'] + data['offset']

        sunrise = datetime.fromtimestamp(sunrise_time, timezone.utc).strftime('%I:%M %p')
        sunset = datetime.fromtimestamp(sunset_time, timezone.utc).strftime('%I:%M %p')
        sun_time = [sunrise, sunset]

        # Hourly Weather
        hourly_source = urllib.request.urlopen(
            'https://api.openweathermap.org/data/2.5/onecall?lat=' + lat + '&lon=' + lon +
            '&exclude=minutely,current&appid=' + api).read()
        hourly_data = json.loads(hourly_source)

        # Hourly Weather stored in dictionary
        data_hourly = {
            'hour_1': hourly_data['hourly'][0]['dt'],
            'hour_1_temp': int(round(1.8 * (hourly_data['hourly'][0]['temp'] - 273) + 32, 0)),
            'hour_1_id': hourly_data['hourly'][0]['weather'][0]['id'],
            'hour_1_main': hourly_data['hourly'][0]['weather'][0]['main'],
            'hour_1_windspeed': hourly_data['hourly'][0]['wind_speed'],
            'hour_2': hourly_data['hourly'][1]['dt'],
            'hour_2_temp': int(round(1.8 * (hourly_data['hourly'][1]['temp'] - 273) + 32, 0)),
            'hour_2_windspeed': hourly_data['hourly'][1]['wind_speed'],
            'hour_2_id': hourly_data['hourly'][1]['weather'][0]['id'],
            'hour_2_main': hourly_data['hourly'][1]['weather'][0]['main'],
            'hour_3': hourly_data['hourly'][2]['dt'],
            'hour_3_temp': int(round(1.8 * (hourly_data['hourly'][2]['temp'] - 273) + 32, 0)),
            'hour_3_windspeed': hourly_data['hourly'][2]['wind_speed'],
            'hour_3_id': hourly_data['hourly'][2]['weather'][0]['id'],
            'hour_3_main': hourly_data['hourly'][2]['weather'][0]['main'],
            'hour_4': hourly_data['hourly'][3]['dt'],
            'hour_4_temp': int(round(1.8 * (hourly_data['hourly'][3]['temp'] - 273) + 32, 0)),
            'hour_4_windspeed': hourly_data['hourly'][3]['wind_speed'],
            'hour_4_id': hourly_data['hourly'][3]['weather'][0]['id'],
            'hour_4_main': hourly_data['hourly'][3]['weather'][0]['main'],
            'hour_5': hourly_data['hourly'][4]['dt'],
            'hour_5_temp': int(round(1.8 * (hourly_data['hourly'][4]['temp'] - 273) + 32, 0)),
            'hour_5_windspeed': hourly_data['hourly'][4]['wind_speed'],
            'hour_5_id': hourly_data['hourly'][4]['weather'][0]['id'],
            'hour_5_main': hourly_data['hourly'][4]['weather'][0]['main'],
            'hour_6': hourly_data['hourly'][5]['dt'],
            'hour_6_temp': int(round(1.8 * (hourly_data['hourly'][5]['temp'] - 273) + 32, 0)),
            'hour_6_windspeed': hourly_data['hourly'][5]['wind_speed'],
            'hour_6_id': hourly_data['hourly'][5]['weather'][0]['id'],
            'hour_6_main': hourly_data['hourly'][5]['weather'][0]['main'],
            'hour_7': hourly_data['hourly'][6]['dt'],
            'hour_7_temp': int(round(1.8 * (hourly_data['hourly'][6]['temp'] - 273) + 32, 0)),
            'hour_7_windspeed': hourly_data['hourly'][6]['wind_speed'],
            'hour_7_id': hourly_data['hourly'][6]['weather'][0]['id'],
            'hour_7_main': hourly_data['hourly'][6]['weather'][0]['main'],
            'hour_8': hourly_data['hourly'][7]['dt'],
            'hour_8_temp': int(round(1.8 * (hourly_data['hourly'][7]['temp'] - 273) + 32, 0)),
            'hour_8_windspeed': hourly_data['hourly'][7]['wind_speed'],
            'hour_8_id': hourly_data['hourly'][7]['weather'][0]['id'],
            'hour_8_main': hourly_data['hourly'][7]['weather'][0]['main'],
            'hour_9': hourly_data['hourly'][8]['dt'],
            'hour_9_temp': int(round(1.8 * (hourly_data['hourly'][8]['temp'] - 273) + 32, 0)),
            'hour_9_windspeed': hourly_data['hourly'][8]['wind_speed'],
            'hour_9_id': hourly_data['hourly'][8]['weather'][0]['id'],
            'hour_9_main': hourly_data['hourly'][8]['weather'][0]['main'],
            'hour_10': hourly_data['hourly'][9]['dt'],
            'hour_10_temp': int(round(1.8 * (hourly_data['hourly'][9]['temp'] - 273) + 32, 0)),
            'hour_10_windspeed': hourly_data['hourly'][9]['wind_speed'],
            'hour_10_id': hourly_data['hourly'][9]['weather'][0]['id'],
            'hour_10_main': hourly_data['hourly'][9]['weather'][0]['main'],
            'hour_11': hourly_data['hourly'][10]['dt'],
            'hour_11_temp': int(round(1.8 * (hourly_data['hourly'][10]['temp'] - 273) + 32, 0)),
            'hour_11_windspeed': hourly_data['hourly'][10]['wind_speed'],
            'hour_11_id': hourly_data['hourly'][10]['weather'][0]['id'],
            'hour_11_main': hourly_data['hourly'][10]['weather'][0]['main'],
            'hour_12': hourly_data['hourly'][11]['dt'],
            'hour_12_temp': int(round(1.8 * (hourly_data['hourly'][11]['temp'] - 273) + 32, 0)),
            'hour_12_windspeed': hourly_data['hourly'][11]['wind_speed'],
            'hour_12_id': hourly_data['hourly'][11]['weather'][0]['id'],
            'hour_12_main': hourly_data['hourly'][11]['weather'][0]['main'],
            'hour_13': hourly_data['hourly'][12]['dt']
        }

        data_daily = {
            'day_1_temp': int(round(1.8 * (hourly_data['daily'][0]['temp']['day'] - 273) + 32, 0)),
            'day_1_max': int(round(1.8 * (hourly_data['daily'][0]['temp']['max'] - 273) + 32, 0)),
            'day_1_min': int(round(1.8 * (hourly_data['daily'][0]['temp']['min'] - 273) + 32, 0)),
            'day_1_main': hourly_data['daily'][0]['weather'][0]['main'],
            'day_1_id': hourly_data['daily'][0]['weather'][0]['id'],
            'day_2_temp': int(round(1.8 * (hourly_data['daily'][1]['temp']['day'] - 273) + 32, 0)),
            'day_2_max': int(round(1.8 * (hourly_data['daily'][1]['temp']['max'] - 273) + 32, 0)),
            'day_2_min': int(round(1.8 * (hourly_data['daily'][1]['temp']['min'] - 273) + 32, 0)),
            'day_2_main': hourly_data['daily'][1]['weather'][0]['main'],
            'day_2_id': hourly_data['daily'][1]['weather'][0]['id'],
            'day_3_temp': int(round(1.8 * (hourly_data['daily'][2]['temp']['day'] - 273) + 32, 0)),
            'day_3_max': int(round(1.8 * (hourly_data['daily'][2]['temp']['max'] - 273) + 32, 0)),
            'day_3_min': int(round(1.8 * (hourly_data['daily'][2]['temp']['min'] - 273) + 32, 0)),
            'day_3_main': hourly_data['daily'][2]['weather'][0]['main'],
            'day_3_id': hourly_data['daily'][2]['weather'][0]['id'],
            'day_4_temp': int(round(1.8 * (hourly_data['daily'][3]['temp']['day'] - 273) + 32, 0)),
            'day_4_max': int(round(1.8 * (hourly_data['daily'][3]['temp']['max'] - 273) + 32, 0)),
            'day_4_min': int(round(1.8 * (hourly_data['daily'][3]['temp']['min'] - 273) + 32, 0)),
            'day_4_main': hourly_data['daily'][3]['weather'][0]['main'],
            'day_4_id': hourly_data['daily'][3]['weather'][0]['id'],
            'day_5_temp': int(round(1.8 * (hourly_data['daily'][4]['temp']['day'] - 273) + 32, 0)),
            'day_5_max': int(round(1.8 * (hourly_data['daily'][4]['temp']['max'] - 273) + 32, 0)),
            'day_5_min': int(round(1.8 * (hourly_data['daily'][4]['temp']['min'] - 273) + 32, 0)),
            'day_5_main': hourly_data['daily'][4]['weather'][0]['main'],
            'day_5_id': hourly_data['daily'][4]['weather'][0]['id'],
            'day_6_temp': int(round(1.8 * (hourly_data['daily'][5]['temp']['day'] - 273) + 32, 0)),
            'day_6_max': int(round(1.8 * (hourly_data['daily'][5]['temp']['max'] - 273) + 32, 0)),
            'day_6_min': int(round(1.8 * (hourly_data['daily'][5]['temp']['min'] - 273) + 32, 0)),
            'day_6_main': hourly_data['daily'][5]['weather'][0]['main'],
            'day_6_id': hourly_data['daily'][5]['weather'][0]['id'],
            'day_7_temp': int(round(1.8 * (hourly_data['daily'][6]['temp']['day'] - 273) + 32, 0)),
            'day_7_max': int(round(1.8 * (hourly_data['daily'][6]['temp']['max'] - 273) + 32, 0)),
            'day_7_min': int(round(1.8 * (hourly_data['daily'][6]['temp']['min'] - 273) + 32, 0)),
            'day_7_main': hourly_data['daily'][6]['weather'][0]['main'],
            'day_7_id': hourly_data['daily'][6]['weather'][0]['id'],
            'day_8_temp': int(round(1.8 * (hourly_data['daily'][7]['temp']['day'] - 273) + 32, 0)),
            'day_8_max': int(round(1.8 * (hourly_data['daily'][7]['temp']['max'] - 273) + 32, 0)),
            'day_8_min': int(round(1.8 * (hourly_data['daily'][7]['temp']['min'] - 273) + 32, 0)),
            'day_8_main': hourly_data['daily'][7]['weather'][0]['main'],
            'day_8_id': hourly_data['daily'][7]['weather'][0]['id'],
        }

        # Organizing the hours
        hour_1 = time.localtime(data_hourly['hour_1']).tm_hour
        hour_2 = time.localtime(data_hourly['hour_2']).tm_hour
        hour_3 = time.localtime(data_hourly['hour_3']).tm_hour
        hour_4 = time.localtime(data_hourly['hour_4']).tm_hour
        hour_5 = time.localtime(data_hourly['hour_5']).tm_hour
        hour_6 = time.localtime(data_hourly['hour_6']).tm_hour
        hour_7 = time.localtime(data_hourly['hour_7']).tm_hour
        hour_8 = time.localtime(data_hourly['hour_8']).tm_hour
        hour_9 = time.localtime(data_hourly['hour_9']).tm_hour
        hour_10 = time.localtime(data_hourly['hour_10']).tm_hour
        hour_11 = time.localtime(data_hourly['hour_11']).tm_hour
        hour_12 = time.localtime(data_hourly['hour_12']).tm_hour
        hour_13 = time.localtime(data_hourly['hour_13']).tm_hour

        hour_times = [hour_1, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7, hour_8, hour_9, hour_10, hour_11, hour_12,
                      hour_13]
        # Got icon for each hour
        for i in range(1, 13):
            hourly_images.append(check_icon(data_hourly['hour_' + str(i) + '_id']))
            main_list.append(data_hourly['hour_' + str(i) + '_main'])

        for j in range(1, 9):
            daily_images.append(check_icon(data_daily['day_' + str(j) + '_id']))

        # Addded pm or am tags based on the time
        for i in range(12):
            if hour_times[i] > 12:
                hour_times[i] -= 12
                hour_times[i] = str(hour_times[i]) + ' pm'

            elif hour_times[i] == 0:
                hour_times[i] = 12
                hour_times[i] = str(hour_times[i]) + ' pm'

            else:
                hour_times[i] = str(hour_times[i]) + ' am'


        id_tag = data['id']
        id_tag_str = str(id_tag)

        # Get icon for current weather
        if id_tag == 800:
            image = 'static/icons/icon-2.svg'

        elif all(x == id_tag for x in (200, 201, 202, 230, 231, 232)):
            image = 'static/icons/icon-11.svg'

        elif all(x == id_tag for x in (210, 211, 212, 221)):
            image = 'static/icons/icon-12.svg'

        elif id_tag_str[0] == '3':
            image = 'static/icons/icon-9.svg'

        elif all(x == id_tag for x in (500, 501, 502, 503, 504)):
            image = 'static/icons/icon-4.svg'

        elif all(x == id_tag for x in (511, 520, 521, 522, 531)):
            image = 'static/icons/icon-10.svg'

        elif id_tag_str[0] == '6':
            image = 'static/icons/icon-13.svg '

        elif id_tag_str[0] == '7':
            image = 'static/icons/icon-8.svg'

        elif id_tag == 801:
            image = 'static/icons/icon-3.svg'

        elif id_tag == 802:
            image = 'static/icons/icon-5.svg'

        elif id_tag == 803 or 804:
            image = 'static/icons/icon-6.svg'

        return render_template('home.html', data=data, image=image, hour_times=hour_times, hourly_images=hourly_images,
                               data_hourly=data_hourly, data_daily=data_daily, daily_images=daily_images, month=month,
                               day=date.day, sun_time=sun_time, lat=lat, lon=lon)


if __name__ == '__main__':
    app.run(debug=True)

