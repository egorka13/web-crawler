from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
import uuid
import requests
from datetime import datetime
from urllib.parse import urlparse

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, os.pardir, os.pardir))

dateTimeObj = datetime.now()
currentDate = str(dateTimeObj.day) + "." + str(dateTimeObj.month) + "." + str(dateTimeObj.year)
currentTime = str(dateTimeObj.hour) + ":" + str(dateTimeObj.minute)

# URL to specific page
URL = "https://pikabu.ru/"
# Site's domain name
domain = "https://pikabu.ru/"

parsed_uri = urlparse(URL)
domainName = '{uri.netloc}'.format(uri=parsed_uri)

save_path = ROOT_DIR + "/output/" + domainName + " " + currentDate + " " + currentTime

# Create new folder
if os.path.isdir(ROOT_DIR + "/output") is False:
    os.mkdir(ROOT_DIR + "/output")

os.mkdir(save_path)

# Start the WebDriver and load the page
wd = webdriver.Chrome(executable_path="/Users/alep/Downloads/chromedriver")
wd.get(URL)

SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = wd.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = wd.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# And grab the page HTML source
html_page = wd.page_source
print(html_page)
wd.quit()

soup = BeautifulSoup(html_page, 'html.parser')

textArray = []

for element in soup.find_all('div'):
    # print(element.text)
    textArray.append(element.text)

text_file = open(os.path.join(save_path, "parsed text.txt"), "w")
text_file.write("".join(textArray).strip().replace("\t", "").replace("\n", ""))
text_file.close()

html_file = open(os.path.join(save_path, "parsed html.txt"), "w")
html_file.write(html_page)
html_file.close()

images = soup.findAll('img')
for image in images:
    #print image source
    print('Image:     ' + image['src'])
    filename, file_extension = os.path.splitext(image['src'])
    print("filename ", file_extension)
    contentData = requests.get(image['src']).content
    unique_filename = str(uuid.uuid4().hex)
    completeName = os.path.join(save_path, unique_filename + file_extension)
    with open(completeName, 'wb') as handler:
        handler.write(contentData)


videos = soup.findAll('video')
for video in videos:
    #print video source
    print('Image:     ' + video['src'])
    filename, file_extension = os.path.splitext(video['src'])
    print("filename ", file_extension)
    contentData = requests.get(video['src']).content
    unique_filename = str(uuid.uuid4().hex)
    completeName = os.path.join(save_path, unique_filename + file_extension)
    with open(completeName, 'wb') as handler:
        handler.write(contentData)