import requests
from lxml import html
from urllib.parse import urljoin
import csv
import json

all_movies =[]

# This function stores the data in a json file. 
def write_to_json(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close
 
 #This function stores the data in a csv file. 
def write_to_csv(filename, data):
    headers = ['name', 'year', 'runtime', 'rating']
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
# Iterates through every index in a list and enters the values in the dictionary as rows in the csv file
        for i in data:
            writer.writerow(i)

def scrape(url):

   resp = requests.get(url = url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
#Creating an elementary object to call xpath. 
   tree = html.fromstring(html = resp.content)
#this searches for and collects all the HTML elements that have the class name 'lister-item-content''. movies represents individual movie listing with movie name, rating, duration, etc. 
   movies = tree.xpath("//div[@class = 'lister-item mode-advanced']//div[@class = 'lister-item-content']") 

   for movie in movies:
        m = {
            'name' : movie.xpath(".//h3[@class = 'lister-item-header']//a/text()")[0],
            'year': (movie.xpath(".//h3[@class = 'lister-item-header']//span[@class = 'lister-item-year text-muted unbold']/text()")[0]),
            'runtime': int((movie.xpath(".//p[@class = 'text-muted ']//span[@class = 'runtime']/text()")[0])[:-4]),
            'rating' : float(movie.xpath(".//div[@class = 'ratings-bar']//div[@class = 'inline-block ratings-imdb-rating']/@data-value")[0])
 
        }
        all_movies.append(m)
 
 #next-page has the xpath of the "Next" option on the website that goes to the next page.  
   next_page = tree.xpath("//div[@class='desc']/a[contains(text(), 'Next')]/@href")

   if len(next_page) != 0:
       scrape(url = urljoin(base = url, url = next_page[0]))
   
   return all_movies
   
#Calling the write_to_csv function and the scrape function. 
write_to_csv('scraped.csv',scrape("https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc&ref_=adv_prv"))
   
  