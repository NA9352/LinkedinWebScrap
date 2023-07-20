from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import json

global data
data = []

linkedin_username = "nikitasomani0304@gmail.com"
linkedin_password = "Nikita@9352"

s = Service('https://my.shell.com/:u:/r/personal/nikita_n_agrawal_shell_com/Documents/Documents/Data%20Science/WebScrap/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
sleep(6)
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(linkedin_username)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(linkedin_password)
sleep(3)
driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()

df = pd.read_csv('Test.csv')



for url in df.loc[:, 'URLs']:
    driver.get(url)

    # #********** Profile Details **************#
    loc = ""
    page = BeautifulSoup(driver.page_source,'lxml')
    try:
        cover = page.find('img', attrs = {'class':'profile-background-image__image relative full-width full-height'})['src']
    except:
        cover = 'None'

    try:
        profile = page.find('img', class_='lazy-image ember-view')['src']
                
    except:
        profile = "None"

    try:
        title = str(page.find("li", attrs = {'class':'inline t-24 t-black t-normal break-words'}).text).strip()
    except:
        title = 'None'
    try:
        heading = str(page.find('h2', attrs = {'class':'mt1 t-18 t-black t-normal'}).text).strip()
    except:
        heading = 'None'
    try:
        loc = str(page.find('li', attrs = {'class':'t-16 t-black t-normal inline-block'}).text).strip()
    except:
        loc = 'None'


    #*******  Contact Information **********#
    sleep(2)
    driver.get(url + 'overlay/contact-info/')

    info = BeautifulSoup(driver.page_source, 'lxml')
    details = info.findAll('section',attrs = {'class':'pv-contact-info__contact-type'})
    try:
        websites = details[1].findAll('a')
        for website in websites:
            website = website['href']
            
    except:
        website = 'None'
    try:
        phone = details[2].find('span').text
    except:
        phone = 'None'
    try:
        email = str(details[3].find('a').text).strip()
    except:
        email = 'None'
    try:
        connected = str(details[-1].find('span').text).strip()
    except:
        connected = 'None'

            
    data.append({'profile_url':url,'cover':cover,'profile':profile,'title':title,'heading':heading,'loc':loc,'website':website,'phone':phone,'email':email,'connected':connected,})
print("!!!!!! Data scrapped !!!!!!")
                
driver.quit()

df = pd.DataFrame(data)
df = df.transpose()
df.to_csv('Output.csv')



