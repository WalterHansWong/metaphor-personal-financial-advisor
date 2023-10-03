from datetime import datetime, timedelta
from metaphor_python import Metaphor
import os
import requests


def get_stock_articles():
    api_key = os.environ.get('METAPHOR_API_KEY')
    if api_key is None:
        raise Exception("METAPHOR_API_KEY not found in environment variables")

    metaphor = Metaphor(api_key)

    current_date = datetime.now().date()

    start_date = current_date - timedelta(days=1)

    start_date_str = str(start_date)

    query = "Best stocks to buy today"
    search_response = metaphor.search(query=query, num_results=9,
                                      start_published_date=start_date_str,
                                      use_autoprompt=True)

    return search_response.results

    # for result in search_response.results:
    #     print(f"Title: {result.title}")
    #     print(f"URL: {result.url}")
    #     print(f"Extract: {result.extract}")
    #     print("-" * 40)


def get_treasury_yield(timeframe: int):
    api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
    if api_key is None:
        raise Exception("ALPHA_VANTAGE_API_KEY not found in environment variables")

    # only Strings 3month, 2year, 5year, 7year,
    # 10year, and 30year are accepted. Round timeframe to nearest
    def round_to_time_values(days):
        # Convert days to years for easier comparison
        years = days / 365

        # Define the fixed time values in years
        time_values = {
            '3month': 3 / 12,
            '2year': 2,
            '5year': 5,
            '7year': 7,
            '10year': 10,
            '30year': 30
        }

        # Find the key (time value) with the minimum difference in years
        closest_time_value = min(time_values.keys(), key=lambda k: abs(time_values[k] - years))

        return closest_time_value

    maturity = round_to_time_values(timeframe)
    # print(f"rounded {timeframe} days, maturity is {maturity}")

    # replace the apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity={maturity}&apikey={api_key}'
    r = requests.get(url)
    info = r.json()

    return (maturity, info['data'][0]['date'], info['data'][0]['value'])


def get_best_interest_rate():
    # TODO
    return None
