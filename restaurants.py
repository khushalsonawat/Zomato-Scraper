from selenium.webdriver.common.by import By
import time

class restaurants:
    def __init__(self,area,city):
        self.area = area.split(" ")
        self.city = city.split(" ")
        self.restaurant_list = []
        self.url = "https://zomato.com/{}/{}-restaurants/".format("-".join(self.city).lower(),"-".join(self.area).lower())

    def getlist(self,driver):
        driver.get(self.url)
        driver.implicitly_wait(10)
        last_height = 0
        update_value = 1000
        end_height = 1000
        n = driver.execute_script("return document.body.scrollHeight")//1000
        i = 1
        while True:
            driver.execute_script("window.scrollTo({},{});".format(last_height,end_height))
            time.sleep(3)
            last_height += update_value
            end_height += update_value
            n = driver.execute_script("return document.body.scrollHeight")//1000
            if i == n-1:
                break
            i += 1
            
        element = driver.find_elements(By.CSS_SELECTOR, ".sc-hdPSEv")

        for item in element:
            try:
                self.restaurant_list.append({item.find_element(By.CSS_SELECTOR,".sc-1hp8d8a-0").text : item.get_attribute('href')})
            except:
                pass    

        return self.restaurant_list


if __name__ == '__main__':
    pass     