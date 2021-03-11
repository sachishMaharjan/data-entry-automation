from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from time import sleep

GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSfnpmbHV2AxxW-I8oQVj1DGNhA_7t_vfPjSVYrvqJMDGIokCw/viewform?usp=sf_link"
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState={%22pagination%22:{},%22mapBounds%22:{%22west%22:-122.55177535009766,%22east%22:-122.31488264990234,%22south%22:37.73932632963956,%22north%22:37.81123909008061},%22mapZoom%22:12,%22isMapVisible%22:true,%22filterState%22:{%22price%22:{%22max%22:872627},%22beds%22:{%22min%22:1},%22pmf%22:{%22value%22:false},%22fore%22:{%22value%22:false},%22mp%22:{%22max%22:3000},%22auc%22:{%22value%22:false},%22nc%22:{%22value%22:false},%22fr%22:{%22value%22:true},%22fsbo%22:{%22value%22:false},%22cmsn%22:{%22value%22:false},%22pf%22:{%22value%22:false},%22fsba%22:{%22value%22:false}},%22isListVisible%22:true}"
CHROME_WEB_DRIVER = "/Users/sash/Documents/App-Brewery/Resources/chrome-webdriver/chromedriver"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


class Property:

    def __init__(self):
        self.response = requests.get(url=ZILLOW_LINK, headers=headers)
        website_html = self.response.text

        self.soup = BeautifulSoup(website_html, "html.parser")

    def get_links(self):
        """
        This function returns the links from the scraped website
        :return: list of links for the homes
        """
        links = self.soup.find_all(name="a", class_="list-card-link list-card-link-top-margin")
        home_links = [link['href'] for link in links]

        # Some of the links from the website are broken so this fixes it
        for index in range(len(home_links)):
            if not home_links[index].startswith("https"):
                home_links[index] = "https://www.zillow.com/"+ home_links[index]

        return home_links

    def get_prices(self):
        """
        This function returns all the prices from the scraped website
        :return: all the prices for the homes
        """
        prices = self.soup.find_all(name="div", class_="list-card-price")
        home_prices = [price.text for price in prices]

        return home_prices

    def get_address(self):
        """
        This function returns address of the house from the website
        :return: all the address for the houses
        """
        address = self.soup.find_all(name="address", class_="list-card-addr")
        home_address = [address.text for address in address]

        return home_address


house = Property()
house_links = house.get_links()
house_prices = house.get_prices()
house_address = house.get_address()

for index in range(len(house_links)):
    driver = webdriver.Chrome(executable_path=CHROME_WEB_DRIVER)
    driver.get(GOOGLE_FORM)
    sleep(2)

    form_address = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_address.send_keys(house_address[index])

    form_prices = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_prices.send_keys(house_prices[index])

    form_links = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_links.send_keys(house_links[index])

    submit_btn = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    submit_btn.click()

    driver.quit()


