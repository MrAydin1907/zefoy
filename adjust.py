import time
import os
import ctypes
import platform
import webbrowser

from colorama import Fore, init, Style
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Zefoy:
    def __init__(self):
        self.driver = None
        self.captcha_box = 'ua-check'
        self.clear = "clear"

        if platform.system() == "Windows":
            self.clear = "cls"

        self.color = Fore.BLUE
        self.sent = 0
        self.xpaths = {
            "followers": "/html/body/div[6]/div/div[2]/div/div/div[2]/div/button",
            "hearts": "/html/body/div[6]/div/div[2]/div/div/div[3]/div/button",
            "comment_hearts": "/html/body/div[6]/div/div[2]/div/div/div[4]/div/button",
            "views": "/html/body/div[6]/div/div[2]/div/div/div[5]/div/button",
            "shares": "/html/body/div[6]/div/div[2]/div/div/div[6]/div/button",
            "favorites": "/html/body/div[6]/div/div[2]/div/div/div[7]/div/button",
        }

    def main(self):
        os.system(self.clear)
        self.change_title("TikTok Automator using zefoy.com | Github: @xtekky")
        print("\n" + self._print("Waiting for Zefoy to load..."))

        # Set the path to the chromedriver executable
        chromedriver_path = '/Users/yuksel/chromedriver/chromedriver'
        
        # Create a Service object
        service = Service(chromedriver_path)

        # Create a webdriver instance
        self.driver = webdriver.Chrome(service=service)

        self.driver.get("https://zefoy.com")

        #captcha_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="695cfbd4c6744e36c532bfe5d82d8f1a7cfa913b4038b0290571e79"]')
        #captcha_input.send_keys("your_captcha_text_here")

        print(self._print("Site loaded, solve the reCAPTCHA to continue."))
        self.solve_recaptcha()
        print(self._print("ReCAPTCHA solved, continuing..."))

        self.wait_for_xpath(self.xpaths["followers"])
        os.system(self.clear)
        status = self.check_status()

        print()
        print(
            self._print(f"Join our {self.color}Discord Server{Fore.WHITE} for exclusive FREE tools.")
        )
        print(
            self._print(
                f"You can also get updates when Zefoy updates the bots and more."
            )
        )
        print(self._print(f"Select your option below." + "\n"))

        counter = 1
        for thing in status:
            print(self._print(f"{thing} {status[thing]}", counter))
            counter += 1

        print(self._print(f"Discord / Support", "7"))
        option = int(input("\n" + self._print(f"")))

        if option == 1:
            div = "7"
            self.driver.find_element(By.XPATH, self.xpaths["followers"]).click()
        elif option == 2:
            div = "8"
            self.driver.find_element(By.XPATH, self.xpaths["hearts"]).click()
        elif option == 3:
            div = "9"
            self.driver.find_element(By.XPATH, self.xpaths["comment_hearts"]).click()
        elif option == 4:  
            div = "10"
            self.driver.find_element(By.XPATH, self.xpaths["views"]).click()
        elif option == 5:
            div = "11"
            self.driver.find_element(By.XPATH, self.xpaths["shares"]).click()
        elif option == 6:
            div = "12"
            self.driver.find_element(By.XPATH, self.xpaths["favorites"]).click()
        elif option == 7:
            webbrowser.open("discord.gg/onlp")
            os._exit(1)
        else:
            os._exit(1)

        video_url_box = f'/html/body/div[{div}]/div/form/div/input'
        search_box = f'/html/body/div[{div}]/div/form/div/div/button'
        vid_info = input("\n" + self._print(f"Username/VideoURL: "))

        self.send_bot(search_box, video_url_box, vid_info, div)

    def send_bot(self, search_button, main_xpath, vid_info, div):
        element = self.driver.find_element(By.XPATH, main_xpath)
        element.clear()
        element.send_keys(vid_info)
        self.driver.find_element(By.XPATH, search_button).click()
        time.sleep(15)

        ratelimit_seconds, full = self.check_submit(div)
        if "(s)" in str(full):
            self.main_sleep(ratelimit_seconds)
            self.driver.find_element(By.XPATH, search_button).click()
            time.sleep(15)

        time.sleep(15)

        send_button = f'/html/body/div[{div}]/div/div/div[1]/div/form/button'
        try:
            WebDriverWait(self.driver, 230).until(
                EC.presence_of_element_located((By.XPATH, send_button))
            )
            self.driver.find_element(By.XPATH, send_button).click()
            self.sent += 1
            print(self._print(f"Sent {self.sent} times."))

            time.sleep(15)
            self.send_bot(search_button, main_xpath, vid_info, div)
        except Exception:
            self.send_bot(search_button, main_xpath, vid_info, div)

        time.sleep(15)
        self.send_bot(search_button, main_xpath, vid_info, div)

    def main_sleep(self, delay):
        while delay != 0:
            time.sleep(1)
            delay -= 1
            self.change_title(
                f"TikTok Zefoy Automator using Zefoy.com | Cooldown: {delay}s | Github: @useragents"
            )

    def convert(self, min, sec):
        seconds = 0

        if min != 0:
            answer = int(min) * 60
            seconds += answer

        seconds += int(sec) + 5
        return seconds

    def check_submit(self, div):
        remaining = f"/html/body/div[{div}]/div/div/h4"

        try:
            element = self.driver.find_element(By.XPATH, remaining)
        except:
            return None, None

        if "READY" in element.text:
            return True, True

        if "seconds for your next submit" in element.text:
            output = element.text.split("Please wait ")[1].split(" for")[0]
            minutes = element.text.split("Please wait ")[1].split(" ")[0]
            seconds         = element.text.split("(s) ")[1].split(" ")[0]
        return int(output), self.convert(minutes, seconds)

    def check_status(self):
        followers = self.driver.find_element(By.XPATH, self.xpaths["followers"]).text
        hearts = self.driver.find_element(By.XPATH, self.xpaths["hearts"]).text
        comment_hearts = self.driver.find_element(By.XPATH, self.xpaths["comment_hearts"]).text
        views = self.driver.find_element(By.XPATH, self.xpaths["views"]).text
        shares = self.driver.find_element(By.XPATH, self.xpaths["shares"]).text
        favorites = self.driver.find_element(By.XPATH, self.xpaths["favorites"]).text

        status = {
            "Followers:": followers,
            "Hearts:": hearts,
            "Comment Hearts:": comment_hearts,
            "Views:": views,
            "Shares:": shares,
            "Favorites:": favorites,
        }

        return status
        
    def wait_for_class(self, class_name, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )

    def wait_for_xpath(self, xpath, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        print(self._print("2"))

    def solve_recaptcha(self):
        self.wait_for_class(self.captcha_box)
        self.driver.execute_script(
            "document.getElementsByClassName('captcha')[0].setAttribute('data-size', 'invisible')"
        )

        self.driver.execute_script(
            "document.getElementsByClassName('captcha')[0].setAttribute('data-badge', 'bottomright')"
        )
        print(self._print("5"))
        
        iframe_locator = (By.XPATH, "//iframe[starts-with(@src, 'https://www.google.com/recaptcha/api2/anchor')]")
        try:
        # Wait for the iframe to be present
            iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(iframe_locator))
        # Switch to the iframe
            self.driver.switch_to.frame(iframe)
        # Perform actions within the iframe
        # ...
        except Exception as e:
            print("An error occurred while solving the reCAPTCHA:", str(e))

        print(self._print("6"))

        self.wait_for_xpath('//div[@class="rc-anchor-content"]/div[@class="rc-anchor-checkbox-holder"]')
        print(self._print("7"))

        checkbox = self.driver.find_element(By.XPATH, '//div[@class="rc-anchor-content"]/div[@class="rc-anchor-checkbox-holder"]')
        print(self._print("8"))

        checkbox.click()
        print(self._print("9"))

        self.driver.switch_to.default_content()
        print(self._print("10"))

    def wait_for_xpath(self, xpath):
        WebDriverWait(self.driver, 3600).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        print(self._print("11"))

    def change_title(self, title):
        if platform.system() == "Windows":
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        else:
            print("\x1b]2;" + title + "\x07", end="")

    def _print(self, text, counter=None):
        if counter is not None:
            return f"[{counter}] {text}"
        else:
            return text

if __name__ == "__main__":
    obj = Zefoy()
    obj.main()
    input()