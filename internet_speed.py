from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv()
TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")
PROMISED_DOWN = int(os.environ.get("PROMISED_DOWN"))
PROMISED_UP = int(os.environ.get("PROMISED_UP"))
SPEED_TEST_EP = "https://www.speedtest.net/id"
TWITTER_EP = "https://x.com/i/flow/login"


class InternetSpeedTwitterBot:
    def __init__(self):
        self.chrome_option = webdriver.ChromeOptions()
        self.chrome_option.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_option)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get(SPEED_TEST_EP)
        time.sleep(5)
        start_button = self.driver.find_element(By.CSS_SELECTOR, value=".start-text")
        start_button.click()

        time.sleep(45)

        download = Wait(self.driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
            '.result-data-large.number.result-data-value.download-speed')))
        print(f"Download/Mbps : {download.text}")
        self.down = float(download.text)

        upload = Wait(self.driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
            '.result-data-large.number.result-data-value.upload-speed')))
        print(f"Upload/Mbps : {upload.text}")
        self.up = float(upload.text)

    def login(self):
        self.driver.get(TWITTER_EP)
        time.sleep(5)
        email = self.driver.find_element(By.NAME, value="text")
        email.send_keys(TWITTER_EMAIL)
        time.sleep(5)
        email.send_keys(Keys.ENTER)

        try:
            time.sleep(2)
            username = self.driver.find_element(By.NAME, value="text")
            username.send_keys("ComplaintsISP")
            time.sleep(2)
            username.send_keys(Keys.ENTER)
        except:
            pass

        password = Wait(self.driver, 20).until(EC.presence_of_element_located((By.NAME,"password")))
        password.send_keys(TWITTER_PASSWORD)
        time.sleep(5)
        password.send_keys(Keys.ENTER)

    def tweet_at_provider(self):
        message = (f"Hey ISP, Why is my internet speed {self.down}down/{self.up}up? "
                        f"I paid for {PROMISED_DOWN}down/{PROMISED_UP}up")

        tweet_box = Wait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/'
            'div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div'
            '/div/div/div/div/div[2]/div/div/div/div'))
        )
        tweet_box.send_keys(message)

        time.sleep(3)

        tweet_button = Wait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/'
                                                  'div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button'))
        )
        tweet_button.click()