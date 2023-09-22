#!/usr/bin/python3

"""
This module defines a Flask-based web application with specified routes.
"""

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Render the 'Hello HBNB!' page.
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Render the 'HBNB' page.
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Render the 'C <text>' page.
    Replace underscores (_) in text with spaces.
    """
    return 'C ' + text.replace('_', ' ')


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """
    Render the 'Python <text>' page.
    Replace underscores (_) in text with spaces.
    """
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """
    Render 'n is a number' page if n is an integer.
    """
    return f'{n} is a number'


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Render a HTML page with "Number: n" inside the H1 tag in the BODY.
    """
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """
    Render a HTML page with Number: n is even|odd inside H1 tag in the BODY
    """
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
