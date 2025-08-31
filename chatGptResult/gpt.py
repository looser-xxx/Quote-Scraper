# This script scrapes quotes and their authors from a simple website
# using the `requests` and `Beautiful Soup` libraries.

# Import the necessary libraries
import requests
from bs4 import BeautifulSoup
import os  # We'll use this module to create directories

# The URL of the website we want to scrape.
# This site is specifically designed for practicing web scraping.
URL = "http://quotes.toscrape.com"


def save_quotes_to_file(quotes, filename="scraped_quotes.txt"):
    """
    Creates a directory if it doesn't exist and saves the quotes to a text file.

    Args:
        quotes (list): A list of dictionaries, where each dictionary
                       contains a 'quote' and 'author'.
        filename (str): The name of the file to save the data to.
    """
    # Define the directory name where we'll save the files.
    # We use a relative path here.
    output_dir = "scraped_data"

    # Check if the directory already exists. If not, create it.
    if not os.path.exists(output_dir):
        print(f"Creating directory: '{output_dir}'")
        os.makedirs(output_dir)

    # Create the full file path.
    file_path = os.path.join(output_dir, filename)

    print(f"Saving quotes to '{file_path}'...")

    # Open the file in write mode ('w').
    # The 'with' statement ensures the file is automatically closed.
    with open(file_path, 'w', encoding='utf-8') as f:
        for quote_data in quotes:
            f.write(f"Quote: {quote_data['quote']}\n")
            f.write(f"Author: - {quote_data['author']}\n")
            f.write("-" * 20 + "\n")

    print("Quotes successfully saved!")


def scrape_quotes():
    """
    Fetches the HTML content, parses it, and returns a list of quote data.
    """
    print(f"Attempting to scrape quotes from: {URL}\n")

    quotes = []

    try:
        # Step 1: Fetch the HTML content of the page.
        response = requests.get(URL)

        # Check if the request was successful (status code 200).
        if response.status_code == 200:
            # Step 2: Parse the raw HTML content using BeautifulSoup.
            soup = BeautifulSoup(response.text, 'html.parser')

            # Step 3: Find the specific HTML elements containing the data.
            quote_elements = soup.find_all('div', class_='quote')

            if not quote_elements:
                print("No quotes found on the page.")
                return []

            print("Quotes found! Processing...\n")
            # Step 4: Loop through each quote element to extract the text.
            for quote_div in quote_elements:
                quote_text = quote_div.find('span', class_='text').text
                author_name = quote_div.find('small', class_='author').text

                # Append the extracted data to our list of quotes.
                quotes.append({'quote': quote_text, 'author': author_name})

            print("\nScraping complete!")
            return quotes

        else:
            print(f"Failed to retrieve the web page. Status code: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


# This ensures the `scrape_quotes` function is called only when the script is executed directly.
if __name__ == "__main__":
    # Scrape the quotes
    scraped_data = scrape_quotes()

    # If scraping was successful, save the data to a file
    if scraped_data:
        save_quotes_to_file(scraped_data)
