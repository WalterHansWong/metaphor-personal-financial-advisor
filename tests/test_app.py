import unittest
from unittest.mock import patch
from app import app  # Import the app object for testing

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    # Use the patch decorator to replace get_stock_articles with a mock function since we are not testing the
    # Metaphor API or financial_calculations.py here
    @patch('app.routes.get_stock_articles')
    def test_index_page(self, mock_get_stock_articles):
        # Define a fixed response for get_stock_articles
        mock_get_stock_articles.return_value = [{'title': 'Test Article', 'url': 'http://test.com'}]

        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    @patch('app.routes.get_stock_articles')
    def test_valid_form_submission(self, mock_get_stock_articles):
        mock_get_stock_articles.return_value = [{'title': 'Test Article', 'url': 'http://test.com'}]

        response = self.app.post('/', data={
            'dollar_amount': '1000',
            'timeframe': '1',
            'timeframe_unit': 'years'
        })
        self.assertEqual(response.status_code, 302) # Redirects to the output page

    @patch('app.routes.get_stock_articles')
    def test_no_articles(self, mock_get_stock_articles):
        mock_get_stock_articles.return_value = []

        response = self.app.get('/output')
        self.assertIn(b'No articles found.', response.data)

if __name__ == '__main__':
    unittest.main()
