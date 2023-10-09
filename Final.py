from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import json

linkedin_username = ""
linkedin_password = ""

s = Service('') #locate chromedrive.exe
driver = webdriver.Chrome(service=s)
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
sleep(6)
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(linkedin_username)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(linkedin_password)
sleep(3)
driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()

df = pd.read_csv('Test.csv')

bio = {
    'Name': [],
    'Headline' : [],
    'Address': [],
    'Position': [],
    'Company_name': [],
    'Year': [],
    'Company_location': [],
    'College_name_1': [],
    'Degree_name_1': [],
    'Passing_year_1':[],
    'College_name_2': [],
    'Degree_name_2': [],
    'Passing_year_2':[],
    'Phone':[],
    'Email':[],
    'Website':[],
}

def education(section):
    list_tag = section.find_elements(By.TAG_NAME, 'li')
    print(e[0].text)
    for inde, a in enumerate(list_tag):
        if inde > 1:
            break
        else:
            try:
                posi = a.find_elements(By.CLASS_NAME, 'visually-hidden')
                bio[f'College_name_{inde+1}'].append(posi[0].text)
                bio[f'Degree_name_{inde+1}'].append(posi[1].text)
                bio[f'Passing_year_{inde+1}'].append(posi[2].text)
            except Exception as e:
                pass

def experience(section):
    f = section.find_element(By.TAG_NAME, 'li')
    posi = f.find_elements(By.CLASS_NAME, 'visually-hidden')
    try:
        bio['Position'].append(posi[0].text)
        bio['Company_name'].append(posi[1].text)
        bio['Year'].append(posi[2].text)
        bio['Company_location'].append(posi[3].text)
    except Exception as e:
        pass


def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

for url in df.loc[:, 'URLs']:
        #try:
                driver.get(url)
                name = driver.find_element(By.CLASS_NAME, 'text-heading-xlarge')
                bio['Name'].append(name.text)
                
                headline = driver.find_element(By.CLASS_NAME, 'text-body-medium.break-words')
                bio['Headline'].append(headline.text)

                # To get the current address
                location = driver.find_element(By.CSS_SELECTOR, 'span.text-body-small.inline.t-black--light.break-words')
                bio['Address'].append(location.text)
                
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
                bio['Website'].append(website)
                    
                try:
                    phone = details[2].find('span').text
                except:
                    phone = 'None'
                bio['Phone'].append(phone)
                
                try:
                    email = str(details[3].find('a').text).strip()
                except:
                    email = 'None'
                bio['Email'].append(email)
                
                sections = driver.find_elements(By.CLASS_NAME, 'artdeco-card.ember-view.relative.break-words.pb3.mt2')
                
                for section in sections:
                    div = section.find_element(By.CLASS_NAME, 'pvs-header__container')
                    if div.text.split('\n')[0] == 'Experience':
                        experience(section)

                    if div.text.split('\n')[0] == 'Education':
                        education(section)
                        
                for item in list(bio.keys()):
                    if len(bio['Name']) > len(bio[item]):
                        bio[item].append("Not Available")
                        
                #current_company = driver.find_element_by_xpath("*").get_attribute("href")
                #bio['Company_name'].append(current_company.text)
                
                #current_position = driver.find_element(By.XPATH, '//*[@id="ember753"]/div[3]/ul/li[1]/div/div[2]/div[1]/a/div/span/span[1]/text()')
                #bio['Title'].append(current_position.text)
                
                
                
driver.close()

df = pd.DataFrame.from_dict(bio, orient='index')
df = df.transpose()
df.to_csv('Output.csv')



