import requests
import json
from typing import List, Optional, Dict, Any


class Search:
    """A client for interacting with the Open Library Search API."""
    
    BASE_URL = "https://openlibrary.org/search.json"
    DEFAULT_FIELDS = ["title", "author_name"]
    DEFAULT_LIMIT = 1

    def __init__(self):
        self.session = requests.Session()

    def _build_url(self, search_term: str, fields: List[str] = None, limit: int = None) -> str:
        """Construct the API URL with query parameters."""
        search_term_formatted = search_term.replace(" ", "+")
        fields = fields or self.DEFAULT_FIELDS
        limit = limit or self.DEFAULT_LIMIT
        
        fields_formatted = ",".join(fields)
        return f"{self.BASE_URL}?title={search_term_formatted}&fields={fields_formatted}&limit={limit}"

    def get_search_results(self, search_term: str) -> bytes:
        """Get raw search results from the API.
        
        Args:
            search_term: The book title to search for
            
        Returns:
            Raw response content as bytes
        """
        try:
            url = self._build_url(search_term)
            response = self.session.get(url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return b''

    def get_search_results_json(self, search_term: str, fields: List[str] = None, 
                              limit: int = None) -> Dict[str, Any]:
        """Get parsed JSON search results from the API.
        
        Args:
            search_term: The book title to search for
            fields: List of fields to include in response
            limit: Maximum number of results to return
            
        Returns:
            Dictionary containing parsed JSON response
        """
        try:
            url = self._build_url(search_term, fields, limit)
            print(f"Request URL: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return {}

    def get_user_search_results(self, search_term: str) -> str:
        """Get formatted search results for user display.
        
        Args:
            search_term: The book title to search for
            
        Returns:
            Formatted string with book information
        """
        try:
            response = self.get_search_results_json(search_term)
            if not response.get('docs'):
                return "No results found."
                
            book = response['docs'][0]
            title = book.get('title', 'Unknown Title')
            author = book.get('author_name', ['Unknown Author'])[0]
            
            return f"Title: {title}\nAuthor: {author}"
        except Exception as e:
            print(f"Error processing results: {e}")
            return "An error occurred while processing your request."


if __name__ == "__main__":
    search = Search()
    print("Open Library Book Search")
    print("-----------------------")
    
    while True:
        search_term = input("\nEnter a book title (or 'quit' to exit): ")
        if search_term.lower() == 'quit':
            break
            
        if not search_term.strip():
            print("Please enter a valid book title.")
            continue
            
        result = search.get_user_search_results(search_term)
        print("\nSearch Result:")
        print(result)
