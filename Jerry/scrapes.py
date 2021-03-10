# 載入需要的套件
from selenium import webdriver
import json
import requests
from fpdf import FPDF

# 開啟瀏覽器視窗(Chrome)
# 方法一：執行前需開啟chromedriver.exe且與執行檔在同一個工作目錄
# driver = webdriver.Chrome('./chromedriver')
option = webdriver.ChromeOptions();
option.add_argument("--headless");
driver = webdriver.Chrome(options=option, executable_path='./chromedriver');

driver.get("http://monospace.kktix.cc/events.json")
driver.save_screenshot('./image_screen1.png')
pre = driver.find_element_by_tag_name("pre").text
# element = driver.find_element_by_tag(“title”).text
data = json.loads(pre)
target_url = 0
for entry in data.get('entry'):
    if (entry.get('title')).find('0xFE') > -1:
        print(entry)
        print('fucking url i want: ')
        target_url = entry.get('url')
        print(target_url)


## Get page url
driver2 = webdriver.Chrome(options = option, executable_path='./chromedriver')
print('欲抓取頁面:')
print(target_url)
driver2.get(target_url) ## driver2: WebDriver object
driver2.save_screenshot('./image_screen2.png')

## Get Image
html_img = driver2.find_element_by_xpath('//div[@class="og-banner"]/img')
html_img = html_img.get_attribute('src')
response = requests.get(html_img) 
newname = 'image_content.jpg'
with open(newname,'wb') as file:
    file.write(response.content)
    
# html1 = driver2.find_element_by_xpath('//img[@src]')
# html1 = driver2.find_element_by_tag_name('img') ## driver1: Webelement object
# pre2 = html1.get("img")
print('Image: ')
print(html_img)

## Get title
html_title = driver2.find_element_by_tag_name('h1')
print('Title: ')
print(html_title.text)

## Get context
html_context = driver2.find_element_by_xpath('//div[@class="description"]')
print('Context:')
print(html_context.text)



## get code
html_code = driver2.find_element_by_xpath('//div[@class="description"]/pre').text
print('Code: ')
print(html_code)
start = False
codeList = []
for char in html_code:
    if(start):
        codeList.append(char)
    if(char == '"'):
        start = True if (start == False) else False
codeList = codeList[:-1]

## decode
import base64
codeString = ''
for char in codeList:
    codeString = codeString + str(char)

codeString = base64.b64decode(codeString)
print(codeString)
codeString = codeString.decode("UTF-8")
print(codeString)



## button
import time
# click radio button

## next button
html_next_button = driver2.find_elements_by_xpath("//a[@class='btn-point']")[1].click()
time.sleep(1)
print('next_button OK!')

## Not for now
html_button2 = driver2.find_elements_by_xpath("//button[@class='btn btn-default pull-right ng-binding']")[0].click()
time.sleep(1)
print('not for now OK!')
driver2.save_screenshot('./image_screen3.png')

## plus button
html_plus_button = driver2.find_element_by_xpath("//button[@class = 'btn-default plus']").click()
time.sleep(1)
print('plus_button OK!')

## read button
html_read_button = driver2.find_element_by_xpath("//input[@id ='person_agree_terms']").click()
time.sleep(1)
print('read_button OK!')

## next button
html_next_button = driver2.find_elements_by_xpath("//button[@class='btn btn-primary btn-lg ng-isolate-scope']")[0].click()
time.sleep(3)
print('next_button OK!')

## Not for now
html_button2 = driver2.find_elements_by_xpath("//button[@class='btn btn-default pull-right ng-binding']")[0].click()
time.sleep(1)
print('not for now OK!')
driver2.save_screenshot('./image_screen4.png')

## Open the Json
with open('./description.json') as f:
    data = json.load(f)

## name
driver2.find_element_by_name("contact[field_text_701843]").click()
time.sleep(1)
driver2.find_element_by_name(
    "contact[field_text_701843]").send_keys(data['name'])
# time.sleep(1)
## email
driver2.find_element_by_name("contact[field_email_701844]").click()
driver2.find_element_by_name("contact[field_email_701844]").send_keys(data['email'])
# time.sleep(1)
## phone
driver2.find_element_by_name("contact[field_text_701845]").click()
driver2.find_element_by_name(
    "contact[field_text_701845]").send_keys(data['phone'])
# time.sleep(1)
## code
driver2.find_element_by_name("contact[field_text_701846]").click()
driver2.find_element_by_name("contact[field_text_701846]").send_keys(codeString)
time.sleep(1)
print('finish')

## read button
html_read_button = driver2.find_element_by_xpath("//input[@id ='person_agree_terms']").click()
time.sleep(1)
print('read_button OK!')

## Next button
html_next_button = driver2.find_element_by_xpath("//a[@class='btn btn-primary btn-lg ng-binding ng-isolate-scope']").click()
time.sleep(1)
print('next_button OK!')
time.sleep(1)
driver2.save_screenshot('./image_screen5.png')

## Get Ticket Image
time.sleep(3)
# html_image = driver2.find_element_by_xpath("//div[@class='qr-code ng-scope']/img")
# html_image = html_image.get_attribute('src')
# response = requests.get(html_image) 
driver2.execute_script("window.scrollTo(0, document.body.scrollHeight)")
driver2.save_screenshot('./image_ticket.png')
# newname = 'image_ticket.png'
# with open(newname,'wb') as file:
#     file.write(response.content)


from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.image('image_screen1.png', 0, 0, 210)
pdf.add_page()
pdf.image('image_screen2.png', 0, 0, 210)
pdf.add_page()
pdf.image('image_screen3.png', 0, 0, 210)
pdf.add_page()
pdf.image('image_screen4.png', 0, 0, 210)
pdf.add_page()
pdf.image('image_screen5.png', 0, 0, 210)
pdf.add_page()
pdf.image('image_ticket.png', 0, 0, 210)
pdf.add_page()
pdf.image('image_content.jpg', 0, 0, 210)
pdf.output('output.pdf', 'F')