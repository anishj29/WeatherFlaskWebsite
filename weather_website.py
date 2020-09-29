
import datetime
import json
import urllib.request

import datetimerange
import ephem
import pytz
from flask import Flask, render_template, request
from flask_compress import Compress
from googletrans import Translator

import send_email
from run_sql import MySQL

hourly_images = []
daily_images = []
id_list = []
main_list = []
alerts_image = ''
pop_list = ''
city = ''
email = ''
lat = 0
lon = 0
data_daily = {'day_1_temp': 0, 'day_1_main': 'Clear'}

day_name = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
time_range = datetimerange.DateTimeRange("T5:00:00+0900", "T9:00:00+0900")


# def auto_complete(city_typed):
#     try:
#         items_auto = ['http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey='
#                       '4zrGVjvJENvvA6SvIPA6hW1qUmtKqCcd&q=', city_typed]
#         corrections = json.loads(urllib.request.urlopen(''.join(items_auto)).read())
#
#         city_list = []
#         for i in range(5):
#             city_list.append(corrections[i]['LocalizedName'])
#
#         city_list = [corrections[0]['LocalizedName'], corrections[1]['LocalizedName'], corrections[2]['LocalizedName']
#                      ,corrections[3]['LocalizedName'], corrections[4]['LocalizedName']]
#
#         print(city_list)
#
#     except urllib.error.HTTPError:
#         city_list = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A']
#
#     return city_list


def send_emails_web():
    if str(datetime.datetime.today().hour) + ":00:00+0900" in time_range:
        global data_daily
        msg = "Hello, \nToday is " + data_daily['day_1_main'].lower()
        database = MySQL()
        all_emails = database.get_all()
        database.close()
        for row in all_emails:
            send_email.send_mail(row[0], row[1], msg, data_daily['day_1_temp'], description + description_2, False)


def verify_icon(id_tag, it_is_day):
    id_tag_str = str(id_tag)
    id_list.append(id_tag)

    if id_tag in (200, 201, 202, 230, 231, 232):
        return 'static/icons/icon-11.svg'

    elif id_tag in (210, 211, 212, 221):
        return 'static/icons/icon-12.svg'

    elif id_tag_str[0] == '3':
        return 'static/icons/light_rain.svg'

    elif id_tag in (511, 520, 521, 522, 531):
        return 'static/icons/heavy_rain.svg'

    elif id_tag_str[0] == '6':
        return 'static/icons/icon-13.svg '

    elif id_tag_str[0] == '7':
        return 'static/icons/fog_2.svg'

    elif id_tag == 802:
        return 'static/icons/cloudy.svg'

    elif id_tag == 803:
        return 'static/icons/icon-6.svg'
    elif id_tag in (803, 804):
        return 'static/icons/icon-6.svg'

    if it_is_day:
        if id_tag == 800:
            return 'static/icons/sunny.svg'
        elif id_tag == 801:
            return 'static/icons/cloudy&sunny.svg'
        elif id_tag in (500, 501, 502, 503, 504):
            return 'static/icons/rain&sunny.svg'

    else:
        if id_tag == 800:
            return 'static/icons/clear_moon.png'
        elif id_tag == 801:
            return 'static/icons/clouds_moon.png'
        elif id_tag in (500, 501, 502, 503, 504):
            return 'static/icons/rain_moon.png'

    return 'error'


app = Flask(__name__)
COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500
Compress(app)

alerts_data = {}
description = ''
description_2 = ''
second_alert = False


@app.route('/', methods=['POST', 'GET'])
def weather():
    # global alerts_image, description, description_2, second_alert, alerts_data, pop_list, day_name, city, data_daily
    global alerts_data, city, alerts_image, second_alert
    city = 'princeton'
    if request.method == 'POST':
        city = request.form['city'].title()
    else:
        geoip = urllib.request.urlopen(
            'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=at_7PwbMzdUGTjddKi5dhSUlOrzUEHhF&ipAddress').read()
        geo = json.loads(geoip)
        city = geo['location']['city']
        # state = geo['location']['region']

    new_city = city
    if ' ' in city:
        new_city = city.replace(' ', '+')

    # source contain json data from api
    try:
        items = ['http://api.openweathermap.org/data/2.5/weather?q=', new_city,
                 '&appid=8a5edfd4d0e0f8953dbe82364cfc0b10']
        source = urllib.request.urlopen(''.join(items)).read()

        list_of_data = json.loads(source)

    except urllib.error.HTTPError:
        return render_template("404.html")

    data = {
        "country_code": str(list_of_data['sys']['country']), "city_name": str(city),
        "main": list_of_data['weather'][0]['main'], "description": list_of_data['weather'][0]['description'],
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "temp": int(round(1.8 * (list_of_data['main']['temp'] - 273) + 32, 0)),
        "temp_min": int(round(1.8 * (list_of_data['main']['temp_min'] - 273) + 32, 0)),
        "temp_max": int(round(1.8 * (list_of_data['main']['temp_max'] - 273) + 32, 0)),
        "feels_like": int(round(1.8 * (list_of_data['main']['feels_like'] - 273) + 32, 0)),
        "humidity": str(list_of_data['main']['humidity']), "wind_speed": list_of_data['wind']['speed'],
        'id': list_of_data['weather'][0]['id'], 'sunrise': list_of_data['sys']['sunrise'],
        'sunset': list_of_data['sys']['sunset'], 'offset': list_of_data['timezone']
    }
    lat = str(list_of_data['coord']['lat'])
    lon = str(list_of_data['coord']['lon'])
    temp = 'imperial'

    # Sunrise and Sunset
    sunrise_time = data['sunrise'] + data['offset']
    sunset_time = data['sunset'] + data['offset']

    sunrise = datetime.datetime.fromtimestamp(sunrise_time, datetime.timezone.utc).strftime('%I:%M %p')
    sunset = datetime.datetime.fromtimestamp(sunset_time, datetime.timezone.utc).strftime('%I:%M %p')
    sun_time = [sunrise, sunset]

    items_hourly = ['https://api.openweathermap.org/data/2.5/onecall?lat=', lat, '&lon=', lon, '&units=', temp,
                    '&exclude=minutely,current&appid=8a5edfd4d0e0f8953dbe82364cfc0b10']
    # Hourly Weather
    hourly_source = urllib.request.urlopen(''.join(items_hourly)).read()
    hourly_data = json.loads(hourly_source)

    # Gets accurate hour, day and month for searched location
    tz = hourly_data['timezone']
    datetime_tz = datetime.datetime.now(pytz.timezone(tz))
    today_date = datetime_tz.day
    day = datetime_tz.today().weekday()

    # Gets day in number
    day_2 = (datetime_tz + datetime.timedelta(days=1)).weekday()
    day_3 = (datetime_tz + datetime.timedelta(days=2)).weekday()
    day_4 = (datetime_tz + datetime.timedelta(days=3)).weekday()
    day_5 = (datetime_tz + datetime.timedelta(days=4)).weekday()
    day_6 = (datetime_tz + datetime.timedelta(days=5)).weekday()
    day_7 = (datetime_tz + datetime.timedelta(days=6)).weekday()

    list_of_days = [day, day_2, day_3, day_4, day_5, day_6, day_7]

    for i, val in enumerate(list_of_days):  # Converts number to day ( 1 = Monday 2 = Tuesday etc)
        list_of_days[i] = day_name[list_of_days[i]]

    month_name = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'June', 7: 'July', 8: 'Aug',
                  9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    current_month = datetime_tz.month
    current_month = month_name[current_month]
    current_hour = int(datetime_tz.strftime("%H"))

    # Gets hour in 12 hour format (am/pm)
    list_of_hours = [current_hour, current_hour + 1, current_hour + 2, current_hour + 3, current_hour + 4,
                     current_hour + 5, current_hour + 6]

    for i, val in enumerate(list_of_hours):
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
        pop_list = []
        items_pop = ['http://dataservice.accuweather.com/locations/v1/cities/search?apikey='
                     '4zrGVjvJENvvA6SvIPA6hW1qUmtKqCcd&q=', new_city.lower(), '&details=false']
        get_id = urllib.request.urlopen(''.join(items_pop)).read()
    except:
        pop_list = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']

    else:
        city_id = json.loads(get_id)
        key = city_id[0]["Key"]

        get_pop = urllib.request.urlopen('http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' + key +
                                         '?apikey=4zrGVjvJENvvA6SvIPA6hW1qUmtKqCcd&details=false').read()
        pop_info = json.loads(get_pop)

        for i in range(0, 8):
            pop_num = pop_info[i]['PrecipitationProbability']
            pop_num = str(int(round(pop_num + 0.1, -1))) + '%'
            if pop_num == '0%':
                pop_num = ''
            pop_list.append(pop_num)

    item_alerts = ['https://api.weatherbit.io/v2.0/alerts?lat=', lat, '&lon=', lon, '&key=',
                   '888c4677014d4578a511570492df67b0']
    # alerts_key = '888c4677014d4578a511570492df67b0'
    alerts_api = urllib.request.urlopen(''.join(item_alerts)).read()
    alerts_store = json.loads(alerts_api)

    try:
        alerts_data = {
            'expires': alerts_store['alerts'][0]['expires_utc'],
            'effective': alerts_store['alerts'][0]['effective_local'],
            'description': alerts_store['alerts'][0]['description'],
            'effective_utc': alerts_store['alerts'][0]['effective_utc'],
            'severity': alerts_store['alerts'][0]['severity'],
            'title': alerts_store['alerts'][0]['title'], 'local_expire': alerts_store['alerts'][0]['expires_local']
        }

    except IndexError:
        alerts_description = 'No alerts in this area!'

    else:
        translator = Translator()
        alerts_description = translator.translate(alerts_data['description'])
        alerts_description = alerts_description.text.replace('English: ', '')
        alerts_description = alerts_description.replace('* WHAT...', 'What: ')
        alerts_description = alerts_description.replace('* WHERE...', 'Where: ')
        alerts_description = alerts_description.replace('* WHEN...', 'When: ')
        alerts_description = alerts_description.replace('* IMPACTS...', 'Impacts: ')

        severity = alerts_data['severity']
        if severity == 'Warning':
            alerts_image = 'static/alerts/warning.png'

        elif severity == 'Watch':
            alerts_image = 'static/alerts/watch.png'

        elif severity == 'Extreme':
            alerts_image = 'static/alerts/extreme.png'

        elif severity == 'Advisory':
            alerts_image = 'static/alerts/advisory.png'

        else:
            alerts_image = 'static/weather_icon-2.co'

        try:
            alerts_data_2 = {
                'expires': alerts_store['alerts'][1]['expires_utc'],
                'effective': alerts_store['alerts'][1]['effective_local'],
                'description': alerts_store['alerts'][1]['description'],
                'effective_utc': alerts_store['alerts'][1]['effective_utc'],
                'severity': alerts_store['alerts'][1]['severity'],
                'title': alerts_store['alerts'][1]['title'],
                'local_expire': alerts_store['alerts'][1]['expires_local']
            }
            second_alert = True

        except IndexError:
            second_alert = False

        else:
            alerts_description_2 = translator.translate(alerts_data_2['description'])
            alerts_description_2 = alerts_description_2.text.replace('English: ', '')
            alerts_description_2 = alerts_description_2.replace('* WHAT...', 'What: ')
            alerts_description_2 = alerts_description_2.replace('* WHERE...', 'Where: ')
            alerts_description_2 = alerts_description_2.replace('* WHEN...', 'When: ')
            alerts_description_2 = alerts_description_2.replace('* IMPACTS...', 'Impacts: ')

    # Hourly Weather stored in dictionary
    data_hourly = {
        'feels_like': int(round(hourly_data['hourly'][0]['feels_like'], 0)),
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
    # Daily weather
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

    if data_hourly['hour_1_main'] == 'Clear':
        # bg_images = 'https://cdn.lynda.com/course/438407/438407-637286184088314228-16x9.jpg'
        bg_images = 'https://res.cloudinary.com/program-explorers/image/upload/v1600480831/Grand-Canyon-Destination' \
                    '-Page_mp557z.jpg '
    elif data_hourly['hour_1_main'] == 'Rain':
        bg_images = 'https://res.cloudinary.com/program-explorers/image/upload/v1600480866/2z1a5tixad121_ahwtn0.jpg'
    elif data_hourly['hour_1_main'] == 'Clouds':
        bg_images = 'https://res.cloudinary.com/program-explorers/image/upload/v1600480909' \
                    '/aAujKcEpiVcrqCCut2biNnG63S5fcwhRYcIb81Z0UnQ_yqq8iy.jpg '
    elif data_hourly['hour_1_main'] == 'Snow':
        bg_images = 'https://res.cloudinary.com/program-explorers/image/upload/v1600480952/GC_Winter_oan3zl.jpg'
    else:
        bg_images = 'https://res.cloudinary.com/program-explorers/image/upload/v1600480973/grand-canyon-sunset_c6yvay' \
                    '.jpg '

    user = ephem.Observer()
    user.lat = lat
    user.lon = lon
    next_sunrise_datetime = user.next_rising(ephem.Sun()).datetime()
    next_sunset_datetime = user.next_setting(ephem.Sun()).datetime()
    it_is_day = next_sunset_datetime < next_sunrise_datetime
    # Got icon for each hour
    for i in range(1, 13):
        hourly_images.append(verify_icon(data_hourly['hour_' + str(i) + '_id'], it_is_day))
        main_list.append(data_hourly['hour_' + str(i) + '_main'])
    for j in range(1, 9):
        daily_images.append(verify_icon(data_daily['day_' + str(j) + '_id'], True))

    id_tag = data['id']
    image = verify_icon(id_tag, it_is_day)

    send_emails_web()

    return render_template('home.html', data=data, image=image, hourly_images=hourly_images,
                           data_hourly=data_hourly, data_daily=data_daily, daily_images=daily_images,
                           days=list_of_days, sun_time=sun_time, list_of_hours=list_of_hours,
                           current_month=current_month, lat=lat, lon=lon, alerts_data=alerts_data,
                           alerts_image=alerts_image, new_des=alerts_description, pop_list=pop_list,
                           todays_date=today_date, bg_images=bg_images)


@app.route('/subscribe/', methods=['POST', 'GET'])
def send_mail():
    global description, description_2, second_alert, data_daily, city, email
    email = request.form['subscribe']
    message = "Please confirm the information below, or edit"
    message2 = ""

    return render_template("subscribe.html", message=message, message2=message2, email=email, city=city)


@app.route('/subscribe/edit', methods=['POST', 'GET'])
def edit():
    return render_template('edit.html')


@app.route('/subscribe/done', methods=['POST', 'GET'])
def update_mail_loc():
    global email, city, data_daily
    msg = "Thank you for subscribing to Weather Website by Program Explorers!"
    alerts_email = description + description_2

    try:
        email = request.form['update_email']
        city = request.form['update_location']
    except:
        pass

    is_email_sent = send_email.send_mail(email, city, msg, data_daily['day_1_temp'], alerts_email, True)

    if is_email_sent:
        message = "Thank You For Subscribing!"

    else:
        message = 'Invalid email try again'

    data_base = MySQL()
    data_base.insert(email=email, location=city)
    data_base.commit()
    data_base.close()

    return render_template('done.html', message=message)


@app.route('/alerts')
def alerts():
    global description, description_2, second_alert, city
    return render_template('alerts.html', des=description, des2=description_2, second_alert=second_alert, city=city)


if __name__ == '__main__':
    app.run(debug=True)
