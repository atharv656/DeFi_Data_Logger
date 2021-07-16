from urllib.request import Request, urlopen
from selenium import webdriver
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
    def __init__(self, rank, name, chain, balance, users, dailyChangeInPrice, volume):
        self.rank = rank
        self.name = name
        self.balance = round(strToNum(re.sub("\$","",balance)))
        self.chain = chain
        self.users = round(strToNum(users))
        self.dailyChangeInPrice = dailyChangeInPrice
        self.volume = round(strToNum(re.sub("\$","",volume)))

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
        cursor.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?,?)", (date, time, coin.name, coin.rank, coin.chain, coin.users, coin.volume, coin.balance))
        print("query executed")
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

connection = create_connection("data.sqlite")
createTable(connection)

url = "https://dappradar.com/rankings/category/defi"
#Uncomment for Windows/Comment for Linux
#driver = webdriver.Firefox(executable_path = "C:/Users/vaidehi/Downloads/geckodriver.exe")
#Uncomment for Linux/Comment for Windows
driver = webdriver.Firefox(executable_path = "/home/vinay/Downloads/geckodriver")
driver.get(url)

try:
    while True:
        driver.refresh()
        time.sleep(1)
        results = driver.find_elements_by_xpath("//*[@id='root']//*[@class='rankings-table']//*[@class='rankings-row']")
        data = []

        current_datetime = datetime.datetime.now()
        date = current_datetime.strftime("%x")
        currentTime = current_datetime.strftime("%X")

        for result in results:
            legible_Data = result.text
            clean = legible_Data.splitlines()
            # print(clean)
            try:
                inp = Coin(int(clean[0]), clean[1], clean[3], clean[4], clean[5], clean[6], clean[7])
                addInfo(connection, inp, str(date), str(currentTime))
                data.append(inp)
                # inp.displayCoin()
            except ValueError as e:
                print(f"Error {e} occurred")

        print(len(data)," rows added")
        time.sleep(10)
except KeyboardInterrupt:
    print("Quitting program...")
    driver.quit()
