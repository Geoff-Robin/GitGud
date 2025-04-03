import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import random

load_dotenv()
LEETCODE_API = os.getenv("LEETCODE_API_URL")

def load_proxies(file_path='proxy.txt') -> list:
    """Load proxies from a file and return them as a list."""
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies

def scraper(query: str) -> str:
    """
    Scrape the problem statement from LeetCode using the provided URL.
    The URL should be in the format: https://leetcode.com/problems/problem_name/description
    Returns the problem statement as a string.
    """
    proxies_list = load_proxies()
    temp = ""
    found = False
    for i in query:
        temp += i

        if temp != "https:/leetcode.com/problems/":
            found = True

        elif found:
            if i == "/":
                break
    problem_name = temp[: len(temp) - 2]
    proxy_address = random.choice(proxies_list)
    proxies = {
        'http': f'http://{proxy_address}',
        'https': f'https://{proxy_address}',
    }

    try:
        description_response = requests.get(
            LEETCODE_API + "/select?titleSlug=" + problem_name,
            proxies=proxies,
            timeout=10 
        )
        description_response.raise_for_status()
        description_json = description_response.json()
        description = description_json["question"]
        soup = BeautifulSoup(description, "html.parser")
        text = soup.get_text(separator="\n")
        return text.strip()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return ""
