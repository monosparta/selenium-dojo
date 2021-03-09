import os
import time
import json
import base64
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#設定現在時間
current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
print("---搜尋API...")
r = requests.get('https://kktix.com/events.json?search=0xFE')
#如果回傳200就傳給data
if r.status_code == requests.codes.ok:
  data = r.text
#轉成dictnary
print("---抓取url資料...")
obj = json.loads(data)
url=obj['entry'][0]['url']

# print("---啟用無頭模式...")
# chrome_options = Options() # 啟動無頭模式
# chrome_options.add_argument('--headless')  #規避google bug
# chrome_options.add_argument('--disable-gpu')
# executable_path = 'chromedriver.exe'#自行設定路徑
# driver = webdriver.Chrome(executable_path=executable_path,
# chrome_options=chrome_options)
driver = webdriver.Chrome() #開啟chrome
driver.get(url)

#創建資料夾
print("---創建資料夾...")
os.makedirs('./img/',exist_ok=True)
#讀取title
print("---讀取標題...")
content = driver.find_element_by_class_name('header-title').text
print(content)

#下載圖片
print("---下載封面圖片...")
banner = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[3]/img").get_attribute('src')
url=banner
r=requests.get(url)
with open('./img/封面.jpg','wb') as f:
#將圖片下載下來
    f.write(r.content)

#讀取內文
print("---讀取內文...")
content = driver.find_element_by_class_name('description').text
print(content)

print("---取得data-code...")
#取得data-code
dataCode=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[6]/div/pre").text
first=dataCode.find('"')+1
end=dataCode.find('"',first)
encodedata=dataCode[first:end]
bytecode=base64.b64decode(encodedata)
code=bytecode.decode("UTF-8")
print("---解碼完畢...")
#下一步
button=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[7]/a")
button.click()

#暫時不要
wait = WebDriverWait(driver, 10)
button1= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="guestModal"]/div[2]/div/div[3]/button')))
button1.click()
#票+1
print("---選擇票券數量...")
button2= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ticket_344407"]/div/span[3]/button[2]')))
button2.click()
#我已經閱讀並同意 授權條款 與 隱私權政策
print("---我已經閱讀並同意 授權條款 與 隱私權政策...")
checkboxs=driver.find_elements_by_css_selector('input[type=checkbox]')
for checkbox in checkboxs:
 	checkbox.click()
#下一步
button=driver.find_element_by_xpath('//*[@id="registrationsNewApp"]/div/div[5]/div[4]/button')
button.click()
print("---不登入...")
#暫時不要
button1= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="guestModal"]/div[2]/div/div[3]/button')))
button1.click()
time.sleep(2)

print("---讀取json檔案...")
f= open("./information.json","r",encoding="utf-8")
word = f.read()
print(word)
f.close()
obj = json.loads(word)
print("---寫入name")
print("---寫入email")
print("---寫入phone")
#填寫資料
print("---填寫資料...")
element=driver.find_element_by_xpath('//*[@id="field_text_701843"]/div/div/input')
element.send_keys(obj['name'])
element=driver.find_element_by_xpath('//*[@id="field_email_701844"]/div/div/input')
element.send_keys(obj['email'])
element=driver.find_element_by_xpath('//*[@id="field_text_701845"]/div/div/input')
element.send_keys(obj['phone'])
element=driver.find_element_by_xpath('//*[@id="field_text_701846"]/div/div/input')
element.send_keys(code)

#我已經閱讀並同意 授權條款 與 隱私權政策
checkboxs=driver.find_elements_by_css_selector('input[type=checkbox]')
for checkbox in checkboxs:
 	checkbox.click()

#確認表單資料
button=driver.find_element_by_xpath('//*[@id="registrations_controller"]/div[4]/div[2]/div/div[6]/a')
button.click()
time.sleep(2)

#下載圖片
print("---下載票券...")
tickurl= driver.find_element_by_xpath('//*[@id="registrations_controller"]/div[1]/div[2]/div/div[2]/div[4]/div[2]/div/ul/li/div/div/div[1]/div[2]/img').get_attribute('ng-src')
url=tickurl
r=requests.get(url)
with open('./img/tick.jpg','wb') as f:
#將圖片下載下來
    f.write(r.content)

#取消訂票
button=driver.find_element_by_xpath('//*[@id="registrations_controller"]/div[1]/div[2]/div/div[2]/div[4]/div[1]/div/a')
button.click()

#送出並取消訂單
button=driver.find_element_by_xpath('//*[@id="registrationsShowApp"]/div[2]/div/div/div/div[2]/div/a[1]')
button.click()
alert = driver.switch_to.alert #切換到alert
print('alert text : ' + alert.text) #列印alert的文字
alert.accept() #點選alert的【確認】按鈕

#關閉瀏覽器
driver.quit()
