# rest_countries_exercise

Python/Flask project that returns information about the borders of a given country.
For a given country the following information about the borders have to be returned:
- Full name of the given country
- Full name of the bordering countries:
- Its capital
- The currency code
If the population of the bordering country is above 5 000 000 the currency code has to be encrypted using
the Caesar cipher (a left rotation of 1 place). If it is not the normal code has to be displayed.

**Dependencies installation**
---

1. Install python3 interpreter [`python3`](https://www.python.org/)
2. It is recommended to create a virtual environment [`venv`](https://docs.python.org/3/library/venv.html)
3. In linux environments use:
    $ pip install -r requirements.txt

**Usage**
---

```
    $ python app.py
```
The command above will run a http server in localhost
    http://127.0.0.1:5000

**Test the application**
---
Hit http://127.0.0.1:5000/name/United%20Arab%20Emirates with a web client, or a HTTP REST testing tool.

**Test using unittest library***
    $ python -m unittest test_app.py