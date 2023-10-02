from datetime import datetime, timedelta
from metaphor_python import Metaphor
import os

def get_stock_articles():
    api_key = os.environ.get('METAPHOR_API_KEY')
    if api_key is None:
        raise Exception("API_KEY not found in environment variables")
    
    metaphor = Metaphor(api_key)

    current_date = datetime.now().date()

    start_date = current_date - timedelta(days=1)

    start_date_str = str(start_date)

    query = "Best stocks to buy today"
    search_response = metaphor.search(query=query, num_results=12, start_published_date=start_date_str, use_autoprompt=True)

    return search_response.results

    # for result in search_response.results:
    #     print(f"Title: {result.title}")
    #     print(f"URL: {result.url}")
    #     print(f"Extract: {result.extract}")
    #     print("-" * 40)


