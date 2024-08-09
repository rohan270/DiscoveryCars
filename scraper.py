import json
import logging
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_json_file(cars_list, filename='data.json'):
    try:
        # Load existing data from the JSON file
        try:
            with open(filename, 'r') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            existing_data = []

        # Append new data to existing data
        existing_data.extend(cars_list)

        # Write updated data back to the JSON file
        with open(filename, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
        
        logging.info(f'Data has been written to {filename}')
    except Exception as e:
        logging.error(f'Failed to write to {filename}: {e}')


def find_cars_cars24mumbai():
    base_url = 'https://www.cars24.com/buy-used-cars-mumbai/'
    
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    service = Service("C:\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    page_num = 1
    cars_list = []

    while True:
        for _ in range(5):  # Scrape 5 pages at a time
            url = f'{base_url}?page={page_num}'
            driver.get(url)

            try:
                logging.info('Waiting for the page to load...')
                wait = WebDriverWait(driver, 20)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'RPKrE')))
                time.sleep(15)

                logging.info('Scrolling the page...')
                body = driver.find_element(By.TAG_NAME, 'body')
                for _ in range(3):
                    body.send_keys(Keys.END)
                    time.sleep(10)

                logging.info('Parsing the page source...')
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                cars_info = soup.find_all('a', class_='IIJDn')

                logging.info('Extracting car details...')
                for car_info in cars_info:
                    car_title = car_info.find('h3', class_='_11dVb').text.strip() if car_info.find('h3', class_='_11dVb') else 'No title available'
                    car_details = ' '.join([li.text.strip() for li in car_info.find('ul', class_='_3J2G-').find_all('li')]) if car_info.find('ul', class_='_3J2G-') else 'No details available'
                    car_price = car_info.find('div', class_='_2KyOK').text.strip() if car_info.find('div', class_='_2KyOK') else 'No price available'
                    more_info = car_info['href'] if 'href' in car_info.attrs else 'No details available'

                    car_dict = {
                        'title': car_title,
                        'details': car_details,
                        'price': car_price,
                        'link': more_info,
                        'image_url': 'No image available'
                    }
                    cars_list.append(car_dict)

                logging.info('Extracting images...')
                car_pictures = soup.find_all('div', class_='RPKrE')
                for car_picture in car_pictures:
                    parent_anchor = car_picture.find_parent('a', class_='IIJDn')
                    if parent_anchor:
                        car_image_tag = car_picture.find('img')
                        car_image_url = car_image_tag['src'] if car_image_tag else 'No image available'
                        for car in cars_list:
                            if car['link'] == parent_anchor['href']:
                                car['image_url'] = car_image_url
                                break

                page_num += 1

            except Exception as e:
                logging.error(f'An error occurred: {e}')
                break

        if not cars_list:
            break  # Exit if no cars were found in the last batch

        logging.info('Updating data.json with new data...')
        update_json_file(cars_list)
        cars_list = []

    driver.quit()


def find_cars_cars24delhi():
    base_url = 'https://www.cars24.com/buy-used-car/?sort=bestmatch&serveWarrantyCount=true&gaId=1476729337.1720017156&storeCityId=2'
    
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    service = Service("C:\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    page_num = 1
    cars_list = []

    while True:
        for _ in range(5):  # Scrape 5 pages at a time
            url = f'{base_url}&page={page_num}'
            driver.get(url)

            try:
                logging.info('Waiting for the page to load...')
                wait = WebDriverWait(driver, 20)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'RPKrE')))
                time.sleep(15)

                logging.info('Scrolling the page...')
                body = driver.find_element(By.TAG_NAME, 'body')
                for _ in range(3):
                    body.send_keys(Keys.END)
                    time.sleep(10)

                logging.info('Parsing the page source...')
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                cars_info = soup.find_all('a', class_='IIJDn')

                logging.info('Extracting car details...')
                for car_info in cars_info:
                    car_title = car_info.find('h3', class_='_11dVb').text.strip() if car_info.find('h3', class_='_11dVb') else 'No title available'
                    car_details = ' '.join([li.text.strip() for li in car_info.find('ul', class_='_3J2G-').find_all('li')]) if car_info.find('ul', class_='_3J2G-') else 'No details available'
                    car_price = car_info.find('div', class_='_2KyOK').text.strip() if car_info.find('div', class_='_2KyOK') else 'No price available'
                    more_info = car_info['href'] if 'href' in car_info.attrs else 'No details available'

                    car_dict = {
                        'title': car_title,
                        'details': car_details,
                        'price': car_price,
                        'link': more_info,
                        'image_url': 'No image available'
                    }
                    cars_list.append(car_dict)

                logging.info('Extracting images...')
                car_pictures = soup.find_all('div', class_='RPKrE')
                for car_picture in car_pictures:
                    parent_anchor = car_picture.find_parent('a', class_='IIJDn')
                    if parent_anchor:
                        car_image_tag = car_picture.find('img')
                        car_image_url = car_image_tag['src'] if car_image_tag else 'No image available'
                        for car in cars_list:
                            if car['link'] == parent_anchor['href']:
                                car['image_url'] = car_image_url
                                break

                page_num += 1

            except Exception as e:
                logging.error(f'An error occurred: {e}')
                break

        if not cars_list:
            break  # Exit if no cars were found in the last batch

        logging.info('Updating data.json with new data...')
        update_json_file(cars_list)
        cars_list = []

    driver.quit()


def find_cars_droom():
    base_url = 'https://droom.in/cars'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    page_num = 1
    cars_list = []

    while True:
        for _ in range(5):  # Scrape 5 pages at a time
            url = f'{base_url}?page={page_num}'

            try:
                logging.info('Sending request to the website...')
                response = requests.get(url, headers=headers)
                response.raise_for_status()

                logging.info('Parsing the page content...')
                soup = BeautifulSoup(response.content, 'html.parser')

                cars_grid = soup.find_all('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-4')

                logging.info('Extracting car details...')
                for car_grid in cars_grid:
                    car_info = car_grid.find('div', class_='jss236')
                    if car_info:
                        car_title_elem = car_info.find('h3', class_='MuiTypography-root jss237 MuiTypography-body1')
                        car_details_elems = car_info.find_all('div', class_='jss242')
                        car_price_elem = car_info.find('div', class_='MuiGrid-root MuiGrid-container')
                        car_link_elem = car_info.find('a', href=True)

                        car_title = car_title_elem.text.strip() if car_title_elem else 'No title available'
                        car_details = ' '.join([elem.text.strip() for elem in car_details_elems]) if car_details_elems else 'No details available'
                        car_price = car_price_elem.text.strip() if car_price_elem else 'No price available'
                        car_link = car_link_elem['href'] if car_link_elem else 'No details available'

                        car_dict = {
                            'title': car_title,
                            'details': car_details,
                            'price': car_price,
                            'link': car_link,
                            'image_url': 'No image available'
                        }
                        cars_list.append(car_dict)

                page_num += 1

            except Exception as e:
                logging.error(f'An error occurred: {e}')
                break

        if not cars_list:
            break  # Exit if no cars were found in the last batch

        logging.info('Updating data.json with new data...')
        update_json_file(cars_list)
        cars_list = []

def update_json_file(cars_list):
    try:
        with open('data.json', 'w') as json_file:
            json.dump(cars_list, json_file, indent=4)
        logging.info('Data has been written to data.json')
    except Exception as e:
        logging.error(f'Failed to write to data.json: {e}')


if __name__ == '__main__':
    find_cars_cars24mumbai()
    find_cars_cars24delhi()
    find_cars_droom()
