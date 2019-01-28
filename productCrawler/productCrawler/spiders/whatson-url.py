import time
import json

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

NEXT_BTN_XPATH = "//*[@class='fa fa-chevron-right']/parent::a"
NEXT_LI_XPATH = "//*[@class='fa fa-chevron-right']/parent::a/parent::li"
LIMIT_TIMEOUT = 15

PRODUCT_LOADING_TIME = 3

product_urls = []
basic_url_list = [
    'https://southaustralia.com/whats-on/',
]

def scrapavs():
    # display = Display(visible=0, size=(800, 600))
    # display.start()

    expected_next_btn = EC.visibility_of_element_located(
        (By.XPATH, NEXT_BTN_XPATH)
    )

    driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver')

    for s_url in basic_url_list:
        print(s_url, "==============================")
        try:
            i = 0
            driver.get(s_url)
            WebDriverWait(driver, LIMIT_TIMEOUT).until(expected_next_btn)
            time.sleep(PRODUCT_LOADING_TIME)

            while True:
                i = i + 1

                try:
                    temp_arr = []
                    for element in driver.find_elements_by_xpath("//li[@class='search-grid__list-item']/div/div/div/a"):
                        product_url = element.get_attribute('href')
                        # print(product_url)
                        temp_arr.append(product_url)

                    print(i, "----------", len(temp_arr))
                    product_urls.extend(temp_arr)

                    time.sleep(2)

                    # driver.find_element_by_xpath(NEXT_BTN_XPATH).click()
                    next_li_element = driver.find_element_by_xpath(NEXT_LI_XPATH)
                    if next_li_element.get_attribute('disabled'):
                        break
                    else:
                        driver.find_element_by_xpath(NEXT_BTN_XPATH).click()

                    time.sleep(2)
                    WebDriverWait(driver, LIMIT_TIMEOUT).until(expected_next_btn)
                    time.sleep(PRODUCT_LOADING_TIME)

                except Exception as e:
                    print(e, "Exception occured.")
                    break
                except TimeoutException as te:
                    print(te, "Timeout occured.")
                    break
        except TimeoutException as te:
            temp_arr = []
            for element in driver.find_elements_by_xpath("/li[@class='search-grid__list-item']/div/div/div/a"):
                product_url = element.get_attribute('href')
                # print(product_url)
                temp_arr.append(product_url)
            print(1, "----------", len(temp_arr))
            product_urls.extend(temp_arr)


    with open('whatson-url.json', 'w') as outfile:
        json.dump(product_urls, outfile)

    print("TOTAL: ", len(product_urls))

    driver.close()

if __name__ == '__main__':
    scrapavs()