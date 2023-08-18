import requests
from lxml import html
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import json

all_movies = []


# This function stores the data in a json file.
def write_to_json(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close


# This function stores the data in a csv file.
def write_to_csv(filename, data):
    headers = ['name', 'year', 'runtime', 'rating']
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        # Iterates through every index in a list and enters the values in the dictionary as rows in the csv file
        for i in data:
            writer.writerow(i)


def scrape(url):
    # Creating service object
    service = Service(r"C:\Users\ishag\chromedriver_win32\chromedriver.exe")
    # Creating ChromeDriver instance with the service object
    driver = webdriver.Chrome(service=service)

    resp = requests.get(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
    # Creating an elementary object to call xpath.
    tree = html.fromstring(html=resp.content)
    # this searches for and collects all the HTML elements that have the class name 'lister-item-content''. movies represents individual movie listing with movie name, rating, duration, etc.
    movies = tree.xpath("//div[@class = 'lister-item mode-advanced']//div[@class = 'lister-item-content']")

    # Iterates through each of the movie listing, scrapes the name, year, runtime, and rating and stores it in a dictionary. the dictionary is then appended in a list.
    for movie in movies:
        m = {
            'name': movie.xpath(".//h3[@class = 'lister-item-header']//a/text()")[0],
            'year': movie.xpath(
                ".//h3[@class = 'lister-item-header']//span[@class = 'lister-item-year text-muted unbold']/text()")[0],
            'runtime': movie.xpath(".//p[@class = 'text-muted ']//span[@class = 'runtime']/text()")[0],
            'rating': movie.xpath(
                ".//div[@class = 'ratings-bar']//div[@class = 'inline-block ratings-imdb-rating']/@data-value")[0]

        }
        all_movies.append(m)

    # next-page has the xpath of the "Next" option on the website that goes to the next page.
    next_page = tree.xpath(
        "//div[@class = 'desc']//a[@class = 'lister-page-next next-page' and contains(text(), 'Next')]")

    # since next_page is a list, if the length of the list is 0, that means there is no other page left. driver is a webdriver instance. It finds the next button by the xpath and clicks on it.
    # once the website opens to the next page, current_url copies the url of the webpage. scrape function is called with the currennt_url as its parameter to scrape the data on the next_page.
    if len(next_page) != 0:
        driver.get(url)
        driver.find_element(By.XPATH,
                            "//div[@class = 'desc']//a[@class = 'lister-page-next next-page' and contains(text(), 'Next')]").click()
        current_url = driver.current_url
        scrape(current_url)

    return all_movies


write_to_csv('movies_scraped.csv', scrape(
    "https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc&ref_=adv_prv"))