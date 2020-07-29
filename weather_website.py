import json
import urllib.request
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def weather():
    if request.method == 'POST':
        city = request.form['city'].title()
    else:
        # for default name mathura 
        city = 'Plainsboro'

    # your API key will come here 
    api = '8a5edfd4d0e0f8953dbe82364cfc0b10'

    # source contain json data from api 
    source = urllib.request.urlopen(
        'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api).read()

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
        "temp_max": int(round(1.8 * (list_of_data['main']['temp_max'] - 273)+32, 0)),
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
        "wind_speed": list_of_data['wind']['speed'],
        'id': list_of_data['weather'][0]['id']
    }

    print(list_of_data)

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
