import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from restaurants import restaurants
from restaurant_details import restaurant_details

class restaurant_list:
    def __init__(self,headers,city):
        self.city = city.split(" ")
        self.restaurant_list = []
        self.locality = []
        self.url = "https://www.zomato.com/{}/".format("-".join(self.city).lower())
        self.headers = headers
        
    def execute(self):
        r = requests.get(self.url,headers=self.headers)

        soup = BeautifulSoup(r.content,'lxml')
        locations = soup.find_all('h5',class_ = 'sc-1uh2q3e-0')
        
        for area in locations:
            place = area.text.split(" (")[0]
            self.locality.append(place)
        
        # Creating a browser instance
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        for i in range(len(self.locality)):
            obj = restaurants(self.locality[i],self.city)
            self.restaurant_list += obj.getlist(driver)
        
        self.restaurant_list = [i for n,i in enumerate(self.restaurant_list) if i not in self.restaurant_list[n+1:]]

        length = len(self.restaurant_list)
        for i in range(length):
            for key in self.restaurant_list[i].keys():
                details = restaurant_details(self.restaurant_list[i][key])
                details.attributes(driver=driver)
                self.restaurant_list[i][key] = {
                    "Address": details.address,
                    "Cost For Two": details.cost_for_two,
                    "Cuisines": details.cuisines,
                    "Link to Menu": details.menu,
                    "Dining Rating": details.dining_rating,
                    "Delivery Rating": details.delivery_rating
                }

        driver.quit()
        json_object = json.dumps(self.restaurant_list,indent = 4)
        with open("result.json","w") as f:
            f.write(json_object)

if __name__ == "__main__":
    city_name = input("Enter city name\n")
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    }
    restro_detail = restaurant_list(headers = headers,city = city_name)

    restro_detail.execute()
    print(len(restro_detail.restaurant_list))