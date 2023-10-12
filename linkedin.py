from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://www.linkedin.com/search/results/people/?geoUrn=%5B%22102264497%22%5D&keywords=HR&origin=FACETED_SEARCH&sid=%403d"

username = "t5004213@gmail.com"
password = "QtYg2xwQRPrymN01xUZv"


# enter signin
driver.get("https://www.linkedin.com/login/ru?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
time.sleep(2)

# enter account
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")
username_field.send_keys(username)
password_field.send_keys(password)

login_button = driver.find_element(By.CLASS_NAME, "login__form_action_container ")
login_button.click()
time.sleep(3)

driver.get(url)
time.sleep(3)

data = {}

pages = driver.find_element(By.XPATH, "//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']/*[last()]/*/span").text
count = 1
for i in range(1, int(pages) + 1):
    try:
        items = driver.find_elements(By.XPATH, "//div[@class='entity-result__item']")
        for item in items:
            account = item.find_element(By.XPATH, ".//a[@class='app-aware-link  scale-down ']").get_attribute("href")

            try:
                image = item.find_element(By.XPATH, ".//div[@class='presence-entity presence-entity--size-3']//img").get_attribute("src")
            except:
                image = 'Не указано'

            job = item.find_element(By.XPATH, ".//div[@class='entity-result__primary-subtitle t-14 t-black t-normal']").text
            try:
                city = item.find_element(By.XPATH, ".//div[@class='entity-result__secondary-subtitle t-14 t-normal']").text
            except:
                city = 'Не указано'

            try:
                description = item.find_element(By.XPATH, ".//p").text
            except:
                description = 'Не указано'

            item_data = {
                "id": count,
                "account": account,
                "image": image,
                "job": job,
                "city": city,
                "description": description
            }

            count += 1
            data[item_data['id']] = item_data

        next_page_button = driver.find_element(By.XPATH, f"//button[@aria-label='Страница {i+1}']")
        next_page_button.click()
        time.sleep(3)

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)