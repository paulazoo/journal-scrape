from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import smtplib
import ssl
from email.message import EmailMessage

from email_password import paulazhupython_email_password, paulazhupython_app_password

import numpy as np

# selenium
driver = webdriver.Chrome()

# nature papers
driver.get("https://www.nature.com/search?q=*&journal=neuro,%20nature&article_type=research&subject=neuroscience&order=date_desc")
elems = driver.find_elements(By.CLASS_NAME, "c-card__link")

all_papers = np.array(['Title', 'Link'])
for elem in elems:
    all_papers = np.vstack([all_papers, [elem.text, elem.get_attribute("href")]])
print(all_papers)
driver.close()

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
 
# start TLS for security
s.starttls()
 
# Authentication
s.login("paulazhupython@gmail.com", paulazhupython_app_password)
 
# message to be sent
message = "Message_you_need_to_send"
 
# sending the mail
s.sendmail("paulazhupython@gmail.com", "paulazhu@college.harvard.edu", message)
 
# terminating the session
s.quit()