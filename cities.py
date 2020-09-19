import json

# city_list = []


def get_cities():
    with open("countries.json", "r") as read_file:
        data = json.load(read_file)
    # print(data["United States"][ in data["United States"])
    #
    # for country in countries:
    #     for i in range(0, len(data[country])):
            # city_list.append(data[country][i])

    return [1, 2, 3, 4, 5]  # Return 5 desired cities for the search bar to show


get_cities()
