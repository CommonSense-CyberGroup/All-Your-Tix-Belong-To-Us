#!/usr/bin/python3

'''
TITLE: The Good Bantix

BY: 
    Common Sense Cyber Group
    Some Guy they call Scooter

Version: 1.0.1

License: GNU v3

Created: 4/8/2022
Updated: 4/15/2022

Purpose:
    -Scrape differnet ticket vendors. This is a bot that will auto purchase (if configured for login) tickets and send out a notification

Considerations:
    -This script requires a lot of leg work to get to run (requirements). It was not built with ease of other users in mind, but rather security and the current running environment it was designed for

To Do:
    -Figure out wait delay for websites so we don't get hit wath an IP ban (slower up until about 2min before tickets drop, then start decreasing wait time?)

'''

### IMPORT LIBRARIES ###
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse
import threading
import colorama
import datetime
import requests


### DEFINE VARIABLES ###
ticket_list = []    #List holdling the URL to the tickets

### CLASSES AND FUNCTIONS ###
class scrappy_scraping:
    def __intit__(self, tix_vendor, sign_in_url, tix_url, tix_count):
        #Define and set up the headless selenium driver (chrome)
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path = r'../drivers/chromedriver', options = options)

        self.sign_in_url = sign_in_url
        self.tix_count = tix_count

        #Get configs for accounts
        self.tm_email, self.tm_passwd = self.read_config()

        #Begin by validating the URL given. Pass/fail will determine if bot starts
        self.check_url(self, tix_url, tix_vendor)

        #Always exit
        exit()

    #Function to read config file for account information
    def read_config():
        #Open the config file
        try:
            with open('bantix.conf') as file:
                rows = file.readlines()

                for row in rows:
                    #Ticketmaster
                    if "ticketmaster:" in row:
                        try:
                            data = row.split("ticketmaster:")[1]
                            tm_email = data.split(":")[0]
                            tm_passwd = data.split(":")[1]
                        except:
                            print(colorama.Fore.RED + "\n\t[!] ERROR - Unable to read credentials for TicketMaster in config file [!]" + colorama.Style.RESET_ALL)
                            exit()

                return tm_email, tm_passwd

        except:
            print(colorama.Fore.RED + "\n\t[!] ERROR - Unable to open config file [!]" + colorama.Style.RESET_ALL)
            exit()

    #Function for checking aspects of the URL and the web page for interaction
    def check_url(self, tix_url, tix_vendor):
        check_items = [":", "/", ".com", "http"]    #List of items to check in URL to ensure it is valid
        
        #URL is formatted properly
        for item in check_items:
            if item not in tix_url:
                print(colorama.Fore.RED + "\n\t[!] ERROR - URL entered was not valid for vendor " + tix_vendor + "[!]" + colorama.Style.RESET_ALL)
                exit()

        #URL gives us a valid return code
        response = requests.get(tix_url)

        if response.status_code != 200:
            print(colorama.Fore.RED + "\n\t[!] ERROR - URL check did not give a 200 status code [!]" + colorama.Style.RESET_ALL)
            exit()

        #URL check passed. Start the bot
        self.gimme_gimme(self, tix_url, tix_vendor)

    #Function to actualy do the scraping and buy the tickets
    def gimme_gimme(self, tix_url, tix_vendor):
        
        #Bot process based on vendor
        if tix_vendor == "TicketMaster":
            ticketmaster(tix_vendor, tix_url)

        #Function for scraping tickets from TicketMaster
        def ticketmaster():
            #Sign in first:
            self.driver.get(self.sign_in_url)

            self.driver.find_element_by_name("email").send_keys(self.tm_email)
            self.driver.find_element_by_name("password").send_keys(self.tm_passwd)
            self.driver.find_element_by_name("sign-in").click()

            #Try/except to ensure we are logged in
            try:
                self.driver.find_element_by_name("My Account")
            except:
                print(colorama.Fore.RED + "\n\t[!] ERROR - Unable to log in using configured credentials for " + tix_vendor + " [!]" + colorama.Style.RESET_ALL)
                exit()

            #Kick off selenium headless and do the thing
            self.driver.get(tix_url)



### THE THING ###
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-tm", "--ticket-master", dest="ticket_master", help="Enter URL of ticket page that you wish to purchase. Scrapes only Ticket Master for tickets.", required=False, type=str) #Searches for tickets on Ticket Master only
        parser.add_argument("-c", "--ticket-count", dest="count", help="Number of tickets to be purchased (ON EACH VENDOR if ran against more than one!!)", required=True, type=int) #Number of tickets to be purchased
        args = parser.parse_args()

        #Error checking to make sure that a site has been chosen to check for tickets
        if args.ticket_master is not None:
            ticket_list.append(args.ticket_master)
            url_list = {"TicketMaster":"https://auth.ticketmaster.com/as/authorization.oauth2?client_id=8bf7204a7e97.web.ticketmaster.us&response_type=code&scope=openid%20profile%20phone%20email%20tm&redirect_uri=https://identity.ticketmaster.com/exchange&visualPresets=tm&lang=en-us&placementId=discovery&hideLeftPanel=false&integratorId=prd1224.ccpDiscovery&intSiteToken=tm-us&deviceId=vU49VxOT9DU4Oj09Pj4%2BPTY5OTiTuFpGqTDxTA"}
        else:
            print(colorama.Fore.RED + "\n\t[!] ERROR - You must make a selection of which ticket vendor to search and input a URL [!]" + colorama.Style.RESET_ALL)
            quit()

        #Run like the wind
        i = 0
        for vendor, sign_in_url in url_list.items():
            threading.Thread(target = scrappy_scraping, args = (vendor, sign_in_url, ticket_list[i], args.count,))
            i += 1
    
    except:
        quit()