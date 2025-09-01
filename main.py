import requests
from bs4 import BeautifulSoup
import os

url = "https://quotes.toscrape.com"


def saveQuotesToDirectory(quotesData, folderName, fileName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    filePath = os.path.join(folderName, fileName)

    with open(filePath, 'w') as f:
        for quotes in quotesData:
            f.write(f"quote: {quotes['quotes']}\n")
            f.write(f"author: {quotes['author']}\n")
            f.write("-" * 20 + "\n" * 5)


def getQuotes():
    quotesWithAuthorData = []

    htmlFile = requests.get(url)
    soup = BeautifulSoup(htmlFile.text, 'html.parser')
    resultString = soup.find_all('div', class_='quote')

    for spanElements in resultString:
        quotes = spanElements.find('span', class_='text').text
        author = spanElements.find('small', class_='author').text
        quotesWithAuthorData.append({'quotes': quotes, 'author': author})

    return quotesWithAuthorData


file = 'quoteData_1'

saveQuotesToDirectory(getQuotes(), "myQuotes", file)
