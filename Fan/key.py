from selenium import webdriver
import time 
from urllib.request import urlretrieve
from selenium.webdriver import ActionChains
import base64
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
result=driver.get("https://www.google.com/")

element=driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input')
element.send_keys('sdfasfasdsda')