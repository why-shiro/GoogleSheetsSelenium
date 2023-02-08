import time

from sheetsapi import table
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
    element = None

    def __init__(self, debug: bool):
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

    def send_food(self):
        tableManager = table()
        list = tableManager.check_status()

        xt = 0
        for i in list:
            wanted = ""
            isIslem = True
            time.sleep(1)

            element = i
            if not(len(element) == 0):
                user = element[0]
                print(user)
                adrress = element[1]
                print(adrress)
                status = element[-1]
                print(status)

            if status == "Bekleniyor":
                self.loadSiteOnNewTab("https://www.google.com/maps")
                time.sleep(5)
                input_enter = self.driver.find_elements(By.XPATH, "//input[contains(@class,'tactile-searchbox-input')]")[0]
                time.sleep(1)
                input_enter.click()
                time.sleep(1)
                input_enter.send_keys(adrress)
                time.sleep(1)
                butx = self.driver.find_elements(By.XPATH, "//button[contains(@id,'searchbox-searchbutton')]")[0]
                time.sleep(1)
                butx.click()
                time.sleep(5)
                query = self.driver.find_elements(By.XPATH, "//div[contains(@role,'article')]//a")
                print("Bulunan sonuçlar: " + str(len(query)))
                time.sleep(2)
                if not (len(query) == 0):
                    query[0].click()
                    time.sleep(5)
                    copys = self.driver.find_elements(By.XPATH, "//button[contains(@data-item-id,'address')]")
                    print("Kopyalama butonu: " + str(len(copys)))
                    time.sleep(5)
                    if len(copys) == 0:
                        print("Hatalı Adres. Lütfen düzeltin")
                        new_data = [[user, adrress, "", "",
                                     "", "", "", "", "", "Hatalı Adres"]]
                        tableManager.set_status(new_data, "A" + str(xt + 2))
                        xt += 1
                        isIslem = False
                        break
                    else:
                        wanted = copys[0].get_attribute("innerText")
                else:
                    query = self.driver.find_elements(By.XPATH, "//button[contains(@data-tooltip,'Adresi kopyala')]")
                    time.sleep(1)
                    if len(query) == 0:
                        print("Adress bulunamadı!")
                    else:
                        copys = self.driver.find_elements(By.XPATH, "//button[contains(@data-tooltip,'Adresi kopyala')]")[0]
                        wanted = copys.get_attribute("innerText")

                if isIslem == True:
                    self.returnMainTab()

                    time.sleep(5)

                    name = self.driver.find_elements(By.XPATH,
                                                     "//input[contains(@class, 'bubble-element') and contains(@placeholder, '* Ad Soyad')]")[
                        0]
                    adres = self.driver.find_elements(By.XPATH,
                                                      "//input[contains(@class, 'tt-input') and contains(@placeholder, '* Adres')]")[
                        0]
                    button = self.driver.find_elements(By.XPATH,
                                                       "//button[contains(@class, 'clickable-element bubble-element')]")[
                        1]
                    textArea = self.driver.find_elements(By.XPATH, "//textarea[contains(@class, 'bubble-element')]")[0]

                    name.click()
                    time.sleep(0.3)
                    name.send_keys(user)
                    adres.click()
                    time.sleep(0.3)
                    adres.send_keys(wanted)
                    textArea.click()
                    time.sleep(0.2)
                    textArea.send_keys("Acil ilk yardım gerekli")
                    time.sleep(1)
                    button.click()

                    new_data = [[user, wanted, "", "",
                                 "", "", "", "", "", "Tamamlandı"]]

                    tableManager.set_status(new_data, "A" + str(xt + 2))
                    xt += 1
                    time.sleep(6)
                    self.driver.get("https://deprem.io/yardim-istek-enkaz")
                else:
                    print("İşleme adresten dolayı devam edilemiyor")
                    self.returnMainTab()

            else:
                print("Tamamlanan işlem")
                xt += 1

    def isAvailable(self):
        name = self.driver.find_elements(By.XPATH,
                                         "//div[contains(@class, 'bubble-element Group baTaIdg bubble-r-container flex row')]")
        if len(name) == 0:
            return False
        else:
            return True

    def loadSiteOnNewTab(self, url: str):
        self.driver.execute_script("window.open('');")
        time.sleep(1.5)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        try:
            self.driver.get(url)
        except WebDriverException:
            print("Page Down! Moving inte next page.")
