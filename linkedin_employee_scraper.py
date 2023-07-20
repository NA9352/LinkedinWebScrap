from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


linkedin_username = "nikita.agrawal.2016@iitkalumni.org"
linkedin_password = "Nikita@9352"

s = Service('https://my.shell.com/:u:/r/personal/nikita_n_agrawal_shell_com/Documents/Documents/Data%20Science/WebScrap/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
sleep(6)
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(linkedin_username)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(linkedin_password)
sleep(3)
driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()

profiles = ['https://www.linkedin.com/in/nikita9352/']


for i in profiles:
	driver.get(i)
	sleep(5)
	title = driver.find_element(By.XPATH,"//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']").text
	print(title)
	description = driver.find_element(By.XPATH,"//div[@class='text-body-medium break-words']").text
	print(description)
	sleep(4)
driver.close()

