import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless")

base_url = "https://auto.ria.com/uk/car/used/"
_driver = webdriver.Chrome(options=options)


def scrape_cars_data(_driver, url_car):
    resp = requests.get(url_car).text
    car_soup = BeautifulSoup(resp, "html.parser")

    _driver.get(url_car)
    time.sleep(5)

    deleted_notice = _driver.find_elements(By.CSS_SELECTOR, "div.notice_head")

    if deleted_notice:
        print("Announcement removed")
        return None

    try:
        cross_element = WebDriverWait(_driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "phone_show_link"))
        )
        _driver.execute_script("arguments[0].click();", cross_element)
        phone_element = _driver.find_element(By.CSS_SELECTOR, "span[data-phone-number]")
    except NoSuchElementException:
        print("The 'phone_show_link' element was not found on this page")
        return None

    image_count_element = car_soup.select_one(".preview-gallery a.show-all")
    price_usd_str = car_soup.select_one(".price_value").text

    data = {
        "url": url_car,
        "title": car_soup.select_one(".auto-content_title").text,
        "price_usd": int(''.join(re.findall(r'\d+', price_usd_str))),
        "odometer": int(car_soup.select_one("span.size18").text) * 1000,
        "username": car_soup.select_one(".seller_info_name").text.strip(),
        "phone_number": phone_element.get_attribute("data-phone-number"),
        "image_url": car_soup.select_one("div.gallery-order img.outline").get("src"),
        "image_count": int(image_count_element.text.split()[2])
        if image_count_element else None,
        "car_number": car_soup.select_one(".t-check span.state-num").text.replace(" ", "")[:8]
        if (car_soup.select_one(".t-check span.state-num")) else "",
        "car_vin": car_soup.select_one(".t-check").text.split()[-1],
    }

    return data


def get_total_pages(page_limit=None, is_testing=False):
    _driver.get(base_url)
    next_button = _driver.find_element(By.CSS_SELECTOR, "a.page-link.js-next")
    total_pages = 1

    while (page_limit is None or total_pages < page_limit) and next_button.is_enabled():
        _driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(10)

        next_button.click()

        WebDriverWait(_driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.page-link.js-next"))
        )

        next_button = _driver.find_element(By.CSS_SELECTOR, "a.page-link.js-next")

        total_pages += 1

        if is_testing:
            break

    return total_pages


def get_urls_cars(_driver, page_limit=None):
    all_urls = []
    num_pages = get_total_pages(page_limit=5)

    if page_limit is not None:
        num_pages = min(page_limit, num_pages)

    for page in range(1, num_pages + 1):
        _driver.get(base_url + f"?page={page}")

        time.sleep(10)

        response = _driver.page_source
        soup = BeautifulSoup(response, "html.parser")
        urls_on_page = [
            url_car.get("href") for url_car in soup.select("div.content a.address")
        ]
        all_urls.extend(urls_on_page)

    return all_urls


def get_all_info_cars(_driver):
    all_cars_data = []
    urls = get_urls_cars(_driver=_driver)

    for url_car in urls:
        car_data = scrape_cars_data(_driver, url_car)
        if car_data:
            all_cars_data.append(car_data)

    return all_cars_data
