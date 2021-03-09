import asyncio
from selenium import webdriver
import time 
from urllib.request import urlretrieve
from selenium.webdriver import ActionChains
import base64
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

async def performClick(driver,xpath):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element=driver.find_element_by_xpath(xpath)
    element.click()

async def performWrite(driver,xpath,inputs):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element=driver.find_element_by_xpath(xpath)
    element.clear()
    element.send_keys(inputs)

async def downloadImage(driver,xpath,fileName):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    img = driver.find_element_by_xpath(xpath)# 找圖片
    src = img.get_attribute('src')
    urlretrieve(src, fileName+nowForFile+".png") # 下載圖片

async def beHuman(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scroll(0, 0);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("...I'M HUMAN...")


loop = asyncio.get_event_loop()
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
nowForFile = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
url = 'https://kktix.com/events.json?search=0xFE'
resp = requests.get(url=url)
data = resp.json() # Check the JSON Response Content documentation below
# print("url from api"+data['entry'][0]['url'])

print('...設定web driver...')
chrome_options = Options() # 啟動無頭模式
chrome_options.add_argument('--headless')  #規避google
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)
result=driver.get(data['entry'][0]['url'])

loop.run_until_complete(downloadImage(driver,'/html/body/div[2]/div[2]/div/div[3]/img','eventImage/eventImage_'))
# 找標題＆內文
title = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[1]/div/h1')
content = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[6]/div/p[1]')
print("標題:"+title.get_attribute('innerHTML'))
print("內文:\n"+content.get_attribute('innerHTML'))
# 找data-code 
dataCode=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[6]/div/pre')
dataCodeFormatted=dataCode.get_attribute('innerHTML')[17:33] #裁切字串
decodedDataCode = base64.b64decode(dataCodeFormatted).decode('utf-8') #解碼
# print(decodedDataCode)

driver.save_screenshot('stepOne/step_one_'+nowForFile+'.png')
print('...Say Cheese!...')
loop.run_until_complete(beHuman(driver))

loop.run_until_complete(performClick(driver,'/html/body/div[2]/div[2]/div/div[7]/a'))
print('...下一步...')
# print(driver.current_url)
#  等待modal載入
loop.run_until_complete(performClick(driver,'//*[@id="guestModal"]/div[2]/div/div[3]/button'))
print('...關閉modal...')
loop.run_until_complete(performClick(driver,'//*[@id="ticket_344407"]/div/span[3]/button[2]'))
print('...票數＋1...')
loop.run_until_complete(performClick(driver,'//*[@id="person_agree_terms"]'))
print('...已閱讀並同意...')
driver.save_screenshot('stepTwo/step_two_'+nowForFile+'.png')
print('...Say Cheese!...')
loop.run_until_complete(beHuman(driver))

loop.run_until_complete(performClick(driver,'//*[@id="registrationsNewApp"]/div/div[5]/div[4]/button'))
print('...下一頁...')
loop.run_until_complete(performClick(driver,'//*[@id="guestModal"]/div[2]/div/div[3]/button'))
print('...關閉modal...')

loop.run_until_complete(performWrite(driver,'//*[@id="field_text_701843"]/div/div/input','測試樊'+now))
print('...寫入姓名...')
loop.run_until_complete(performWrite(driver,'//*[@id="field_email_701844"]/div/div/input','fanfanfan9453@gmail.com'))
print('...寫入信箱...')
loop.run_until_complete(performWrite(driver,'//*[@id="field_text_701845"]/div/div/input','0912345678'))
print('...寫入電話...')
loop.run_until_complete(performWrite(driver,'//*[@id="field_text_701846"]/div/div/input',decodedDataCode))
print('...寫入data-code...')
loop.run_until_complete(performClick(driver,'//*[@id="person_agree_terms"]'))
print('...我已經閱讀並同意...')
driver.save_screenshot('stepThree/step_three_'+nowForFile+'.png')
print('...Say Cheese!...')
loop.run_until_complete(beHuman(driver))

loop.run_until_complete(performClick(driver,'//*[@id="registrations_controller"]/div[4]/div[2]/div/div[6]/a'))
print('...確認表單資料...')
loop.run_until_complete(downloadImage(driver,'//*[@id="registrations_controller"]/div[1]/div[2]/div/div[2]/div[4]/div[2]/div/ul/li/div/div/div[1]/div[2]/img','Ticket/event_qr_code_'))
print('...下載活動票券...')
driver.save_screenshot('ending/ending_'+nowForFile+'.png')
print('...Say Cheese!...')
print('...完成所有程序，即將關閉瀏覽器...')
driver.quit()#關閉瀏覽器 
