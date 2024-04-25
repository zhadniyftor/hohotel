import requests

import Take_city_Module as tcm


class Take_info():
    def __init__(self):
        self.url = "https://hotels4.p.rapidapi.com/properties/v2/list"
        self.take_city = tcm.City_id()
        self.response = None
        self.city_id = None
        ######################
        self.status = "PRICE_LOW_TO_HIGH"
        ######################
        self.max_Size = 200
        ######################
        self.max = None
        self.min = None
        ######################
        self.adults = None
        self.list_children = []
        #####################
        self.day_in = None
        self.month_in = None
        self.year_in = None
        #####################
        self.day_out = None
        self.month_out = None
        self.year_out = None
        #####################
        self.headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "45d2bcb1e8msh203e7eea9164163p156373jsncd8ddf16b0bc",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        #######################
        self.payload = None
        #######################
        self.responce = None

    def city(self, city):
        self.take_city.setter(city)
        self.response = self.take_city.response()
        self.city_id = self.take_city.take_id_city(self.response)

    def setter_data_in(self, datain):
        datalist = datain.split(".")
        if datalist[0].startswith('0'):
            self.day_in = int(datalist[0][1])
        else:
            self.day_in = int(datalist[0])

        if datalist[1].startswith('0'):
            self.month_in = int(datalist[1][1])
        else:
            self.month_in = int(datalist[1])
        self.year_in = int(datalist[2])

    def setter_data_out(self, data_time_out):
        datalist = data_time_out.split(".")
        self.day_out = int(datalist[0])
        self.month_out = int(datalist[1])
        self.year_out = int(datalist[2])

    def setter_adult(self, adults):
        self.adults = adults

    def setter_children(self, list_of_ages):
        try:
            self.list_children = [{"age": int(child_age)} for child_age in list_of_ages]
        except:
            self.list_children = []

    def price_max_min(self, maxSum, minSum):
        self.max = maxSum
        self.min = minSum

    def max_Sizes(self, maxSize):
        self.max_Size = maxSize

    def stat(self, choice):
        if choice == '/highprice':
            self.status = "DISTANCE"
        else:
            self.status = "PRICE_LOW_TO_HIGH"

    def payloads(self):
        self.payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "destination": {"regionId": self.city_id},
            "checkInDate": {
                "day": self.day_in,
                "month": self.month_in,
                "year": self.year_in
            },
            "checkOutDate": {
                "day": self.day_out,
                "month": self.month_out,
                "year": self.year_out
            },
            "rooms": [
                {
                    "adults": self.adults,
                    "children": self.list_children
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": self.max_Size,
            "sort": self.status,
            "filters": {"price": {
                "max": self.max,
                "min": self.min
            }}
        }
        # print(self.payload)

    def responces(self):
        self.response = requests.request("POST", self.url, json=self.payload, headers=self.headers).json()
        return self.response

    def get_properties(self):
        info = self.response['data']['propertySearch']['properties']
        return info

    def get_id_name_of_hotel(self, datas):
        id_hotel = datas["id"]
        name_hotel = datas["name"]
        distanse_for_center = round(float(datas['destinationInfo']['distanceFromDestination']["value"]) / 0.62137)
        return (id_hotel, name_hotel, distanse_for_center)

    def get_distance_to_center(self, datas):
        distance = datas['destinationInfo']['distanceFromDestination']['value'] / 0.62137
        return round(distance, 3)

    def get_summary(self, datas):
        print(datas)
        price = datas['price']['options'][0]['formattedDisplayPrice']
        return price


if __name__ == "__main__":
    info = Take_info()
    # city = input("Введите город ").lower()
    city = "Las Vegas".lower()
    info.city(city)
    # datatimein = input("Введите дату въезда (например: 01.01.1111) ")
    datatimein = '10.11.2023'
    info.setter_data_in(datatimein)
    # datatimeout = input("Введите дату выезда (например: 01.01.1111) ")
    datatimeout = "15.11.2023"
    info.setter_data_out(datatimeout)
    # adults = int(input("Сколько будет взрослых? "))
    adults = 2
    info.setter_adult(adults)
    # answer = input("Будут ли дети(Да/Нет)")
    # if answer.lower() == "да":
    #    info.setter_children()
    # maxSum = int(input("Введите максимальную сумму... "))
    # minSum = int(input("Введите минимальную сумму... "))
    maxSum = 99999999999
    minSum = 1
    info.price_max_min(maxSum, minSum)
    # maxSize = int(input("Максимум отелей? "))
    info.stat(choice="/highprice")
    info.max_Sizes(200)
    info.payloads()
    info.responces()
    nes_list = list(info.get_properties())

    try:
        for n in nes_list:
            print(n)
            info.get_id_name_of_hotel(n)
            print(info.get_distance_to_center(n))
            print(info.get_summary(n))
    except:
        print("Нету подходящих отелей")
    print(len(nes_list))

# New York
# 2
# 2
# 300
# 100
# 10.05.2023
# 15.05.2023
