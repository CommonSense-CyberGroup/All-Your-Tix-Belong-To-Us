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
    -Scrape differnet ticket vendors. This is a bot that will auto purchase (if configured for login) tickets and send out a notification

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
import requests


### DEFINE VARIABLES ###


### CLASSES AND FUNCTIONS ###
class scrappy_scraping:
    def __intit__(self, tix_vendor, url):
        #Define and set up the headless selenium driver (chrome)
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path = r'../drivers/chromedriver', options = options)

        #Begin by validating the URL given. Pass/fail will determine if bot starts
        valid_url = self.check_url(self, url, tix_vendor)

        #Always exit
        exit()

    #Function for checking aspects of the URL and the web page for interaction
    def check_url(self, url, tix_vendor):
        check_items = [":", "/", ".com", "http"]    #List of items to check in URL to ensure it is valid
        
        #URL is formatted properly
        for item in check_items:
            if item not in url:
                print(colorama.Fore.RED + "\n\t[!] ERROR - URL entered was not valid for vendor " + tix_vendor + "[!]" + colorama.Style.RESET_ALL)
                quit()

        #URL gives us a valid return code
        response = requests.get(url)

        if response.status_code != 200:
            print(colorama.Fore.RED + "\n\t[!] ERROR - URL check did not give a 200 status code [!]" + colorama.Style.RESET_ALL)
            quit()

        #URL check passed. Start the bot
        self.gimme_gimme(url, tix_vendor)

    #Function to actualy do the scraping and buy the tickets
    def gimme_gimme(url, tix_vendor):
        print()


### THE THING ###
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-tm", "--ticket-master", dest="ticket_master", help="Enter URL of ticket page that you wish to purchase. Scrapes only Ticket Master for tickets.", required=False, type=str) #Searches for tickets on Ticket Master only
        parser.add_argument("-c", "--ticket-count", dest="count", help="Number of tickets to be purchased (ON EACH VENDOR if ran against more than one!!)", required=True, type=int) #Number of tickets to be purchased
        args = parser.parse_args()

        #Error checking to make sure that a site has been chosen to check for tickets
        if args.ticket_master is not None:
            url_list = {"TicketMaster":"base_ticket_master_URL"}
        else:
            print(colorama.Fore.RED + "\n\t[!] ERROR - You must make a selection of which ticket vendor to search and input a URL [!]" + colorama.Style.RESET_ALL)
            quit()

        #Run like the wind
        for vendor, url in url_list.items():
            scrappy_scraping(vendor, url)
    
    except:
        quit()