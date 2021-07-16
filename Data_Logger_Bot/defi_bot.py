from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sqlite3
from sqlite3 import Error
import datetime
import re

def strToNum(string):
    try:
        if "k" in string:
            string = string.replace("k","")
            string = float(string)*1000
        elif "M" in string:
            string = string.replace("M","")
            string = float(string)*1000000
        elif "B" in string:
            string = string.replace("B","")
            string = float(string)*1000000000
        else:
            string = float(string)
        return string
    except Error as e:
        print(f"The error '{e}' occurred")

class Coin:
    def __init__(self, rank, name, chain, balance, users, dailyChangeInPrice, volume, price):
        self.rank = rank
        self.name = name
        self.balance = round(strToNum(re.sub("\$","",balance)))
        self.chain = chain
        self.users = round(strToNum(users))
        self.dailyChangeInPrice = dailyChangeInPrice
        self.volume = round(strToNum(re.sub("\$","",volume)))
        self.price = strToNum(re.sub("\$","",price))

    def displayCoin(self):
        print("Coin #"+str(self.rank)+": ", self.name, "\t", self.users, " users\t", self.volume)

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        print("cursor loaded")
        cursor.execute(query)
        print("query executed")
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def createTable(connection):
    create_cryto_data_table = """
    CREATE TABLE IF NOT EXISTS data (
      date TEXT,
      time TEXT,
      name TEXT,
      rank INTEGER,
      price FLOAT(8,2),
      network TEXT,
      users INTEGER,
      volume INTEGER,
      balance INTEGER
    );
    """

    execute_query(connection, create_cryto_data_table)

def addInfo(connection, coin, date, time):
    # """
    # INSERT INTO data
    # VALUES
    #     ({date}, {time}, {coin.name}, {coin.rank}, {coin.chain}, {coin.users}, {coin.volume}, {coin.balance});
    # """
    cursor = connection.cursor()
    try:
        print("cursor loaded")
        cursor.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?)", (date, time, coin.name, coin.rank, coin.price, coin.chain, coin.users, coin.volume, coin.balance))
        print("query executed")
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

#INIT
connection = create_connection("data.sqlite")
createTable(connection)

url = "https://dappradar.com/rankings/category/defi"
#Uncomment for Windows/Comment for Linux
# driver = webdriver.Firefox(executable_path = "C:/Users/vaidehi/Downloads/geckodriver.exe")
# secondDriver = webdriver.Firefox(executable_path = "C:/Users/vaidehi/Downloads/geckodriver.exe")

#Uncomment for Linux/Comment for Windows
driver = webdriver.Firefox(executable_path = "/home/vinay/Downloads/geckodriver")
secondDriver = webdriver.Firefox(executable_path = "/home/vinay/Downloads/geckodriver")

driver.get(url)
secondDriver.get(url)
try:
    driver.find_element_by_xpath("//*[@class='launch__not-show-again css-vurnku']").click()
except Error as e:
    print("Error ",e, "occurred")
try:
    secondDriver.find_element_by_xpath("//*[@class='launch__not-show-again css-vurnku']").click()
except Error as e:
    print("Error ",e, "occurred")

#MAIN
try:
    while True:
        counter = 0
        for i in range(4):
            results = driver.find_elements_by_xpath("//*[@id='root']//*[@class='rankings-table']//*[@class='rankings-row']")

            for result in results:
                legible_Data = result.text
                clean = legible_Data.splitlines()

                try:
                    rank = int(clean[0])
                    name = re.sub("NEW", "", str(clean[1]))

                    element = f"//*[@title='{name}']"
                    link = driver.find_element_by_xpath(element).get_attribute("href")
                    secondDriver.get(link)

                    loading = True
                    t0 = time.time()
                    while loading:
                        try:
                            broken_page = secondDriver.find_elements_by_xpath("//*[contains(text(), 'Oops!')]")
                            if(len(broken_page)>0):
                                price = "-10"
                                loading = False
                                break
                            tokenPriceExists = len(secondDriver.find_elements_by_xpath("//*[contains(text(), 'Token Price')]"))>0

                            time_elapsed = time.time() - t0
                            if(time_elapsed>3):
                                price = "-10"
                                loading = False

                            if(tokenPriceExists):
                                price = secondDriver.find_elements_by_xpath("//*[@class='css-otg2q8']")[3].text
                                if "$" not in price:
                                    price = "-10"
                                loading = False

                        except IndexError:
                            pass
                    print(name, ": ", price)
                    # driver.execute_script("window.history.go(-1)")
                    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + "w")
                    inp = Coin(rank, name, clean[3], clean[4], clean[5], clean[6], clean[7],price)
                    current_datetime = datetime.datetime.now()
                    date = current_datetime.strftime("%x")
                    currentTime = current_datetime.strftime("%X")
                    addInfo(connection, inp, str(date), str(currentTime))
                    # inp.displayCoin()
                    counter = counter + 1
                except ValueError as e:
                    print(f"Error {e} occurred")

            next_button = driver.find_element_by_partial_link_text("next")
            next_button.click()
            time.sleep(2)

        print(counter," rows added")
        driver.get(url)
        time.sleep(2)

except KeyboardInterrupt:
    print("Quitting program...")
    driver.quit()
