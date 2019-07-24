import os  
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-U', '--username', help='username for python anywhere account')
parser.add_argument('-P', '--password', help='password for python anywhere account')


def reload_application():
	args = parser.parse_args()

	if not args.password or not args.username:
		return 'no username or password supplied'

	day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

	chrome_options = Options()  
	chrome_options.add_argument("--headless") 
	chromedriver = os.path.join(os.getcwd(), 'chromedriver.exe')
	driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)
	driver.implicitly_wait(10)

	driver.get('https://www.pythonanywhere.com/login/?next=/')
	driver.find_element_by_id('id_auth-username').send_keys(args.username)
	driver.find_element_by_id('id_auth-password').send_keys(args.password)
	driver.find_element_by_id('id_next').click()

	try:
	    web_tab_link = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'id_web_app_link')))
	except TimeoutException:
	    return f'Timed out on web tab locator at {datetime.now().strftime("%d-%m-%y %H:%I:%S")}.'
	else:
		driver.find_element_by_id('id_web_app_link').click()

	try:
		extend_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'webapp_extend')))
	except TimeoutException:
		return f'Timed out on refresh application button locator at {datetime.now().strftime("%d-%m-%y %H:%I:%S")}.'
	else:
		driver.find_element_by_class_name('webapp_extend').click()

	expiry_text = driver.find_element_by_class_name('webapp_expiry').text

	day_of_expiry = list(filter(lambda x: x in expiry_text, day_names))[0]

	expiry_date = expiry_text[expiry_text.index(day_of_expiry):]

	return f'Successfully reloaded application to run until {expiry_date}'


if __name__ == '__main__':
	reload_application()
