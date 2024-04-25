import requests


class City_id():

    def __init__(self):
        self.url = "https://hotels4.p.rapidapi.com/locations/v3/search"

        self.headers = {
            "X-RapidAPI-Key": "45d2bcb1e8msh203e7eea9164163p156373jsncd8ddf16b0bc",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

    def setter(self, city):
        self.city = city
        self.querystring = {"q": self.city, "locale": "en_US", "langid": "1033", "siteid": "300000001"}

    def response(self):
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring).json()
        return response

    def take_id_city(self, data):
        return data['sr'][0]['gaiaId']


if __name__ == "__main__":
    cl = City_id()
    cl.setter("Nha Trang".lower())
    response = cl.response()
    print(response)
    c = cl.take_id_city(response)
    print(c)
