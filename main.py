from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import smtplib
import ssl
from email.message import EmailMessage

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email_password import paulazhupython_email_password, paulazhupython_app_password

import datetime
import numpy as np
import pandas as pd

# selenium
driver = webdriver.Chrome()

all_papers = np.array(['', ''])
# nature and nature neuroscience papers
driver.get("https://www.nature.com/search?q=*&journal=neuro,%20nature&article_type=research&subject=neuroscience&date_range=last_7_days&order=date_desc")
elems = driver.find_elements(By.CLASS_NAME, "c-card__link")
for elem in elems:
    all_papers = np.vstack([all_papers, [elem.text, elem.get_attribute("href")]])

# cell and neuron papers
today = datetime.date.today()
lastweek = today - datetime.timedelta(days = 7)
# YYYYmmdd
cell_today = today.strftime("%Y%m%d")
cell_lastweek = lastweek.strftime("%Y%m%d")
driver.get("https://www.cell.com/action/doSearch?text1=*&field1=Keyword&Ppub=&Ppub="+cell_lastweek+"-"+cell_today+"&SeriesKey=cell&SeriesKey=neuron&type=advanced&ContentItemType=fla&startPage=0&sortBy=Earliest")
elems = driver.find_elements(By.CLASS_NAME, "meta__title")
for parent_elem in elems:
    elem = parent_elem.find_element(By.TAG_NAME,"a")
    all_papers = np.vstack([all_papers, [elem.text, elem.get_attribute("href")]])

# science papers
today = datetime.date.today()
science_month =today.strftime("%m")
science_year = today.strftime("%Y")
driver.get("https://www.science.org/action/doSearch?field1=AllField&text1=Neuroscience&field2=AllField&text2=&publication=&Ppub=&AfterMonth="+science_month+"&AfterYear="+science_year+"&BeforeMonth=&BeforeYear=&ConceptID=505143&ConceptID=505154&startPage=0&sortBy=Earliest")
elems = driver.find_elements(By.CLASS_NAME, "text-reset")
for elem in elems:
    all_papers = np.vstack([all_papers, [elem.text, elem.get_attribute("href")]])

driver.close()

df = pd.DataFrame(all_papers[1:,:], columns=['Title', 'Link'])
all_papers_html = df.to_html()

# email parameters
sender_email = "paulazhupython@gmail.com"
receiver_email = "paulazhu@college.harvard.edu"

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
 
# start TLS for security
s.starttls()
 
# Authentication
s.login(sender_email, paulazhupython_app_password)

message = MIMEMultipart("alternative")
message["Subject"] = "Neuro Papers This Week"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = np.array2string(all_papers)
html = all_papers_html

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# sending the mail
s.sendmail(sender_email, receiver_email, message.as_string())
 
# terminating the session
s.quit()




