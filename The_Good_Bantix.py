#!/usr/bin/python3

'''
TITLE: The Good Bantix

BY: 
    Common Sense Cyber Group
    Some Guy they call Scooter

Version: 1.0.1

License: GNU v3

Created: 4/8/2022
Updated: 4/8/2022

Purpose:
    -

Considerations:
    -This script requires a lot of leg work to get to run (requirements). It was not built with ease of other users in mind, but rather security and the current running environment it was designed for

To Do:
    -Figure out wait delay for websites so we don't get hit wath an IP ban (slower up until about 2min before tickets drop, then start decreasing wait time?)

'''

### IMPORT LIBRARIES ###
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse
import subprocess
import colorama
import datetime


### DEFINE VARIABLES ###
base_ticket_master = "" 
url_list = [base_ticket_master]   


#Define Selenium headless options to run in the background
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path = '../drivers/chromedriver', options = options)


### CLASSES AND FUNCTIONS ###



### THE THING ###
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", dest="all", help="Scrapes ALL ticket sites for tickets.", required=False, type=str) #Searches for provided tickets on ALL urls ()
    parser.add_argument("-tm", "--ticket-master", dest="ticket_master", help="Scrapes only Ticket Master for tickets.", required=False, type=str) #Searches for tickets on Ticket Master only
    args = parser.parse_args()

    #Error checking to make sure that a site has been chosen to check for tickets
    if args.ticket_master is not None:
        print()
    elif args.all is not None:
        print()

    #Fetch URL
    driver.get(base_ticket_master)


    print('Page title: ' + driver.title)

    #Quit to stay clean
    driver.quit()