from selenium.webdriver.common.by import By
import time

class restaurant_details:
    def __init__(self,url):
        self.url = url.replace("/order","")
        self.dining_rating = 0.0
        self.delivery_rating = 0.0
        self.address = ""
        self.cost_for_two = 0.0
        self.menu = ""
        self.cuisines = []

    def attributes(self,driver):
        
        driver.get(self.url)
        driver.implicitly_wait(10)

        last_height = 0
        update_value = 1000
        end_height = 1000
        for _ in range(2):
            driver.execute_script("window.scrollTo({},{});".format(last_height,end_height))
            time.sleep(3)
            last_height += update_value
            end_height += update_value
    
        address_element = driver.find_elements(By.CSS_SELECTOR, ".sc-1hez2tp-0.clKRrC")
        for i in address_element:
            if i.get_attribute('color') == "#1C1C1C":
                self.address = i.text
                break

        self.dining_rating = driver.find_elements(By.CSS_SELECTOR,".sc-1q7bklc-1")[0].text
        self.delivery_rating = driver.find_elements(By.CSS_SELECTOR,".sc-1q7bklc-1")[1].text
        
        categories = driver.find_elements(By.TAG_NAME,"a")
        for category in categories:
            if category.get_attribute('rel') == "noopener noreferrer":
                if category.text == "OpenStreetMap":
                    break
                elif category.text != "Direction":
                    self.cuisines.append(category.text)
        
        temp = driver.find_elements(By.CSS_SELECTOR,".sc-1hez2tp-0")
        for i in temp:
            if "₹" in i.text:
                self.cost_for_two = i.text.split(" ")[0][1:]
                break

        menu = driver.find_elements(By.CSS_SELECTOR,".sc-s1isp7-5")

        for item in menu:
            if "Menu menu" in item.get_attribute("alt"):
                self.menu = item.get_attribute("src")
        
        
if __name__ == '__main__':
    pass     