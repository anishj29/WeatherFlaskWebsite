def convert_to_c(dataF, dataFH, dataFD):
    c_dict_M = {}
    c_dict_H = {}
    c_dict_D = {}

    c_dict_M['temp'] = int(round((dataF['temp'] - 32) * 5 / 9))
    c_dict_M['temp_min'] = int(round((dataF['temp_min'] - 32) * 5 / 9))
    c_dict_M['temp_max'] = int(round((dataF['temp_max'] - 32) * 5 / 9))
    c_dict_M['feels_like'] = int(round((dataF['feels_like'] - 32) * 5 / 9))
    c_dict_M["country_code"] = dataF["country_code"]
    c_dict_M["city_name"] = dataF["city_name"]
    c_dict_M["main"] = dataF["main"]
    c_dict_M['description'] = dataF['description']
    c_dict_M['coordinate'] = dataF['coordinate']
    c_dict_M['humidity'] = dataF['humidity']
    c_dict_M['wind_speed'] = dataF['wind_speed']
    c_dict_M['id'] = dataF['id']
    c_dict_M['sunrise'] = dataF['sunrise']
    c_dict_M['sunset'] = dataF['sunset']
    c_dict_M['offset'] = dataF['offset']

    for i in range(1, 13):  # hourly data
        x = str(i)
        c_dict_H['hour_' + x + '_temp'] = int(round((dataFH['hour_' + x + '_temp'] - 32) * 5 / 9))
        c_dict_H['hour_' + x + '_main'] = dataFH['hour_' + x + '_main']
        c_dict_H['hour_' + x + '_id'] = dataFH['hour_' + x + '_id']

    c_dict_H['feels_like'] = dataFH['feels_like']

    for i in range(1, 8):  # Daily data
        x = str(i)
        c_dict_D['day_' + str(x) + '_temp'] = int(round((dataFD['day_' + str(x) + '_temp'] - 32) * 5 / 9))
        c_dict_D['day_' + str(x) + '_max'] = int(round((dataFD['day_' + str(x) + '_max'] - 32) * 5 / 9))
        c_dict_D['day_' + str(x) + '_min'] = int(round((dataFD['day_' + str(x) + '_min'] - 32) * 5 / 9))
        c_dict_D['day_' + str(x) + '_id'] = dataFD['day_' + str(x) + '_id']
        c_dict_D['day_' + str(x) + '_main'] = dataFD['day_' + str(x) + '_main']

    c_dict_D['uv'] = dataFD['uv']  # Extra daily data

    return c_dict_M, c_dict_H, c_dict_D
