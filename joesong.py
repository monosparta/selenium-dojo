import urllib.parse
import urllib.request
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options() # 啟動無頭模式
chrome_options.add_argument('--headless')  #規避google bug
chrome_options.add_argument('--disable-gpu')

url='https://kktix.com/events.json?search=0xFE'

# 請求頭資訊
herders={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36', 'Referer':'https://movie.douban.com','Connection':'keep-alive'}

# 設定請求頭
req = urllib.request.Request(url,headers=herders)
# 發起請求，得到response響應
response=urllib.request.urlopen(req)


# json轉換為字典
hjson = json.loads(response.read())


# 印出他的URL
for item in hjson["entry"]:
    print(item["url"])
a=item["url"]
executable_path = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=executable_path,
chrome_options=chrome_options)
driver.get(a) 
print('截圖照片')
imagename=datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

driver.save_screenshot('stepOne/'+imagename+'.png') 
#下載圖片
print("---下載封面圖片...")
banner = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[3]/img").get_attribute('src')
url=banner
r=requests.get(url)
with open('./stepOne/封面.jpg','wb') as f:
#將圖片下載下來
    f.write(r.content)
text =driver.find_element_by_class_name('description').text
print(text)
print('下一步......')             
button=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[7]/a")
button.click()

print('關閉登入通知......')
wait = WebDriverWait(driver, 10)
button1= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="guestModal"]/div[2]/div/div[3]/button')))
button1.click()
print('購買票數......')
wait = WebDriverWait(driver, 10)
input1= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ticket_344407"]/div/span[3]/button[2]')))
input1.click()
print('同意授權條款......')
wait = WebDriverWait(driver, 10)
check1= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="person_agree_terms"]')))
check1.click()
print('下一步......')
wait = WebDriverWait(driver, 10)
button3= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="registrationsNewApp"]/div/div[5]/div[4]/button')))
button3.click()
print('關閉登入通知......')
wait = WebDriverWait(driver, 10)
button4= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="guestModal"]/div[2]/div/div[3]/button')))
button4.click()


print('填寫姓名......')
wait = WebDriverWait(driver, 10)
name= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field_text_701843"]/div/div/input')))
name.send_keys("宋鎔宇")
print('填寫信箱......')
wait = WebDriverWait(driver, 10)
email= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field_email_701844"]/div/div/input')))
email.send_keys("mononojoesong@gmail.com")
print('填寫電話......')
wait = WebDriverWait(driver, 10)
phone= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field_text_701845"]/div/div/input')))
phone.send_keys("0987696900")
print('填寫代號......')
wait = WebDriverWait(driver, 10)
input3= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field_text_701846"]/div/div/input')))
input3.send_keys("MONOSPARTA")


print('同意授權條款......')
wait = WebDriverWait(driver, 10)
check2 =wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="person_agree_terms"]')))
check2.click()

print('確認表單資料.....')
button4=driver.find_element_by_xpath('//*[@id="registrations_controller"]/div[4]/div[2]/div/div[6]/a')
button4.click()
print('恭喜!您已完成購票.....')






