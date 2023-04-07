import time
import logging
import random

# Selenuim imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd
from bs4 import BeautifulSoup

# Define variables for origin, destination, and airline (for future customization)
global depart, arrive, departure_date, return_date, airline
depart = "LAX"
arrive = " ORD"
departure_date = "05/01/2023"
return_date = "05/07/2023"
airline = "Americanairline"

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options = options)
    return driver

def random_sleep(min_sec, max_sec):
    sleep_time = random.uniform(min_sec, max_sec)
    time.sleep(sleep_time)

def fill_form(web_id, client_input, driver, wait):
    try:
        # Locate the input field using its ID
        original_input = driver.find_element(By.ID, web_id)

        # Find the element you want to scroll to
        element_to_scroll = driver.find_element(By.CSS_SELECTOR, "#flightSearchForm\.button\.reSubmit")

        # Scroll the webpage to the element
        driver.execute_script("arguments[0].scrollIntoView();", element_to_scroll)

        # Clear the input field and enter the desired input value
        original_input.clear()
        original_input.click()
        original_input.send_keys(client_input)
        time.sleep(2)

    except Exception as err:
        # Log an error message and the exception details
        print("failed in filling form")

def page_scrape():
    flights_dict = {}

    try:
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.cell.large-3.origin")))
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.cell.large-3.destination")))
        wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span.connecting-flt-details.flight-number")))
    except Exception as err:
        print ("Error locating elements:", exc_info=True)
        return flights_dict

    # locate all elements by different div
    origin_elements = driver.find_elements(By.CSS_SELECTOR, "div.cell.large-3.origin")
    destination_elements = driver.find_elements(By.CSS_SELECTOR, "div.cell.large-3.destination")
    flight_number_elements = driver.find_elements(By.CSS_SELECTOR, "span.connecting-flt-details.flight-number")
    duration_elements = driver.find_elements(By.CSS_SELECTOR, "div.cell.large-4.pad-left-sm")
    price_elements = driver.find_elements(By.CSS_SELECTOR, "div.large-7")

    # Check that the lengths of the lists are the same
    if len(origin_elements) != len(destination_elements) or len(origin_elements) != len(flight_number_elements):
        print ("The number of elements are different")
        return flights_dict

    # Iterate through the flight_number_elements, origin_elements, and destination_elements lists,
    # extracting flight numbers, departure times, and arrival times
    for flight_number, origin, destination in zip(flight_number_elements, origin_elements, destination_elements):
        number = flight_number.text
        departure_time = origin.find_element(By.CSS_SELECTOR, "div.flt-times-sm").text
        arrival_time = destination.find_element(By.CSS_SELECTOR, "div.flt-times-sm").text

        flights_dict[number] = {
            "departure_time": departure_time,
            "arrival_time": arrival_time
        }
    return flights_dict

def export_file(flights_list, file_name):
    with open(file_name, "w") as file:
        file.write(f"This is flights info from {depart} ({departure_date}) to {arrive}({return_date}):")
        file.write("\n")
        for flight in flights_list:
            file.write(
                f"Departure Time: {flight['departure_time']} | Arrival Time: {flight['arrival_time']}")
            file.write("\n")

# URL of the website to scrape
url = "https://www.aa.com/homePage.do"
# driver = webdriver.Chrome()
driver = setup_driver()
driver.get(url)
wait = WebDriverWait(driver, 5)
wait.until(EC.visibility_of_element_located((By.ID, 'flightSearchForm.button.reSubmit')))

# Locate the origin input field
fill_form('reservationFlightSearchForm.originAirport', depart, driver, wait)
fill_form('reservationFlightSearchForm.destinationAirport', arrive, driver, wait)
fill_form('aa-leavingOn', departure_date, driver, wait)
fill_form('aa-returningFrom', return_date, driver, wait)

# Click the search button to submit the form
search_button = wait.until(EC.element_to_be_clickable((By.ID, 'flightSearchForm.button.reSubmit')))
search_button.click()
time.sleep(50)
scraped_data = page_scrape()
print(scraped_data)
export_file(scraped_data, "mini_test")