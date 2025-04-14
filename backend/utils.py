"""
This module provides utility functions for the backend routes.

It includes a scraper function to fetch and parse problem descriptions from LeetCode.
"""

import requests
import json
from bs4 import BeautifulSoup

def scraper(problem_slug: str) -> str:
    """
    Fetch and extract the text description of a LeetCode problem using its slug.

    Args:
        problem_slug (str): The slug of the LeetCode problem (e.g., 'two-sum').

    Returns:
        str: The problem description as plain text, or an error message if the request fails.
    """
    url = 'https://leetcode.com/graphql/'
    headers = {
        'Content-Type': 'application/json',
        'Referer': f'https://leetcode.com/problems/{problem_slug}/'
    }
    payload = {
        'operationName': 'questionData',
        'variables': {'titleSlug': problem_slug},
        'query': '''
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            content
          }
        }
        '''
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        if 'errors' in data:
            return f"Error: {data['errors']}"

        # Extract the HTML content
        html_content = data['data']['question']['content']
        
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text from the parsed HTML
        text = soup.get_text(separator='\n', strip=True)
        
        return text
    except requests.RequestException as e:
        return f"Request failed: {e}"
