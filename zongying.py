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

print("---CALL API...")
r = requests.get('https://kktix.com/events.json?search=0xFE')
if r.status_code == requests.codes.ok:
  print(r.status_code,"OK")

print("---抓取url資料...")
obj = r.json()
url=obj['entry'][0]['url']

print("---啟用無頭模式...")
chrome_options = Options() # 方法一啟動無頭模式
chrome_options.add_argument('--headless')
userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.add_argument("--window-size=1280,1440")
chrome_options.add_argument("--hide-scrollbars")

executable_path = './chromedriver.exe'#自行設定路徑
driver = webdriver.Chrome(executable_path=executable_path,chrome_options=chrome_options)
# 方法二開啟實體chrome
# driver = webdriver.Chrome() 

#設定瀏覽器高度
scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(scroll_width, scroll_height)

driver.get(url)

#設定最常等待時間
wait = WebDriverWait(driver, 10)
driver.save_screenshot('./img/步驟一進入頁面.png')
print("---創建資料夾...")
os.makedirs('./img/',exist_ok=True)
print("---讀取標題...")
title = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[1]/div/h1").text
print(title)

#下載封面
print("---下載封面圖片...")
banner = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[3]/img").get_attribute('src')
url=banner
r=requests.get(url)
with open('./img/封面.jpg','wb') as f:
  f.write(r.content)

#讀取內文
print("---讀取內文...")
content = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[6]/div").text
print(content)

print("---取得data-code...")
dataCode=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[6]/div/pre").text
first=dataCode.find('"')+1
end=dataCode.find('"',first)
encodedata=dataCode[first:end]
bytecode=base64.b64decode(encodedata)
code=bytecode.decode("UTF-8")
print("---解碼完畢...")

print("---下一頁...")
button=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[7]/a")
time.sleep(1)

button.click()

#暫時不要
print("---不登入...")
button1= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="guestModal"]/div[2]/div/div[3]/button')))
time.sleep(1)
driver.save_screenshot('./img/步驟二登入選項.png')
button1.click()

#票+1
print("---選擇票券數量...")
button2= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ticket_344407"]/div/span[3]/button[2]')))
button2.click()

#我已經閱讀並同意 授權條款 與 隱私權政策
print("---我已經閱讀並同意 授權條款 與 隱私權政策...")
checkbox=driver.find_element_by_xpath('//*[@id="person_agree_terms"]')
checkbox.click()
print("---下一步...")
button=driver.find_element_by_xpath('//*[@id="registrationsNewApp"]/div/div[5]/div[4]/button')

time.sleep(1)
driver.save_screenshot('./img/步驟三選擇票卷數量及確認隱私權政策.png')
button.click()

#暫時不要
print("---不登入...")
button1= wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[1]/div/div[2]/div/div[3]/button')))
time.sleep(1)
button1.click()

#讀取json檔案
print("---讀取json檔案...")
f= open("./information.json","r",encoding="utf-8")
word = f.read()
print(word)
f.close()
obj = json.loads(word)
print("---讀取name")
print("---讀取email")
print("---讀取phone")

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
print("---我已經閱讀並同意 授權條款 與 隱私權政策...")
checkbox=driver.find_element_by_xpath('//*[@id="person_agree_terms"]')
checkbox.click()

time.sleep(1)
driver.save_screenshot('./img/步驟四填寫完畢.png')

#確認表單資料
print("---確認表單資料...")
button=driver.find_element_by_xpath('//*[@id="registrations_controller"]/div[4]/div[2]/div/div[6]/a')
button.click()
time.sleep(2)

#下載票券
print("---下載票券...")
tickurl=wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="registrations_controller"]/div[1]/div[2]/div/div[2]/div[4]/div[2]/div/ul/li/div/div/div[1]/div[2]/img'))).get_attribute('ng-src')
url=tickurl
r=requests.get(url)
#將圖片下載下來
with open('./img/tick.jpg','wb') as f:
    f.write(r.content)
time.sleep(1)
driver.save_screenshot('./img/步驟五訂票成功.png')

#取消訂票
print("---取消票券...")
button=driver.find_element_by_xpath('//*[@id="registrations_controller"]/div[1]/div[2]/div/div[2]/div[4]/div[1]/div/a')
button.click()

#送出並取消訂單
print("---確認取消...")
button=driver.find_element_by_xpath('//*[@id="registrationsShowApp"]/div[2]/div/div/div/div[2]/div/a[1]')
button.click()
alert = driver.switch_to.alert #切換到alert
print('alert text : ' + alert.text) #列印alert的文字
alert.accept() #點選alert的【確認】按鈕

#關閉瀏覽器
print("---執行結束...")
driver.quit()

#產生pdf
from fpdf import FPDF
import glob
xx=['一','二','三','四','五']
#A4高度335
yy=[10,105,200,10,105,200]
filenames=[]
for i in xx:
  filename=(glob.glob("./img/步驟"+i+"*.png")) #步驟一到六
  filenames.append(filename[0])#放入陣列

pdf = FPDF()
pdf.add_font('微軟正黑體','','微軟正黑體-1.ttf',True)
pdf.set_font("微軟正黑體", size=12)

pdf.add_page()
pdf.write(10,title)
pdf.image("./img/封面.jpg",x=0,y=30,w=190)
pdf.write(10,content)
pdf.image("./img/tick.jpg",x=75,y=230,w=50,h=50)

pdf.add_page()
pdf.text(10,10,"Welcome to kktix")
pdf.image(filenames[0],x=5,y=20,w=200)
pdf.add_page()
pdf.text(10,10,"登入選項")
pdf.image(filenames[1],x=5,y=20,w=200)
pdf.add_page()
pdf.text(10,10,"選擇票卷數量")
pdf.image(filenames[2],x=5,y=20,w=200)
pdf.add_page()
pdf.text(10,10,"填寫資料")
pdf.image(filenames[3],x=5,y=20,w=200)
pdf.add_page()
pdf.text(10,10,"訂票成功")
pdf.image(filenames[4],x=5,y=20,w=200)
pdf.output("kktix訂票流程.pdf")
