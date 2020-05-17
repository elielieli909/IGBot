# USAGE =========================================================
# python3 main.py *username* *password* *account1* *account2* ...

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

from time import sleep, ctime
import sys
import random

# Instagram allows 160 follows/hour, or 1 follow every 22.5 seconds

INSTAGRAM_URL='https://www.instagram.com/'

class Bot():
    def __init__(self):
        # Create a headless browser
        opts = Options()
        #opts.headless = True    
        self.browser = Firefox(options=opts)
        # so as not to try and find things before they're loaded
        self.browser.implicitly_wait(3)
        self.browser.get(INSTAGRAM_URL)
        
        self.numFollowed = 0

    def login(self, username, password):
        # Sleep to ensure page is loaded
        #sleep(2)
        inputs = self.browser.find_elements_by_tag_name('input')
        # Username
        inputs[0].clear()
        inputs[0].send_keys(username)
        # Password
        inputs[1].clear()
        inputs[1].send_keys(password)
        # Login
        inputs[1].send_keys(Keys.RETURN)
        sleep(2)

    def start_following(self, accounts):
        for account in accounts:
            # Go to their page
            self.browser.get(INSTAGRAM_URL + account)
            sleep(2)

            followers_button = self.browser.find_element_by_partial_link_text('followers')
            followers_button.click()
            sleep(1)

            buttons = self.browser.find_elements_by_tag_name('button')
            # first 4 buttons are not what we want
            buttons = buttons[4:]
            sleep(1)
            # Follow everybody on this account
            for button in buttons:
                if button is buttons[0]:
                    continue
                button.click()
                self.numFollowed += 1
                # This averages to 1 follow every 22.5 seconds, but its random so not super sus
                #sleeptime = random.randint(15, 30)
                #sleep(sleeptime)

            print("Followed " + str(self.numFollowed) + " accounts who follow " + account)




# Arguments should be username, password, [accounts to follow]
def main():
    if len(sys.argv) < 4:
        print('ERROR: Missing arguments')
        sys.exit()

    # Get all the info from the command line args
    username = sys.argv[1]
    password = sys.argv[2]

    accounts = []
    i = 3
    while i < len(sys.argv):
        accounts.append(sys.argv[i])
        i += 1

    # Initiate the bot class
    bot = Bot()
    bot.login(username, password)
    bot.start_following(accounts)

if __name__ == "__main__":
    main()