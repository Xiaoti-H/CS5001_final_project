'''
This is the test file containing 2 test classes,
test FlightsData by Test_FlightsData and
tests DataExport by Test_DataExport

Classes:
    Test_FlightsData
    Test_DataExport

NAME: Xiaoti Hu
SEMESTER: 2023 Spring
'''
import unittest
from unittest.mock import MagicMock, patch, mock_open
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from unittest.mock import PropertyMock
from web_scraper import FlightsData, DataExport
import time


class Test_FlightsData(unittest.TestCase):
    """
    Test for FlightsData class in the web_scraper.

    Please note that page_scrape/run/get_flight_cards are
    higher-level functions which combine multiple operations
    and interaction with actual flight website. Testing these
    functions require more libraries/ packages.
    A better option is checking these function while running program.
    """

    def test_init(self):
        """
        Test the __init__ in FlightsData class.
        """
        #Test 1
        flights_data1 = FlightsData("JFK", "SFO", "2023-05-10", "2023-05-15")

        self.assertEqual(flights_data1.depart, "JFK")
        self.assertEqual(flights_data1.arrive, "SFO")
        self.assertEqual(flights_data1.departure_date, "2023-05-10")
        self.assertEqual(flights_data1.return_date, "2023-05-15")
        self.assertIsInstance(flights_data1.driver, webdriver.Chrome)
        self.assertIsNotNone(flights_data1.wait)

        # Test 2
        flights_data2 = FlightsData("LAX", "ORD", "2023-08-20", "2023-08-23")

        self.assertEqual(flights_data2.depart, "LAX")
        self.assertEqual(flights_data2.arrive, "ORD")
        self.assertEqual(flights_data2.departure_date, "2023-08-20")
        self.assertEqual(flights_data2.return_date, "2023-08-23")

    @patch('web_scraper.webdriver.Chrome')
    def test_setup_driver(self, mock_chrome):
        """
        Test setup_driver by mock webdriver.Chrome.
        """
        flights_data1 = FlightsData("SFO", "JFK", "2023-08-17", "2023-08-24")
        # Call the setup_driver function
        driver = flights_data1.setup_driver()

        # Check if webdriver.Chrome was called with the correct options
        options = mock_chrome.call_args.kwargs['options']
        self.assertIn(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            options.arguments)
        self.assertIn('--window-size=1920,1080', options.arguments)

        # Check if the function returns the correct driver instance
        self.assertEqual(driver, mock_chrome.return_value)

    def test_random_sleep(self):
        """
        Test the random_sleep for certain duration within defined range.
        """
        flights_data1 = FlightsData("JFK", "SFO", "2023-05-10", "2023-05-15")
        min_sec = 1
        max_sec = 3

        start_time = time.time()
        flights_data1.random_sleep(min_sec, max_sec)
        elapsed_time = time.time() - start_time

        self.assertTrue(min_sec <= elapsed_time <= max_sec)

    def test_get_price(self):
        """
        Test get_price returns the correct prices.
        """
        flight_data1 = FlightsData("JFK", "SFO", "2023-05-10", "2023-05-15")

        # Test by mocked prices
        mock_prices = [MagicMock(text="$100"), MagicMock(text="$200"), MagicMock(text="$300")]
        self.assertEqual(flight_data1.get_price(mock_prices, 0), "$100")
        self.assertEqual(flight_data1.get_price(mock_prices, 1), "$200")

        # Test with an invalid index out of range
        self.assertEqual(flight_data1.get_price(mock_prices, 5), "N/A")

    @patch("web_scraper.WebDriverWait")
    @patch("web_scraper.webdriver.Chrome")
    def test_fill_form(self, mock_chrome, mock_wait):
        """
        Test the fill_form with a mocked webdriver.Chrome and WebDriverWait.
        """
        flights_data1 = FlightsData("JFK", "SFO", "2023-05-10", "2023-05-15")
        flights_data1.driver = mock_chrome
        flights_data1.wait = mock_wait

        # create a MagicMock object to replace the various attributes
        mock_input = MagicMock()
        mock_input.clear = MagicMock()
        mock_input.click = MagicMock()
        mock_input.send_keys = MagicMock()
        mock_scroll_element = MagicMock()

        # Define side_effect function for find_element
        def side_effect(selector, value):
            if selector == By.ID and value == "id":
                return mock_input
            elif selector == By.CSS_SELECTOR:
                return mock_scroll_element
            else:
                return None

        mock_chrome.find_element.side_effect = side_effect

        # input for testing and use these info to fill form
        test_web_id, test_input = "id", "input"
        flights_data1.fill_form(test_web_id, test_input)

        # find_element with the correct arguments
        mock_chrome.find_element.assert_any_call(By.ID, test_web_id)
        # Assert that the mock was called exactly once
        mock_input.clear.assert_called_once()

    def test_process_prices(self):
        """
        Test process_prices and see if function can get price in
        specific location and present "N/A" if not catch any info.
        """
        flight_data1 = FlightsData("JFK", "SFO", "2023-05-10", "2023-05-15")

        # test 3 prices all existing
        mock_price1 = [MagicMock(text="$100"), MagicMock(text="$200"), MagicMock(text="$300")]
        basic_economy_price, main_cabin_price, first_class_price = flight_data1.process_prices(mock_price1)
        self.assertEqual(basic_economy_price, "$100")
        self.assertEqual(main_cabin_price, "$200")
        self.assertEqual(first_class_price, "$300")

        # test 2 prices
        mock_price2 = [MagicMock(text="200"), MagicMock(text="300")]
        basic_economy_price, main_cabin_price, first_class_price = flight_data1.process_prices(mock_price2)
        self.assertEqual(basic_economy_price, "N/A")
        self.assertEqual(main_cabin_price, "200")
        self.assertEqual(first_class_price, "300")

        # test no price
        mock_price3 = []
        basic_economy_price, main_cabin_price, first_class_price = flight_data1.process_prices(mock_price3)
        self.assertEqual(basic_economy_price, "N/A")
        self.assertEqual(main_cabin_price, "N/A")
        self.assertEqual(first_class_price, "N/A")

    def test_extract_info_and_find_text(self):
        """
        Test 2 functions extract_info and find_text together
        with a simple HTML string.
        """
        flights_data1 = FlightsData("JFK", "SFO", "2023-05-10", "2023-05-15")

        html_test = """
        <html>
            <body>
                <div class=\"test-class\">Test 1</div>
                <div class=\"test-class\">Test 2</div>
            </body>
        </html>
        """

        # test for find text
        bs = BeautifulSoup(html_test, "html.parser")
        result = FlightsData.find_text(bs, "test-class")
        self.assertEqual(result, "Test 1")

        # test for extract_info
        with patch.object(webdriver.Chrome, "page_source", new_callable=PropertyMock) as mock_page_source:
            mock_page_source.return_value = html_test

            class_name = "test-class"
            result = flights_data1.extract_info(class_name)

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0].text.strip(), "Test 1")
            self.assertEqual(result[1].text.strip(), "Test 2")


class Test_DataExport(unittest.TestCase):
    """
    Test class for the DataExport class.
     """

    def setUp(self):
        """
        Test setup in a correct format.
        """
        self.file_name = "test_file"
        self.flights_dict = {
            "depart": "LAX",
            "arrive": "SFO",
            "departure_date": "2023-05-15",
            "return_date": "2023-05-21",
            "flights": {
                1: {
                    "departure_time": "06:00",
                    "arrival_time": "08:00",
                    "main_cabin_price": "100",
                    "business_class_price": "800"
                },
                2: {
                    "departure_time": "14:00",
                    "arrival_time": "15:40",
                    "main_cabin_price": "220",
                    "business_class_price": None
                }
            }
        }
        self.data_export = DataExport(self.file_name, self.flights_dict)

    def test_export_to_csv(self):
        """
        Test if the export_to_csv supported by DataFrame works as expected.
        """
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            self.data_export.export_to_csv()
            mock_to_csv.assert_called_once()

    def test_export_to_txt(self):
        """
        Test if the export_to_txt works as expected.
        """
        with patch("builtins.open", mock_open()) as mock_to_txt:
            self.data_export.export_to_txt()
            mock_to_txt.assert_called_once_with(self.file_name, "w")


if __name__ == "__main__":
    unittest.main()
