from urllib.request import urlopen

import requests


class Take_info():
    def __init__(self):
        self.url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
        self.id = None
        self.payload = None
        self.headers = {
            "content-type": "application/json",
            # 45d2bcb1e8msh203e7eea9164163p156373jsncd8ddf16b0bc
            # 2b6ae294e3msh7dadcd29aa3eab5p1f13e4jsn47fbbecb8105
            "X-RapidAPI-Key": "45d2bcb1e8msh203e7eea9164163p156373jsncd8ddf16b0bc",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        self.response = None

    def setter_payload_response(self, hotel_id):
        self.payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": str(hotel_id)
        }
        self.response = requests.request("POST", self.url, json=self.payload, headers=self.headers).json()
        return self.response

    def get_photos(self, response, count_of_photo):
        list_of_photo = []
        get_photo_list = response['data']['propertyInfo']['propertyGallery']['images']
        iters = len(get_photo_list)
        if iters >= count_of_photo:
            iters = count_of_photo
        for photo_list in get_photo_list:
            if iters != 0:
                list_of_photo.append(photo_list['image']['url'])
                iters -= 1
            else:
                break
        return list_of_photo

    def publish_photo(self, list_photo):
        for url in list_photo:
            img = urlopen(url).read()
            yield img


if __name__ == "__main__":
    count_for_write = 20
    info = Take_info()
    g = info.setter_payload_response(996214)
    list_photo = info.get_photos(g, count_for_write)
    p = info.publish_photo(list_photo)
