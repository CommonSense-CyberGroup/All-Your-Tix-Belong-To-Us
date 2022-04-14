#!/usr/bin/python3

'''
TITLE: The Good Bantix

BY: 
    Common Sense Cyber Group
    Some Guy they call Scooter

Version: 1.0.1

License: GNU v3

Created: 4/8/2022
Updated: 4/14/2022

Purpose:
    -

Considerations:
    -This script requires a lot of leg work to get to run (requirements). It was not built with ease of other users in mind, but rather security and the current running environment it was designed for

To Do:
    -Figure out wait delay for websites so we don't get hit wath an IP ban (slower up until about 2min before tickets drop, then start decreasing wait time?)
    -How are we going to tell the script what tickets to search for?

    -How to subprocess a class? Or are we going to need to use threading?

'''

### IMPORT LIBRARIES ###
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse
import subprocess
import colorama
import datetime


### DEFINE VARIABLES ###


#Define Selenium headless options to run in the background



### CLASSES AND FUNCTIONS ###
class scrappy_scraping:
    def __intit__(self, tix_vendor, url):
        #Define and set up the headless selenium driver (chrome)
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path = r'../drivers/chromedriver', options = options)

        #Begin by validating the URL given as well as ensuring that we are able to refresh the page, click on things, and visit the cart
        self.check_url()

    #Function for checking aspects of the URL and the web page for interaction
    def check_url():
        print()




### THE THING ###
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "--all", dest="all", help="Scrapes ALL ticket sites for tickets.", required=False, type=str) #Searches for provided tickets on ALL urls ()
        parser.add_argument("-tm", "--ticket-master", dest="ticket_master", help="Scrapes only Ticket Master for tickets.", required=False, type=str) #Searches for tickets on Ticket Master only
        args = parser.parse_args()

        #Error checking to make sure that a site has been chosen to check for tickets
        if args.ticket_master is not None:
            url_list = {"TicketMaster":"base_ticket_master_URL"}
        elif args.all is not None:
            url_list = {"TicketMaster":"base_ticket_master_URL"}
        else:
            print(colorama.Fore.RED + "\n\t[!] ERROR - You must make a selection of which ticket vendor to search [!]")
            quit()

        #Run like the wind
        for vendor, url in url_list.items():
            scrappy_scraping(vendor, url)
    
    except:
        quit()