import unittest
from unittest.mock import patch, MagicMock
from app.financial_calculations import get_stock_articles, get_treasury_yield

class TestFinancialCalculations(unittest.TestCase):

    @patch('app.financial_calculations.Metaphor')
    @patch('app.financial_calculations.os')
    def test_get_stock_articles(self, mock_os, mock_metaphor):
        # Mocking the os.environ.get method to return a dummy API key
        mock_os.environ.get.return_value = 'test_api_key'

        # Creating a mock for search_response.results
        mock_results = [{'title': 'Test Article', 'url': 'http://test.com'}]

        # Creating a mock object for search_response
        mock_search_response = MagicMock()
        mock_search_response.results = mock_results

        # Setting the return value of metaphor.search to mock_search_response
        mock_metaphor_instance = mock_metaphor.return_value
        mock_metaphor_instance.search.return_value = mock_search_response

        articles = get_stock_articles()

        # Verifying that get was called with 'METAPHOR_API_KEY'
        mock_os.environ.get.assert_called_with('METAPHOR_API_KEY')

        # Verifying that the Metaphor object was created with the correct API key
        mock_metaphor.assert_called_with('test_api_key')

        # Verifying that search was called with the correct arguments
        mock_metaphor_instance.search.assert_called_once()

        # Asserting that the function returns the correct results
        self.assertEqual(articles, mock_results)

    @patch('app.financial_calculations.requests.get')  # This line patches requests.get with a mock object
    def test_get_treasury_yield(self, mock_get):
        # Arrange
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            'data': [{'date': '2023-09-28', 'value': '4.38'}]
        }  # This is the response that requests.get(url).json() will return

        # Act
        maturity, date, value = get_treasury_yield(1000)

        # Assert
        self.assertEqual(maturity, '2year')
        self.assertEqual(date, '2023-09-28')
        self.assertEqual(value, '4.38')

    @patch('app.financial_calculations.requests.get')  # This line patches requests.get with a mock object
    def test_get_treasury_yield_rounding(self, mock_get):
        # Arrange
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            'data': [{'date': '2023-09-28', 'value': '4.38'}]
        }  # This is the response that requests.get(url).json() will return

        # Act
        maturity1, date, value = get_treasury_yield(8 * 365)
        maturity2, date, value = get_treasury_yield(60 * 365)

        # Assert
        self.assertEqual(maturity1, '7year') # 8 years is closer to 7 than 10
        self.assertEqual(maturity2, '30year') # 60 years is closest to 30 years
        

if __name__ == '__main__':
    unittest.main()
