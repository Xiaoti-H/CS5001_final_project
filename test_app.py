"""
This is test app.py using the pytest framework and Flask-Testing extension.
This test suite includes tests for the read_csv function,
as well as the GET request to the index route.

To successful run it, please install packages below:
pip install blinker
pip install pytest Flask-Testing

This is not a standalone application, please use the command below in terminal
after install pytest:
pytest test_app.py

NAME: Xiaoti Hu
SEMESTER: 2023 Spring
"""

import os
import tempfile
import pytest
from app import app, read_csv
from flask import template_rendered
from contextlib import contextmanager


@contextmanager
def captured_templates(app):
    """
    Context manager to capture the rendered template and context.

    args:
        app: The Flask application instance.

    yields:
        recorded: A list of tuples containing the template and its context.
    """
    recorded = []
    records = lambda sender, template, context, **extra: recorded.append((template, context))

    template_rendered.connect(records, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(records, app)


# Test the read_csv function
def test_read_csv():
    """
    Test read_csv in app.py.
    """
    # CSV file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as test_csv:
        test_csv.write("header1,header2\n")
        test_csv.write("r1_c1,r1_c2\n")
        test_csv.write("r2_c1,r2_c2\n")

    expected = [
        ["r1_c1", "r1_c2"],
        ["r2_c1", "r2_c2"]
    ]

    assert read_csv(test_csv.name) == expected
    os.unlink(test_csv.name)


# Test the GET request to the index route
@pytest.fixture
def client():
    """
    Pytest fixture to create a test client.

    yields:
        client: test client.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """
    Test if the route rendered the main page.

    args:
        client: test client.dd
    """
    with captured_templates(app) as templates:
        response = client.get('/')
        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'index.html'
        assert context['flight_options'] == []
        assert context['flight_headers'] == []
