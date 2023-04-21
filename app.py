'''
This is the main entry point for the web application.

NAME: Xiaoti Hu
SEMESTER: 2023 Spring
'''
from flask import Flask, render_template, request
import csv
from web_scraper import FlightsData
from datetime import datetime

app = Flask(__name__, template_folder='templates')

def read_csv(file_path):
    """
    Read CSV file and return its data as a list of rows.

    args: file_path: Path to the CSV file
    return: List of rows in the CSV file, excluding the header row
    """
    flight_options = []
    try:
        with open(file_path, newline='') as csvfile:
            flight_data = csv.reader(csvfile, delimiter=',')
            next(flight_data)  # Skip the header row
            for row in flight_data:
                flight_options.append(row)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Unexpected error while reading {file_path}: {e}")

    return flight_options

@app.route('/', methods=['GET', 'POST'])
def index ():
    """
    Flask route for the main page of the Flight Search application.

    If the request method is POST, the function processes the form data,
    retrieves flight information, and displays it in a table.

    If the request method is GET, the function renders the main page without flight data.
    """
    flight_options = []
    flight_headers = []

    # Process form data if the request method is POST
    if request.method == 'POST':
        try:
            # request data from client
            depart = request.form['departure']
            arrive = request.form['arrival']
            departure_date = request.form['departure_date']
            return_date = request.form['return_date']

            # Parse and format the dates to fit FlightsData class
            formatted_departure_date = datetime.strptime(departure_date, "%Y-%m-%d").strftime("%m/%d/%Y")
            formatted_return_date = datetime.strptime(return_date, "%Y-%m-%d").strftime("%m/%d/%Y")
            # check point
            ## print(f"Received form data: {depart}, {arrive}, {formatted_departure_date}, {departure_date}, {return_date}")

            # Call the web_scrape function to retrieve flight data
            flights_data = FlightsData(depart, arrive, formatted_departure_date, formatted_return_date)
            csv_file = flights_data.run()
            # Read the CSV file and store the flight data in a list
            flight_options = read_csv(csv_file)

            # Get the header from the CSV file
            with open(csv_file, newline='') as csvfile:
                flight_headers = next(csv.reader(csvfile, delimiter=','))
            # print(f"Flight options: {flight_options}")

        # exception condition
        except Exception as e:
            import traceback
            print(f"Error occurred: {e}")
            print(traceback.format_exc())
            return render_template('error.html', error_message=str(e))

    # Render the main page with flight data (if available)
    return render_template('index.html', flight_options=flight_options, flight_headers=flight_headers)

if __name__ == '__main__':
    app.run(debug=True)