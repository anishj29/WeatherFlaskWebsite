# Import Statements
import datetime
import json
import urllib.request
import pytz
from flask import Flask, render_template, request
from googletrans import Translator

hourly_images = []
daily_images = []
id_list = []
main_list = []
alerts_image = ''

month_to_short = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                  11: 'Nov', 12: 'Dec'}
date = datetime.datetime.today()

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


@app.route('/', methods=['POST', 'GET'])
def weather():
    global alerts_image
    if request.method == 'POST':
        city = request.form['city'].title()
    else:
        # for default name mathura
        city = 'Princeton'

    new_city = city

    if ' ' in city:
        new_city = city.replace(' ', '+')

    # your API key will come here
    api = '8a5edfd4d0e0f8953dbe82364cfc0b10'
    ref_description = ''
    alerts_data = ''
    try:
        # source contain json data from api
        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + new_city + '&appid=' + api).read()

        # converting JSON data to a dictionary
        list_of_data = json.loads(source)

    except:
        return render_template('404.html')

    else:
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

        sunrise = datetime.datetime.fromtimestamp(sunrise_time, datetime.timezone.utc).strftime('%I:%M %p')
        sunset = datetime.datetime.fromtimestamp(sunset_time, datetime.timezone.utc).strftime('%I:%M %p')
        sun_time = [sunrise, sunset]

        temp = 'imperial'

        # Hourly Weather
        hourly_source = urllib.request.urlopen(
            'https://api.openweathermap.org/data/2.5/onecall?lat=' + lat + '&lon=' + lon +
            '&units=' + temp + '&exclude=minutely,current&appid=' + api).read()

        hourly_data = json.loads(hourly_source)

        # Gets accurate hour, day and month for searched location
        tz = hourly_data['timezone']
        datetime_tz = datetime.datetime.now(pytz.timezone(tz))
        day = datetime_tz.day
        day_2 = datetime_tz + datetime.timedelta(days=1)
        day_2 = day_2.day
        day_3 = datetime_tz + datetime.timedelta(days=2)
        day_3 = day_3.day
        day_4 = datetime_tz + datetime.timedelta(days=3)
        day_4 = day_4.day
        day_5 = datetime_tz + datetime.timedelta(days=4)
        day_5 = day_5.day
        day_6 = datetime_tz + datetime.timedelta(days=5)
        day_6 = day_6.day
        day_7 = datetime_tz + datetime.timedelta(days=6)
        day_7 = day_7.day

        list_of_days = [day, day_2, day_3, day_4, day_5, day_6, day_7]

        month_name = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                      10: 'Oct', 11: 'Nov', 12: 'Dec'}

        current_month = datetime_tz.month
        current_month = month_name[current_month]
        month_2 = datetime_tz + datetime.timedelta(days=1)
        month_2 = month_name[month_2.month]
        month_3 = datetime_tz + datetime.timedelta(days=2)
        month_3 = month_name[month_3.month]
        month_4 = datetime_tz + datetime.timedelta(days=3)
        month_4 = month_name[month_4.month]
        month_5 = datetime_tz + datetime.timedelta(days=4)
        month_5 = month_name[month_5.month]
        month_6 = datetime_tz + datetime.timedelta(days=5)
        month_6 = month_name[month_6.month]
        month_7 = datetime_tz + datetime.timedelta(days=6)
        month_7 = month_name[month_7.month]

        list_of_months = [current_month, month_2, month_3, month_4, month_5, month_6, month_7]

        current_hour = int(datetime_tz.strftime("%H"))
        hour_2 = current_hour + 1
        hour_3 = hour_2 + 1
        hour_4 = hour_3 + 1
        hour_5 = hour_4 + 1
        hour_6 = hour_5 + 1
        hour_7 = hour_6 + 1

        list_of_hours = [current_hour, hour_2, hour_3, hour_4, hour_5, hour_6, hour_7]

        for i in range(len(list_of_hours)):
            if list_of_hours[i] > 24:
                list_of_hours[i] -= 24

            if list_of_hours[i] > 12:
                list_of_hours[i] -= 12
                list_of_hours[i] = str(list_of_hours[i]) + ' pm'

            elif list_of_hours[i] == 0:
                list_of_hours[i] = 12
                list_of_hours[i] = str(list_of_hours[i]) + ' pm'

            else:
                list_of_hours[i] = str(list_of_hours[i]) + ' am'
        try:
            get_id = urllib.request.urlopen('http://dataservice.accuweather.com/locations/v1/cities/search?' +
                                            'apikey=4zrGVjvJENvvA6SvIPA6hW1qUmtKqCcd&q=' + new_city.lower() +
                                            '&details=false').read()

        except:
            pop_list = []

            for i in range(0, 8):
                pop_list.append('N/A')

        else:
            city_id = json.loads(get_id)
            key = city_id[0]["Key"]

            get_pop = urllib.request.urlopen('http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' + key +
                                             '?apikey=4zrGVjvJENvvA6SvIPA6hW1qUmtKqCcd&details=false').read()
            pop_info = json.loads(get_pop)

            pop_list = []

            for i in range(0, 8):
                pop_list.append(pop_info[i]['PrecipitationProbability'])

        alerts_api = '888c4677014d4578a511570492df67b0'
        alerts = urllib.request.urlopen(
            'https://api.weatherbit.io/v2.0/alerts?lat=' + lat + '&lon=' + lon + '&key=' + alerts_api).read()
        alerts_store = json.loads(alerts)

        try:
            alerts_data = {
                'expires': alerts_store['alerts'][0]['expires_utc'],
                'effective': alerts_store['alerts'][0]['effective_local'],
                'description': alerts_store['alerts'][0]['description'],
                'effective_utc': alerts_store['alerts'][0]['effective_utc'],
                'severity': alerts_store['alerts'][0]['severity'],
                'title': alerts_store['alerts'][0]['title'],
                'local_expire': alerts_store['alerts'][0]['expires_local']
            }

        except IndexError:
            ref_description = 'No alerts in this area!'

        else:
            translator = Translator()
            description = translator.translate(alerts_data['description'])
            description = description.text.replace('English: ', '')
            description = description.replace('* WHAT...', 'What: ')
            description = description.replace('* WHEN...', 'When: ')
            description = description.replace('* WHERE...', 'Where: ')
            description = description.replace('* IMPACTS...', 'Impacts: ')
            description = description.replace('* ADDITIONAL DETAILS...', 'Add Details: ')
            # print(description)

            where_start = description.find('Where: ') + len('Where: ')
            where_end = description.find('When')
            where = description[where_start:where_end]

            when_start = description.find('When: ') + len('When: ')
            when_end = description.find('Impacts: ')
            when = description[when_start:when_end]

            impacts_start = description.find('Impacts: ') + len('Impacts: ')
            impacts_end = description.find('Add Details: ')
            impacts = description[impacts_start:impacts_end]

            add_start = description.find('Add Details: ') + len('Add Details: ')
            add_details = description[add_start:]

            ref_description = [where, when, impacts, add_details]

            alerts_data['description'] = description

            if alerts_data['severity'] == 'Warning':
                alerts_image = 'static/alerts/warning.png'

            elif alerts_data['severity'] == 'Watch':
                alerts_data = 'static/alerts/watch.png'

        # Hourly Weather stored in dictionary
        data_hourly = {
            'hour_1_temp': int(round(hourly_data['hourly'][0]['temp'], 0)),
            'hour_1_id': hourly_data['hourly'][0]['weather'][0]['id'],
            'hour_1_main': hourly_data['hourly'][0]['weather'][0]['main'],
            'hour_2_temp': int(round(hourly_data['hourly'][1]['temp'], 0)),
            'hour_2_id': hourly_data['hourly'][1]['weather'][0]['id'],
            'hour_2_main': hourly_data['hourly'][1]['weather'][0]['main'],
            'hour_3_temp': int(round(hourly_data['hourly'][2]['temp'], 0)),
            'hour_3_id': hourly_data['hourly'][2]['weather'][0]['id'],
            'hour_3_main': hourly_data['hourly'][2]['weather'][0]['main'],
            'hour_4_temp': int(round(hourly_data['hourly'][3]['temp'], 0)),
            'hour_4_id': hourly_data['hourly'][3]['weather'][0]['id'],
            'hour_4_main': hourly_data['hourly'][3]['weather'][0]['main'],
            'hour_5_temp': int(round(hourly_data['hourly'][4]['temp'], 0)),
            'hour_5_id': hourly_data['hourly'][4]['weather'][0]['id'],
            'hour_5_main': hourly_data['hourly'][4]['weather'][0]['main'],
            'hour_6_temp': int(round(hourly_data['hourly'][5]['temp'], 0)),
            'hour_6_id': hourly_data['hourly'][5]['weather'][0]['id'],
            'hour_6_main': hourly_data['hourly'][5]['weather'][0]['main'],
            'hour_7_temp': int(round(hourly_data['hourly'][6]['temp'], 0)),
            'hour_7_id': hourly_data['hourly'][6]['weather'][0]['id'],
            'hour_7_main': hourly_data['hourly'][6]['weather'][0]['main'],
            'hour_8_temp': int(round(hourly_data['hourly'][7]['temp'], 0)),
            'hour_8_id': hourly_data['hourly'][7]['weather'][0]['id'],
            'hour_8_main': hourly_data['hourly'][7]['weather'][0]['main'],
            'hour_9_temp': int(round(hourly_data['hourly'][8]['temp'], 0)),
            'hour_9_id': hourly_data['hourly'][8]['weather'][0]['id'],
            'hour_9_main': hourly_data['hourly'][8]['weather'][0]['main'],
            'hour_10_temp': int(round(hourly_data['hourly'][9]['temp'], 0)),
            'hour_10_id': hourly_data['hourly'][9]['weather'][0]['id'],
            'hour_10_main': hourly_data['hourly'][9]['weather'][0]['main'],
            'hour_11_temp': int(round(hourly_data['hourly'][10]['temp'], 0)),
            'hour_11_id': hourly_data['hourly'][10]['weather'][0]['id'],
            'hour_11_main': hourly_data['hourly'][10]['weather'][0]['main'],
            'hour_12_temp': int(round(hourly_data['hourly'][11]['temp'], 0)),
            'hour_12_id': hourly_data['hourly'][11]['weather'][0]['id'],
            'hour_12_main': hourly_data['hourly'][11]['weather'][0]['main'],
            'hour_13': hourly_data['hourly'][12]['dt']
        }

        data_daily = {
            'day_1_temp': int(round(hourly_data['daily'][0]['temp']['day'], 0)),
            'day_1_max': int(round(hourly_data['daily'][0]['temp']['max'], 0)),
            'day_1_min': int(round(hourly_data['daily'][0]['temp']['min'], 0)),
            'day_1_main': hourly_data['daily'][0]['weather'][0]['main'],
            'day_1_id': hourly_data['daily'][0]['weather'][0]['id'],
            'day_2_temp': int(round(hourly_data['daily'][1]['temp']['day'], 0)),
            'day_2_max': int(round(hourly_data['daily'][1]['temp']['max'], 0)),
            'day_2_min': int(round(hourly_data['daily'][1]['temp']['min'], 0)),
            'day_2_main': hourly_data['daily'][1]['weather'][0]['main'],
            'day_2_id': hourly_data['daily'][1]['weather'][0]['id'],
            'day_3_temp': int(round(hourly_data['daily'][2]['temp']['day'], 0)),
            'day_3_max': int(round(hourly_data['daily'][2]['temp']['max'], 0)),
            'day_3_min': int(round(hourly_data['daily'][2]['temp']['min'], 0)),
            'day_3_main': hourly_data['daily'][2]['weather'][0]['main'],
            'day_3_id': hourly_data['daily'][2]['weather'][0]['id'],
            'day_4_temp': int(round(hourly_data['daily'][3]['temp']['day'], 0)),
            'day_4_max': int(round(hourly_data['daily'][3]['temp']['max'], 0)),
            'day_4_min': int(round(hourly_data['daily'][3]['temp']['min'], 0)),
            'day_4_main': hourly_data['daily'][3]['weather'][0]['main'],
            'day_4_id': hourly_data['daily'][3]['weather'][0]['id'],
            'day_5_temp': int(round(hourly_data['daily'][4]['temp']['day'], 0)),
            'day_5_max': int(round(hourly_data['daily'][4]['temp']['max'], 0)),
            'day_5_min': int(round(hourly_data['daily'][4]['temp']['min'], 0)),
            'day_5_main': hourly_data['daily'][4]['weather'][0]['main'],
            'day_5_id': hourly_data['daily'][4]['weather'][0]['id'],
            'day_6_temp': int(round(hourly_data['daily'][5]['temp']['day'], 0)),
            'day_6_max': int(round(hourly_data['daily'][5]['temp']['max'], 0)),
            'day_6_min': int(round(hourly_data['daily'][5]['temp']['min'], 0)),
            'day_6_main': hourly_data['daily'][5]['weather'][0]['main'],
            'day_6_id': hourly_data['daily'][5]['weather'][0]['id'],
            'day_7_temp': int(round(hourly_data['daily'][6]['temp']['day'], 0)),
            'day_7_max': int(round(hourly_data['daily'][6]['temp']['max'], 0)),
            'day_7_min': int(round(hourly_data['daily'][6]['temp']['min'], 0)),
            'day_7_main': hourly_data['daily'][6]['weather'][0]['main'],
            'day_7_id': hourly_data['daily'][6]['weather'][0]['id'],
            'day_8_temp': int(round(hourly_data['daily'][7]['temp']['day'], 0)),
            'day_8_max': int(round(hourly_data['daily'][7]['temp']['max'], 0)),
            'day_8_min': int(round(hourly_data['daily'][7]['temp']['min'], 0)),
            'day_8_main': hourly_data['daily'][7]['weather'][0]['main'],
            'day_8_id': hourly_data['daily'][7]['weather'][0]['id'],
            'uv': round(hourly_data['daily'][0]['uvi'])
        }

        # Got icon for each hour
        for i in range(1, 13):
            hourly_images.append(check_icon(data_hourly['hour_' + str(i) + '_id']))
            main_list.append(data_hourly['hour_' + str(i) + '_main'])

        for j in range(1, 9):
            daily_images.append(check_icon(data_daily['day_' + str(j) + '_id']))

        id_tag = data['id']
        image = check_icon(id_tag)

        return render_template('home.html', data=data, image=image, hourly_images=hourly_images,
                               data_hourly=data_hourly, data_daily=data_daily, daily_images=daily_images,
                               days=list_of_days, sun_time=sun_time, list_of_hours=list_of_hours,
                               list_of_months=list_of_months, lat=lat, lon=lon, alerts_data=alerts_data,
                               alerts_image=alerts_image, new_des=ref_description, pop_list=pop_list)


if __name__ == '__main__':
    app.run(debug=True)
