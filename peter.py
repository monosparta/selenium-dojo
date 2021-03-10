import requests
import json
import os
import urllib
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fpdf import FPDF
from tqdm import tqdm

current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

# Call API
print('===Call API===')
response = requests.get('http://monospace.kktix.cc/events.json')
print(response.status_code, "OK")

# get url
print('===Get Url===')
data = response.json()
for i in data['entry']:
    if '0xFE' in i['title']:
        data_url = i['url']
print(data_url)

chromedriver_path = './chromedriver'
brave_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
option = webdriver.ChromeOptions()
option.binary_location = brave_path
# option.add_argument('--headless')
driver = webdriver.Chrome(executable_path=chromedriver_path, options=option)
driver.get(data_url)
# driver.maximize_window()

# make directory
print('===Make Directory===')
path = './img/'
if not os.path.isdir(path):
    os.makedirs(path)

# get title
print('===Get Title===')
title = driver.find_element_by_class_name('header-title')
print(title.text)

# get banner img
print('===Get banner img===')
img = driver.find_element_by_xpath('//div[@class="og-banner"]/img')
src = img.get_attribute('src')
print(src)
urllib.request.urlretrieve(src, "./img/banner.png")

# get description
print('===Get description===')
description = driver.find_element_by_class_name('description')
print(description.text)

# get data-code
print('===Get data-code===')
code = driver.find_element_by_xpath('//div[@class="description"]/pre')
data_code = str(code.text)
print(data_code[14:30])

# decode
print('===Decode===')
data_code = data_code[14:30]
decode = base64.b64decode(data_code)
decode = decode.decode("UTF-8")
decode = str(decode)
print(decode)

image_list = []

# screenshot
print('===Screenshot===')
img_path = './img/screenshot1.png'
driver.save_screenshot(img_path)
image_list.append(img_path)

# read json
print('===Read JSON===')
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(data)

name = data['name']
email = data['email']
phone = data['phone']
code = decode

# 報名
print('===Sign Up===')
try:
    # next
    driver.find_elements_by_xpath('//a[@class="btn-point"]')[1].click()
    time.sleep(3)
    # not for now
    driver.find_element_by_xpath(
        '//button[@class="btn btn-default pull-right ng-binding"]').click()
    time.sleep(1)
    # +1 button
    driver.find_element_by_xpath(
        '//button[@class="btn-default plus"]').click()
    time.sleep(1)
    # agree checkbox
    driver.find_element_by_id("person_agree_terms").click()
    time.sleep(1)
    # next
    driver.find_element_by_xpath(
        '//button[@class="btn btn-primary btn-lg ng-isolate-scope"]').click()
    time.sleep(3)
    # not for now
    driver.find_element_by_xpath(
        '//button[@class="btn btn-default pull-right ng-binding"]').click()
    # name
    driver.find_element_by_name("contact[field_text_701843]").click()
    driver.find_element_by_name(
        "contact[field_text_701843]").send_keys(name)
    # email
    driver.find_element_by_name("contact[field_email_701844]").click()
    driver.find_element_by_name("contact[field_email_701844]").send_keys(email)
    # phone
    driver.find_element_by_name("contact[field_text_701845]").click()
    driver.find_element_by_name(
        "contact[field_text_701845]").send_keys(phone)
    # code
    driver.find_element_by_name("contact[field_text_701846]").click()
    driver.find_element_by_name("contact[field_text_701846]").send_keys(code)
    # agree
    driver.find_element_by_id("person_agree_terms").click()
    # screenshot
    img_path = './img/screenshot2.png'
    driver.save_screenshot(img_path)
    image_list.append(img_path)
    # submit
    driver.find_element_by_xpath(
        '//a[@class="btn btn-primary btn-lg ng-binding ng-isolate-scope"]').click()
    time.sleep(3)
    print('Finish')
except Exception as e:
    print("Exception found", format(e))

img_path = './img/screenshot3.png'
driver.save_screenshot(img_path)
image_list.append(img_path)
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
img_path = './img/screenshot4.png'
driver.save_screenshot(img_path)
image_list.append(img_path)

qrcode = driver.find_element_by_xpath('//div[@class="qr-code ng-scope"]/img')
qrcode_src = qrcode.get_attribute('src')
img_path = './img/qrcode.png'
urllib.request.urlretrieve(qrcode_src, img_path)

# img to pdf
print('===Generate PDF===')
pdf = FPDF()
for img in tqdm(image_list):
    pdf.add_page()
    pdf.image(img, 0, 0, 210, 0)
pdf.output('result.pdf', 'F')

driver.quit()
