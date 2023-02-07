import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import xlsxwriter


class SearchEngine:
    driver = None
    account_links = None
    workbook = None
    worksheet = None
    element = None

    def __init__(self, debug: bool):
        self.workbook = xlsxwriter.Workbook('values.xlsx')
        self.worksheet = self.workbook.add_worksheet("Mined Elements")
        options = Options()
        options.page_load_strategy = 'eager'
        disableInfoBar = ['enable-automation']
        options.add_experimental_option('excludeSwitches', disableInfoBar)
        # options.add_argument("--headless")
        if debug:
            options.add_argument("--force-device-scale-factor=0.1")
        else:
            options.add_argument("--force-device-scale-factor=1")

        """try:
            options.add_extension('Buster.crx')
            print("Extension setup completed.")
        except:
            print("Extension setup has failed! Please check extension file is installed!")"""

        self.driver = webdriver.Chrome(options=options)
        print(self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])
        self.account_links = []

    def load_site(self, url: str):
        try:
            self.driver.get(url)
        except Exception as e:
            print("An error occured while trying to open website: " + url)
            print(str(e))

    def returnMainTab(self):
        time.sleep(1.5)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


    def list_all_beta(self):
        """childs = x[0].find_elements(By.XPATH,".//div[contains(@class,'_4lg0 _4lg5 _4h2p _4h2m')]")
                name = x[0].find_elements(By.XPATH, ".//a[contains(@class,'xt0psk2 x1hl2dhg xt0b8zv x8t9es0 x1fvot60 xxio538 xjnfcd9 xq9mrsl x1yc453h x1h4wwuj x1fcty0u') and contains(@aria-label,'Open ad object to view children in the table')]")
                print(name[0].get_attribute("innerText"))
                for i in range(len(childs)):
                    print(childs[i].get_attribute("innerText"))"""

