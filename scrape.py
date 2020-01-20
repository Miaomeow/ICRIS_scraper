#!/usr/bin/env python3
import logging
import pathlib
import shutil
import sys
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep

def logout():
    driver.execute_script("forwardTo('main_s.jsp')")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "userinfo"))
    )
    driver.execute_script("logout_s();")

#
# Main Program
#
company_filename = "companies.txt"
PATH = os.getcwd()

# create results folder
shutil.rmtree(PATH+"/results")
pathlib.Path(PATH+"/results").mkdir(parents=True, exist_ok=True) 

# initialize logger
logging.basicConfig(filename='log', level=logging.DEBUG)
logging.info('start scraping companies from ICRIS')

# start browser
driver = webdriver.Chrome()
driver.get("https://www.mobile-cr.gov.hk/mob/index.jsp")
driver.execute_script("loginSubscriber()")
driver.switch_to_window(driver.window_handles[1])
driver.find_element_by_name("username").send_keys("wyk747")
driver.find_element_by_name("password").send_keys("1k151k15")
try:
    driver.execute_script("document.getElementById('CHKBOX_01').checked = true;")
    driver.execute_script("validate_option()")
    driver.execute_script("forwardTo('main_s.jsp')")
    driver.execute_script("changeLocale('en_US')")
    sleep(0.5)
except:
    logout()

# start looping through each company
# load previous progress

with open(company_filename, 'r') as f:
    with open("skipped.txt", 'w') as skipped_file:

        for i, company in enumerate(f):
            try:
                driver.execute_script("forwardTo('cps_search.jsp')")
                mode = driver.find_element_by_xpath("//input[@id='mode-2']")
                driver.execute_script("arguments[0].click();", mode)
                query = driver.find_element_by_name("query")
                query.clear()
                query.send_keys(company)

                driver.find_element_by_css_selector("a[href*='selectCompany']").click()
                driver.execute_script("submitThis()")
                driver.find_element_by_xpath("//input[@value='Deduct from Account']").click()
                driver.execute_script("viewResultCPS()")

            except KeyboardInterrupt:
                logout()
                
            except:
                logging.debug("Error with scraping %s %s" % (i, company))
                print("skipped company %s %s" % (i, company))
                skipped_file.write(company)
                continue
            
            # save the webpage as html into /results
            
            try:
                filename = "results/" + '{:04}'.format(i)+ '_' + "_".join(company[:-1].split(' ')) + ".html"
                with open(filename, 'w') as f:
                    f.write(driver.page_source)

            except KeyboardInterrupt:
                logout()

            except:
                print("Error with saving %s to folder /results" % filename)

            sleep(8) # gives the webserver some rest

        logout()






