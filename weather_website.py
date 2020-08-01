# Import Statements
import json
import time
import urllib.request
from flask import Flask, render_template, request

# App
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def weather():
    if request.method == 'POST':
        city = request.form['city'].title()
    else:
        # for default name mathura 
        city = 'Plainsboro'

    new_city = city

    if ' ' in city:
        print('space')
        new_city = city.replace(' ', '+')

    # your API key will come here 
    api = '8a5edfd4d0e0f8953dbe82364cfc0b10'

    # source contain json data from api 
    source = urllib.request.urlopen(
        'http://api.openweathermap.org/data/2.5/weather?q=' + new_city + '&appid=' + api).read()

    # converting JSON data to a dictionary 
    list_of_data = json.loads(source)

    # data for variable list_of_data 
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
        'sunset': list_of_data['sys']['sunset']
    }

    print(list_of_data)

    id_tag = data['id']
    id_tag_str = str(id_tag)

    if id_tag == 800:
        image = 'dayclear.png'

    elif id_tag_str[0] == '2':
        image = 'lightning.png'

    elif id_tag_str[0] == '3':
        image = 'rain.png'

    elif id_tag_str[0] == '5' and id_tag_str[1] == '0' or id_tag_str[1] == '1':
        image = 'partlyrain.png'

    elif id_tag_str[0] == '5' and id_tag_str[1] == '2':
        image = 'rain.png'

    elif id_tag == 531:
        image = 'rain.png'

    elif id_tag_str[0] == '6':
        image = 'snow.png'

    elif id_tag_str[0] == '7':
        image = 'atmosphere.png'

    elif id_tag == 801:
        image = 'dayclouds.png'

    elif id_tag == 802:
        image = 'scatteredclouds.png'

    elif id_tag == 803 or 804:
        image = 'brokenclouds.png'

    sunrise = time.localtime(data['sunrise'])
    sunset = time.localtime(data['sunset'])

    # print('sunrise', sunrise.tm_hour, sunrise.tm_min)
    # print('sunset', sunset.tm_hour, sunset.tm_min)
    sunset_min = sunset.tm_min

    if len(str(sunset_min)) == 1:
        sunset_min = str(0) + str(sunset_min)

    return render_template('index.html', data=data, image=image, sunrise=sunrise, sunset=sunset, sunset_min=sunset_min)


if __name__ == '__main__':
    app.run(debug=True)
