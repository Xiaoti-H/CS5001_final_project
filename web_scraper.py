'''
This Python file scrapes American Airlines flight data for a specified travel
airports and dates, exporting data to a CSV or TXT file.

Classes:
    FlightsData
    DataExport

NAME: Xiaoti Hu
SEMESTER: 2023 Spring
'''

import time
import logging
import random

# Selenuim imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Other tools for web data scraping
# pandas for csv exporting, beautifulsoup for data scrape
import pandas as pd
from bs4 import BeautifulSoup

# Define variables for origin, destination, and airline
# (for future customization)
global depart, arrive, departure_date, return_date, airline

'''
depart = "SJC"
arrive = "LAS"
departure_date = "08/25/2023"
return_date = "09/01/2023"
'''


class FlightsData:
    """
    A class to scrape flight data from the American Airlines,
    including departure and arrival times, durations, and prices for
    various fare classes.
    """

    def __init__(self, depart, arrive,
                 departure_date, return_date=None,
                 trip_type="round trip", airline="AmericanAirline"):
        """
            Initializes the FlightsData class with the provided input data.

             Args:
                depart (str): The departure airport.
                arrive (str): The arrival airport.
                departure_date (str): The departure date in MM/DD/YYYY format.
                return_date (str, optional): The return date in MM/DD/YYYY format. Defaults to None.
                trip_type (str, optional): The type of trip ("round trip" or "one way"). Defaults to "round trip".
                airline (str, optional): The airline to scrape data for. Defaults to "AmericanAirline".
        """
        # self.price = price
        self.depart = depart
        self.arrive = arrive
        self.departure_date = departure_date
        self.return_date = return_date
        self.trip_type = trip_type
        self.airline = airline
        self.driver = self.setup_driver()
        self.wait = WebDriverWait(self.driver, 5)

    def setup_driver(self):
        """
        Sets up the Selenium WebDriver with the necessary options.

        Returns: webdriver.Chrome(A configured Selenium WebDriver).
        """
        options = webdriver.ChromeOptions()
        # hidden the webdriver info
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(options=options)
        return driver

    def random_sleep(self, min_sec, max_sec):
        """
        Sleeps for a random number within minimal and maximum seconds provided
        by custom.(mimic human's action or leave a reasonable loading time for driver)

        Args: min_sec (float): The minimum number of seconds to sleep.
              max_sec (float): The maximum number of seconds to sleep.
        """

        sleep_time = random.uniform(min_sec, max_sec)
        time.sleep(sleep_time)

    def fill_form(self, web_id, client_input):
        """
        Fills a form field on the web page with the provided input.

        Args:
            web_id (str): The ID of the form field to fill.
            client_input (str): The input to fill the form field with.
        """
        try:
            # Locate the input field using its ID
            original_input = self.driver.find_element(By.ID, web_id)
            # Find the element you want to scroll to
            element_to_scroll = self.driver.find_element(By.CSS_SELECTOR, "#flightSearchForm\.button\.reSubmit")
            # Scroll to the element
            self.driver.execute_script("arguments[0].scrollIntoView();", element_to_scroll)

            # Clear the default input field and enter the desired value
            original_input.clear()
            original_input.click()
            original_input.send_keys(client_input)
            self.random_sleep(1, 3)

        except Exception as e:
            # Log an error message and the exception details
            logging.error(e, exc_info=True)

    def extract_info(self, classname: str, container="div") -> list:
        """
        Extracts all elements with a specified CSS class name
        and container tag from the current web page's source code.

        Args:
            classname (str): The CSS class name to search for.
            container (str, optional): The HTML tag name of
                      the container element to search within.
                      Defaults to "div".

        Returns: A list of all elements that match the specified CSS
                 class name and container tag.
        """
        # creates a BeautifulSoup object by parsing the HTML content of the webpage.
        # in this case, the built-in Python "html.parser" is used.
        bs = BeautifulSoup(self.driver.page_source, "html.parser")
        return bs.find_all(container, class_=classname)

    def get_price(self, prices, index):
        """
            Gets the price at the specified aircraft class from the prices list,
            or returns "N/A" if the class is not available.

            Args:
                prices (list): The list of prices.
                index (int): The index of the desired price.

            Returns:
                str: The price at the specified aircraft class,
                     or "N/A" if the index is out of range.
        """
        try:
            return prices[index].text.strip()
        except IndexError as e:
            return "N/A"

    @staticmethod
    def find_text(block: list, class_name: str, container="div"):
        """
        Finds the text within an element with the specified CSS class name
        and container tag within a block.

        Args:
            block (list): The block to search within.
            class_name (str): The CSS class name to search for.
            container (str, optional): The HTML tag name of the container element
                                       to search within. Defaults to "div".

        Returns:
            str: The text within the found element.
        """
        return block.find(container, class_=class_name).get_text().strip()

    def get_flight_cards(self):
        """
        Gets all the flight cards from the current web page.

        Returns: list: A list of all flight card elements.
        """
        # 'WebDriverWait' object with a 5 seconds to wait for a specific
        # condition to be satisfied before interacting with them in the script.
        # helps the script to be more robust and prevent failures
        # due to slow-loading elements.
        wait = WebDriverWait(self.driver, 5)
        return wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR,
             "#aa-content > div > app-results-grid-desktop > div > virtual-scroller > div.scrollable-content > div.results-grid-container > div")
        ))

    def extract_flight_details(self, flight_card):
        """
        Extracts flight details from a flight card.
        Target items are: flight number, departure_time, arrival_time,
                                duration, price_element
        Args:
            flight_card (WebElement): The flight cards to extract flight details from.

        Returns:
            tuple: A tuple containing the extracted flight details
                  (flight, departure_time, arrival_time, duration, price_element).
            """
        # find sub-field in each flight card
        origin = flight_card.find_element(By.CSS_SELECTOR, "div.cell.large-3.origin")
        destination = flight_card.find_element(By.CSS_SELECTOR, "div.cell.large-3.destination")
        duration_element = flight_card.find_element(By.CSS_SELECTOR, "div.cell.large-4.pad-left-sm")
        price_element = flight_card.find_element(By.CSS_SELECTOR, "app-choose-flights-price-desktop")

        # extract targeted information from related fields,
        # the connection flights will contain more than 1 flight number
        # so here we create a list for all flight numbers.
        flights = flight_card.find_elements(By.CSS_SELECTOR, "span.connecting-flt-details.flight-number")
        flight = [number.text for number in flights]

        # extract text by locating CSS_SELECTORs
        departure_time = origin.find_element(By.CSS_SELECTOR, "div.flt-times-sm").text
        arrival_time = destination.find_element(By.CSS_SELECTOR, "div.flt-times-sm").text
        duration = duration_element.find_element(By.CSS_SELECTOR, "div.duration").text

        return flight, departure_time, arrival_time, duration, price_element

    def process_prices(self, prices):
        """
        Extract price for different class from lists of price elements.
        Treat various cabin conditions

        Args: prices (list): The list of price elements.

        Returns:
            tuple: A tuple containing the processed prices
                  (basic_economy_price, main_cabin_price, first_class_price).
        """
        if len(prices) == 3:
            basic_economy_price = self.get_price(prices, 0)
            main_cabin_price = self.get_price(prices, 1)
            first_class_price = self.get_price(prices, 2)
        else:
            basic_economy_price = "N/A"
            main_cabin_price = self.get_price(prices, 0)
            first_class_price = self.get_price(prices, 1)

        return basic_economy_price, main_cabin_price, first_class_price

    def page_scrape(self, flight_card_elements=None):
        """
        Scrapes flight data from the current web page and stores it in a dictionary.

        Returns:
            dict: A dictionary containing the scraped flight data.
        """
        # create an empty dictionary for all flight information
        flights_dict = {}
        # Set an index for output, from the first flight option to last in this page
        flight_id = 1

        # If no flight_card_elements provided, call get_flight_cards() to get cards from webpage
        if flight_card_elements is None:
            flight_card_elements = self.get_flight_cards()

        # Check if flight_card_elements is of the correct datatype (list)
        if not isinstance(flight_card_elements, list):
            raise TypeError("'flight_card_elements' is not of the correct datatype(list).")

        # iterating each flight card in flight_cards to extract relevant details
        for flight_card in flight_card_elements:
            # unpack tuple
            flight, departure_time, arrival_time, duration, price_element = self.extract_flight_details(flight_card)
            prices = price_element.find_elements(By.CSS_SELECTOR, "span.per-pax-amount.ng-star-inserted")
            basic_economy_price, main_cabin_price, first_class_price = self.process_prices(prices)

            flights_dict[flight_id] = {
                "flight_numbers": flight,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "duration": duration,
                "main_cabin_price": main_cabin_price,
            }
            flight_id += 1

        return flights_dict

    def run(self):
        """
        Runs the entire process of scraping flight data from the specified URL and exporting it to a CSV file.

        Returns:
            str: The name of the generated CSV file. (for flask  in app.py)
            """
        # Navigate to the URL
        url = "https://www.aa.com/homePage.do"

        # locate and fill the form
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located((By.ID, 'flightSearchForm.button.reSubmit')))

        # Fill the form
        self.fill_form('reservationFlightSearchForm.originAirport', self.depart)
        self.fill_form('reservationFlightSearchForm.destinationAirport', self.arrive)
        self.fill_form('aa-leavingOn', self.departure_date)
        self.fill_form('aa-returningFrom', self.return_date)

        # Click the search button to submit the form
        search_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'flightSearchForm.button.reSubmit')))
        search_button.click()
        # Adjust sleep time as needed
        self.random_sleep(30, 50)

        # Scrape data from the page
        scraped_data = self.page_scrape()

        # export csv file
        csv_name = f"{self.depart}to{self.arrive}.csv"
        data_exporter = DataExport(csv_name, scraped_data)
        data_exporter.export_to_csv()

        # Close the driver after finishing
        self.driver.quit()

        return csv_name


class DataExport:
    """
    This class handle the exporting of flight data int various formats.
    Currently supports exporting to CSV and TXT files.
    The class takes a file_name and a flights_dict as input arguments.
    """

    def __init__(self, file_name, flights_dict):
        """
        Initializes the DataExport class with a file name
        and a dictionary containing flight data.

        Args: file_name: str, name of the output file
              flights_dict: private dictionary containing flight information
                            (prevent unexpected changes)
        """
        self.file_name = file_name
        self._flights_dict = flights_dict

    def export_to_csv(self):
        """
        Exports flight data to a CSV file using the provided file_name.

        return: str, the file path of the exported CSV file, or None if an exception occurs
        """
        try:
            # Convert the dictionary to a Pandas DataFrame
            df = pd.DataFrame(self._flights_dict)

            # Create the file path for the CSV file using the provided file name
            file_path = f"{self.file_name}"

            # Export the DataFrame to a CSV file with the specified file path,
            # including the index and encoding
            df.to_csv(file_path, index=True, encoding='utf-8-sig')

            return file_path
        except OSError as e:
            print(f"Error was found when exporting to CSV: {e}")
            return 'None'

    def export_to_txt(self):
        """
        Exports flight data to a TXT file using the provided file_name.

        return: None
        """
        try:
            # Retrieve departure, arrival airports, and departure and return dates from the flight data dictionary
            depart = self._flights_dict["depart"]
            arrive = self._flights_dict["arrive"]
            departure_date = self._flights_dict["departure_date"]
            return_date = self._flights_dict["return_date"]

            # Open the file
            with open(self.file_name, "w") as file:
                # Write the header information
                file.write(f"This is flights info from {depart} ({departure_date}) to {arrive}({return_date}):")
                file.write("\n")

                # Loop through the flight data in the "flights" dictionary
                for flight in self._flights_dict["flights"].values():
                    file.write(
                        f"Departure Time: {flight['departure_time']} | Arrival Time: {flight['arrival_time']} | "
                        f"Main Cabin Price: {flight['main_cabin_price']} ")
                    file.write("\n")

        # handleing error
        except PermissionError:
            print("You do not have permission to use that file")
        except OSError as e:
            print(f"Error was fount when exporting to TXT: {e}")


if __name__ == "__main__":
    flights_data = FlightsData(depart, arrive, departure_date, return_date)
    flights_data.run()
