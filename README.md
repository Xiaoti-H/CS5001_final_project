# ✈️ Flight Search Application 

* **Course**: CS 5001: Intensive Foundations of Computer Science
* **Semester**: 2023 Spring
* **Student**: Xiaoti Hu

The goal of this project is to build a flight search application to scrape American Airline's flight information, and to display flights result in a single HTML page.

## Background

The Flight Search page allows users to input their trip details, including the departure location, arrival destination, departure date, and return date. Upon submission, the application initiates a web-scraping process on the American Airlines website to extract live flight data. The search results are then displayed on the webpage, and a CSV file containing the data is saved in the same directory as the application.



## Goals

- Automate the process of searching for flight information from American Airlines

- Extract relevant flight details for users based on their input

- Present the gathered flight data in an organized and user-friendly interface

  

## Built with

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Python library used to scrap HTML pages

- [Selenium](https://pypi.org/project/selenium/) [ChromeDriver](http://chromedriver.chromium.org/getting-started) - used to automate Chrome browser interaction from Python

- [Flask](https://flask.palletsprojects.com/en/1.0.x/) - Python framework used to build the web application

  

## Method

In this project, a diverse range of Python concepts we learned from 5001 were employed, such as **iteration**, **dictionaries**, **file handling**, and **error handling**. To effectively tackle the overarching problem, it was broken down into a series of smaller, manageable tasks. Each of these tasks was addressed by implementing dedicated class functions, resulting in a modular and efficient solution :

### 1. Web Scraping 

###### web_scraper.py/class FlightsData

- Configure Selenium ChromeDriver for automated browser interactions
- Use Selenium ChromeDriver to access and interact with American Airlines flight search results
- Implement BeautifulSoup to parse HTML content and extract pertinent flight information, such as origin/destination (based on user input), flight number, departure/arrival times, duration, and pricing details
- Process the extracted flight data and store it in a dictionary for subsequent operations

### 2.  Data Export and Storage

###### web_scraper.py/class DataExport

- Offer two functions for exporting flight data in CSV or TXT formats

  Note: to succesfully run app.py, please export as CSV

### 3. Develop Flask App

###### app.py

- Design a Flask app with a primary route supporting both GET and POST methods
- Employ the POST method to process form data and retrieve flight information
- Utilize the `read_csv` function to read a CSV file and return flight data as a list, then render the main page with flight data (if available) using an HTML template

### 4. HTML Interface

###### index.html

- Craft a user-friendly HTML interface for the Flight Search application, including a form for user input and a customized table for displaying flight data
- Implement a JavaScript function to reveal the results section upon form submission

### 5. Test

- test_web_scraper.py 

- test_app.py

  

# Instructions

### Preparation

1. Install the required libraries using pip:

```
pip install Flask selenium beautifulsoup4
```

1. Download the appropriate version of [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) based on your installed Chrome version. Extract the executable file and place it in a directory that is part of your system's `PATH` variable.
2. Create a new directory to store the project files. Inside the directory, create the following files and directories:

- `app.py`: This file contains the Flask application code provided above.
- `web_scraper.py`: This file should contain the implementation of the `FlightsData` and `DataExport` classes responsible for web scraping and exporting flight data.
- `templates/`: This directory should contain your HTML templates, such as `index.html` and `error.html`.

### Running the Application

1. Open a terminal/command prompt, navigate to the project directory containing `app.py`, and run the following command:

```
python app.py
```

1. Open a web browser and visit http://127.0.0.1:5000/. You should see the main page of the Flight Search application.

2. Fill in the form with your desired departure, arrival, and dates, then click "Submit" to retrieve and display the flight information.

   

## Challenges

### Scraping dynamic HTML pages

- Adapt to website changes: Airlines frequently update their website designs and code, which can cause a previous code unable to work. So,it is important to check the website structure.
- Airlines often implement various anti-scraping techniques to prevent automated data extraction. So I need to be very cautious in testing the code to prevent blocking. For example, the American Airline website is sensitive with search frenquency and duplicated information. A helpful tip is change the inputs(depart,arrive,date) when searching flights.
- Handling JavaScript website structure. Since this is my first time touching webpage design, I'm struggling with locating and extracting data from dynamic HTML pages.

### FLASK Framework

- Navigating the framework's structure: I spent a quite long time understanding Flask's modular design and related syntax/methods.

- Handling database/program connections is another challenge I have when learning Flask.

- Building a customized HTML webpage is a challenge for me. However, it is always good to find references that has similar structure and/or portion(s).

## References 
<img src="[FlightSearch_preview.gif](https://github.com/Xiaoti-H/CS5001_final_project/blob/564ff95c97654efdf2899b534a6d52f6dfe9e812/FlightSearch_preview.gif)" style="zoom: 33%;" />

## References

### Key tutorials

- [How to build a web application using Flask and deploy it to the cloud](https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/)
- [100 Days of Code: The Complete Python Pro Bootcamp for 2023](https://www.udemy.com/course/100-days-of-code/)
- [Flask Documentation (2.2.x)](https://flask.palletsprojects.com/en/1.1.x/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### Examples 

- [AmericanAirline by [thehappydinoa]](https://github.com/thehappydinoa/AmericanAirlines/commits?author=thehappydinoa)
- [flight_scraper by fnneves](https://github.com/fnneves/flight_scraper)
- [AmericanAirlines-scraper by Austerius](https://github.com/Austerius/AmericanAirlines-scraper/blob/9848f133d941e715c2a28c8e6ed99440967e908d/american_airlines.py)
- [NLP-Flask-Website](https://github.com/pemagrg1/NLP-Flask-Website)
- [Web Scraping using Beautiful Soup and Selenium for dynamic page](https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25)
- ChatGPT, personal communication

### Image sources

- [Unplash](https://www.pinterest.se/pin/261631059581218212/)

- [Canva](https://www.canva.com/)

  
