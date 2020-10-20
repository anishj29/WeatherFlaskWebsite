def convert_to_c(dataF, dataFH, dataFD):
    c_dict = {'c_temp': dataF['temp'], 'c_temp_min': dataF['temp_min'], 'c_temp_max': dataF['temp_max'],
              'c_hour_1_temp': dataFH['hour_1_temp'], 'c_hour_2_temp': dataFH['hour_2_temp'],
              'c_hour_3_temp': dataFH['hour_3_temp'], 'c_hour_4_temp': dataFH['hour_4_temp'],
              'c_hour_5_temp': dataFH['hour_5_temp'], 'c_hour_6_temp': dataFH['hour_6_temp'],
              'c_hour_7_temp': dataFH['hour_7_temp'], 'c_hour_8_temp': dataFH['hour_8_temp'],
              'c_hour_9_temp': dataFH['hour_9_temp'], 'c_hour_10_temp': dataFH['hour_10_temp'],
              'c_hour_11_temp': dataFH['hour_11_temp'], 'c_hour_12_temp': dataFH['hour_12_temp'],
              'c_day_1_temp': dataFD['day_1_temp'], 'c_day_2_temp': dataFD['day_2_temp'],
              'c_day_3_temp': dataFD['day_3_temp'], 'c_day_4_temp': dataFD['day_4_temp'],
              'c_day_5_temp': dataFD['day_5_temp'], 'c_day_6_temp': dataFD['day_6_temp'],
              'c_day_7_temp': dataFD['day_7_temp'], 'c_day_1_max': dataFD['day_1_max'],
              'c_day_2_max': dataFD['day_2_max'], 'c_day_3_max': dataFD['day_3_max'],
              'c_day_4_max': dataFD['day_4_max'], 'c_day_5_max': dataFD['day_5_max'],
              'c_day_6_max': dataFD['day_6_max'], 'c_day_7_max': dataFD['day_7_max'],
              'c_day_8_max': dataFD['day_8_max'], 'c_day_1_min': dataFD['day_1_min'],
              'c_day_2_min': dataFD['day_2_min'], 'c_day_3_min': dataFD['day_3_min'],
              'c_day_4_min': dataFD['day_4_min'], 'c_day_5_min': dataFD['day_5_min'],
              'c_day_6_min': dataFD['day_6_min'], 'c_day_7_min': dataFD['day_7_min']}

    for key, temp in c_dict.values():
        c_dict[key] = round((temp - 32) * 5 / 9)
