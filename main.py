import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
from mail import sendMail

load_dotenv()

# Chrome driver options
options = webdriver.ChromeOptions()
options.headless = True

# Initializing chrome driver
driver = webdriver.Chrome(
    os.getenv('CHROME_DRIVER_PATH'), options=options)

driver.get(os.getenv('PORTAL_URL'))
print('Driver Initialized ...')
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Credentials
STUDENT_ID = os.getenv('STUDENT_ID')
PASSWORD = os.getenv('PASSWORD')

# Driver elements
username_xpath = '//*[@id="username"]'
pass_xpath = '//*[@id="pass"]'
captcha_xpath = '//*[@id="lblcaptchaAnswer"]'
button_xpath = '//*[@id="submit"]'

# Fillup username & password
driver.find_element_by_xpath(username_xpath).send_keys(STUDENT_ID)
print('Filled Username ...')
driver.find_element_by_xpath(pass_xpath).send_keys(PASSWORD)
print('Filled Password ...')

# Fillup captcha
firstNum = soup.find('label', {'id': 'lblFirstNo'}).get_text()
print(f'First Number: {firstNum}')
secondNum = soup.find('label', {'id': 'lblSecondNo'}).get_text()
print(f'Second Number: {secondNum}')
total = int(firstNum) + int(secondNum)

driver.find_element_by_xpath(captcha_xpath).send_keys(str(total))
print(f'Filled in Captcha: {total}')

# Submit Form
driver.find_element_by_xpath(button_xpath).click()
print('From Submitted ...')

# Switch view to Grade Report
gradeReport_xpath = '/html/body/div[1]/div[1]/nav/ul/li[3]/a'
driver.find_element_by_xpath(gradeReport_xpath).click()
time.sleep(7)
print('Switched to Grade Report')

# Find grade summary
soup = BeautifulSoup(driver.page_source, 'html.parser')
summary = soup.find('div', {'id': 'transcriptSummary'})
report = summary.find_all('td')
report.reverse()

GRADE_REPORT = '\n'

# Find CGPA
for data in report[1:3]:
    GRADE_REPORT += data.get_text() + '\n'

# Find term GPA
semester = soup.find_all('div', class_='courseContainerDiv')
semester.pop()

GRADE_REPORT += '\n'
for table in semester:
    sem = table.find('h6', class_='headingabovetable').get_text(
    ) + ' ' + table.find_all('tr')[-1].find_all('td')[-1].get_text().lstrip().rstrip() + '\n'
    GRADE_REPORT += sem

print(GRADE_REPORT)

RECIEVER_ADDRESS = os.getenv('RECIEVER_ADDRESS')

# Send email with Grade Report
sendMail(RECIEVER_ADDRESS, GRADE_REPORT)

driver.quit()
