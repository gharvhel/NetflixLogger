import os
import sys
from time import sleep
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Dictionary of netflix videos to watch after login in
VIDEOS = {"BlackPanther":"https://www.netflix.com/watch/80201906?trackId=14277281&tctx=0%2C0%2Caeb8ade3-36dd-4dda-aefa-5954e742db53-3950738%2C%2C"}

class Netflix():
    # Netlix Username and Password
    USER = "thecarrefam@gmail.com"
    PWD = "4thefamily"
    PROFILE = "Gharvhel"
    
    def set_up(self):
        """ Set Up selenium"""
        print("LOG: Setting Up")

        # Finding path to driver required by selenium to interface with Chrome
        dir_path = os.path.dirname(os.path.realpath(__file__))
        drvr_path = dir_path + "/chromedriver"

        # Create Chrome WebDriver
        self.driver = webdriver.Chrome(executable_path = drvr_path)

    def login(self):
        """ Login into netflix"""
        print("LOG: Logging in")

        # launch netflix
        self.driver.get("http://www.netflix.com/Login")
        assert "Netflix" in self.driver.title
        Netflix.wait(1)

        try:
            # Enter email
            elem = self.driver.find_element_by_name("userLoginId")
        except NoSuchElementException:
            elem = self.driver.find_element_by_name("email")

        elem.send_keys(Netflix.USER)

        # Enter password
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(Netflix.PWD)
        elem.send_keys(Keys.RETURN)

        # Choose profile
        print("LOG: Choosing Profile")
        Netflix.wait(1)
        elem = self.driver.find_element_by_link_text(Netflix.PROFILE)
        elem.click()

    def start_video(self, video):
        """Go to a video link after login in"""
        Netflix.wait(1)
        print("LOG: Starting Video")
        self.driver.get(video)

    def pick_resolution(self, resolution):
        """find and choose video resolution closest to given resolution"""
        # Open quality window
        Netflix.wait(3)
        pyautogui.hotkey('ctrl', 'shift', 'alt', 's')

        # Find div containing resolutions
        Netflix.wait(2)
        divs = self.driver.find_elements_by_tag_name("select")

        # Find available resolutions
        print("LOG: finding resolutions")
        all_options = divs[1].find_elements_by_tag_name("option")
        resolutions = []
        for i, option in enumerate(all_options):
            print(f"LOG: Resolution Option [{i+1}]: {option.get_attribute('value')}p")
            resolutions.append(int(option.get_attribute('value')))

        # Find resolution closest to given resolution
        best_match = min(resolutions, key=lambda x:abs(x-resolution))
        print("LOG: The closest resolution to", resolution, "is", best_match)

        # Choose best match resolution
        for option in all_options:
            if int(option.get_attribute("value")) == best_match:
                option.click()
        self.driver.find_element_by_xpath('//button[text()="Override"]').click()

    def track_stats(self):
        """Track video stats"""
        pyautogui.hotkey('ctrl', 'shift', 'alt', 'q')


    def wait_until_q(self):
        """wait until q is pressed to continue"""
        print("Enter q to quit:")
        key = input()
        while True:
            if key == "q":
                break
            print("Enter q to quit:")
            key = input()

    def tear_down(self):
        """clean up and exit"""
        self.driver.close()
        exit()

    def wait(time):
        while time > 0:
            print("LOG: Waiting", time, "second(s)")
            sleep(1)
            time -= 1

def main():
    netflix = Netflix()
    netflix.set_up()
    netflix.login()
    netflix.start_video(VIDEOS["BlackPanther"])
    netflix.pick_resolution(720)
    netflix.track_stats()
    netflix.wait_until_q()
    netflix.tear_down()

        

if __name__== '__main__':
    main()
