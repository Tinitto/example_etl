# Example ETL (Extract Transform Load)

An example of an ETL app written in python pulling data from [https://finnhub.io/](https://finnhub.io/)
and saving its results in a CSV file. To find out more what an ETL app is,
read [the wikipedia article](https://en.wikipedia.org/wiki/Extract,_transform,_load).

## Purpose

This is a sample application with real-life scenario code. It is to be used for anyone interested in data analytics
who wishes to have a real-life project to mimic and build on top of.

I encourage you to make a clone of this
project, [create a new github project](https://docs.github.com/en/get-started/quickstart/create-a-repo), change
this projects remote to that url (type `git remote set-origin <your-new-github-project-url>` in your terminal while at
the root of this project's folder) and study the code then attempt
the [suggested further challenges](#suggested-further-challenges)

### Description

- This is a CLI (command line interface) app built with [Typer](https://typer.tiangolo.com/typer-cli/)
- It queries the https://finnhub.io/ free stock price API without using the Finnhub client but plain
  old [requests](https://pypi.org/project/requests/)
- It gets the latest price for Apple, Amazon, Netflix, Facebook, Google. Each of these has a number of variants e.g.
  Apple has "AAPL", "AAPL.SN" etc.
- From amongst these, it finds the stock that moved the most percentage points from the previous day. This stock is the
  most_volatile_stock.
- It saves the following information for the most_volatile_stock to a CSV file with the columns shown in the example
  below

Example:

```text
stock_symbol,percentage_change,current_price,last_close_price
AAPL, 13.2, 120.5, 150
```

## Dependencies

- [Python 3.9+](https://www.python.org/downloads/release/python-3913/)
- [Typer](https://typer.tiangolo.com/)
- [requests](https://pypi.org/project/requests/)

## Quick Start

- Clone this repo

```shell
git clone git@github.com:Tinitto/example_etl.git
```

- Create and activate your virtual environment for python 3.9+

```shell
python3 -m venv env
source env/bin/activate
```

- Install dependencies

```shell
pip install -r requirements.txt
```

- Run the `cli.py` module, providing it your Finnhub API KEY got from [Dashboard](https://finnhub.io/dashboard) and
  optionally the `api_rate_limit` basing on your Finnhub plan.

```shell
python cli.py --api-key your-api-key --api-rate-limit 60
```

- For more options, run the `help`

```shell
python cli.py --help
```

- To run tests

```shell
python -m unittest
```

## Design Decisions

- Have a single entry point called 'cli.py' which, when run must require args of:
    - api-key
    - api-rate-limit (int: optional; default=60)
- Split the task into three general parts
    - `extract` (get data from Finnhub API)
    - `transform` (convert received data into data to be saved)
    - `load` (save the data into the CSV file)
- `extract`:
    - the API request to get the latest price for a given stock has the following constraints according to
      the [docs](https://finnhub.io/docs/api/introduction).

      ```shell
      # for apple's "AAPL"
      curl --location --request GET 'https://finnhub.io/api/v1/quote?symbol=AAPL' \
      --header 'X-Finnhub-Token: api_key'
      ```

      returning a response:

      ```JSON
      {
        "c": 146.87,
        "d": 0.52,
        "dp": 0.3553,
        "h": 147.025,
        "l": 145,
        "o": 145.265,
        "pc": 146.35,
        "t": 1657290751
      }
      ```

      where "dp" is "Percent change", "c" is "Current price", "pc" is "Previous close price".

        - an API KEY is required either as a token parameter `token=apiKey` or as `X-Finnhub-Token : apiKey` header on
          every request.
            - We shall use the `X-Finnhub-Token : apiKey` header option as it will leave our URL's cleaner
        - a `symbol` for the given stock is required. For example for Apple, the symbol is "AAPL".
            - A list of stock_symbols is populated in the [config.py](core/config.py) module for the stocks of Apple,
              Amazon, Netflix, Facebook, Google.
            - The list is got be querying Finnhubs `api/v1/search?q={stock_search_term}` endpoint for each
              listed stock description and manually checking that each result item belongs to the given stock name.
            - This had to be manual because `api/v1/search?q={stock_search_term}` returns items that are similar to the
              search term also.
        - There are two environments
            - sandbox mode
                - free for testing all endpoints including premium ones
                - simply use the "Sandbox API key" in [Dashboard](https://finnhub.io/dashboard)
                - There is a `60 calls/minute` limit.
            - non-sandbox mode
                - Has [multiple plans](https://finnhub.io/pricing), some of which are paid for.
                - There is a limit to `number_of_api_calls` per minute depending on the plan.
        - On top of the API call limit per minute, there is a `30 API calls/ second` limit for each Finnhub plan.
            - When one's limit is exceeded, the response fails with status code `429`
            - We shall handle for the `429` possible exception by:
                - wait for 1 second then try the request again.
                    - If it fails again with the same error, wait again for a minute then try again.
                    - If it fails again with the same error, wait again for 3 minutes then try again.
                    - If it fails again with the same error, print to stdout
                      "number of API calls to Finnhub exceeded. Check that you are not using the same key in another
                      script or something then try again in 2 minutes".
            - To also reduce the chances of this happening:
                - Since `60 calls/minute` seems to be the lowest permissible limit, we shall make an api query per
                  second at most.
                - To allow for those with bigger Finnhub plans to speed this up, we will use the commandline
                  arg `api_rate_limit`
                  to adjust this rate in case it is supplied at the commandline
        - There maybe symbols that are not permitted for a given Finnhub plan basing on the API key being used.
            - the response returned is with status code 403 and an error message

          ```JSON
          {
            "error": "You don't have access to this resource."
          }
          ```

            - Handle such with a print to stdout that "Skipping because symbol {symbol} is not available due to {error
              message}"
- `transform`:
    - this will require schema definitions of input data type, and output data type.
    - Use python 3.9+ so as to use `dataclasses` for ease of transformation from one schema to another
    - There will be two transform operations:
        - Transform JSON from `extract` into `StockRecord` instances (parse JSON to Data Transfer Object)
        - Find most volatile stock in list of `StockRecord`s and return it
- `load`
    - this will open the `most_volatile_stock.csv` file on root; or create it if not exist.
    - It will then append the most volatile `StockRecord` passed to it.

## Suggested Further Challenges

Try any or all.

- Try to create a similar app that feeds into a [PostgreSQL database](https://www.postgresql.org/)
  . [Hint: You could look into using [SQLAlchemy](https://www.sqlalchemy.org/)]
- Or try to dump the raw data into PostgreSQL at a given interval either as
  a [cronjob](https://www.geeksforgeeks.org/how-to-setup-cron-jobs-in-ubuntu/) or using an in-process scheduler
  like [schedule](https://schedule.readthedocs.io/en/stable/) or [celery](https://docs.celeryq.dev/en/stable/).
  Open up a [jupyter notebook](https://jupyter.org/install) and connect to the database
  using [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) and study the
  data, formulate any analytical questions you can about the data and plot graphs with matplotlib.
- Or use [dbeaver](https://dbeaver.io/) or [DataGrip](https://www.jetbrains.com/datagrip/) to run SQL queries on that
  raw data to get a picture of what analytical questions to ask.
- Look into [Prefect](https://www.prefect.io/) and [Airflow](https://airflow.apache.org/). How can they improve your
  ETL pipeline above?

## License

Copyright (c) 2022 [Martin Ahindura](https://github.com/tinitto). Licensed under the [MIT License](./LICENSE)

## Gratitude

All glory be to God.

<a href="https://www.buymeacoffee.com/martinahinJ" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

