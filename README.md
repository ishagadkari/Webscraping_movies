# Webscraping_movies
MOVIE DATA SCRAPER:

File name: movies_imdb_details

The python script has a function called ‘scrape()’ which scrapes data on movies from IMDb’s Top 250 Drama Movies page. The script uses the ‘requests’ library in order to fetch web content and ‘lxml’ in order to parse the HTML and extract important and relevant information, specifically, the movie name, the year released, the runtime and the rating. 

USAGE:

Installation of Required packages:

To make this code functions, the required packages need to be installed by running the following code:
1.	pip install requests 
2.	pip install lxml
3.	pip install selenium
   
OUTPUT:

The script will scrape aforementioned details of the movies from the IMDb page. The data is stored in a list of dictionaries, where each dictionary represents a movie. Furthermore, the script provides options to save the scraped data in both JSON and CSV formats. 

HOW IT WORKS?

1.	The Script fetches the web content using ‘requests’ library and parses it with ‘lxml’. 
2.	It identifies the XPath to extract the listings of each movie on the IMDb page. 
3.	A loop iterates through each movie listing, extracting and storing relevant details (name, runtime, year, and rating) in a dictionary. 
4.	The dictionaries are then appended to the ‘all_movies’ list. 
5.	After all the movie details have been scraped for that page, the script looks for the “Next” button on the page. 
6.	If the “Next” button is found, the Selenium webdriver instance called driver finds the “Next” button through the XPath and automates the clicking of that button to go to the next page. 
7.	Then, through recursion by calling the scrape function, all pages are scraped, and the ‘all_movies’ list is returned. 
8.	Additional functions are provided to store the data in both JSON and CSV formats. 

NOTES:

A.	The script showcases a basic example of web scraping using the ‘requests’ and ‘lxml’ libraries in python. 
B.	It demonstrates the process of iterating through pages using the “Next” button and collecting data from each page. 

SHORT-COMINGS:

There are quite a few shortcomings in the code I have written. 

Time complexity:

a.	The scrape function is called recursively; thus, the time complexity depends on the number of pages there which in turn affects the number of times the ‘scrape function’ is called recursively. 

b.	For each recursive call, the page performs the following actions:
•	Fetching page content using ‘requests’
•	Setting up an instance of the Chrome web driver using Selenium. 
•	Scraping data using ‘lxml’ – Since there is a for loop which runs until all the movies are scraped, we can say that there are n movies and the time complexity for this will be O(n). 
•	Clicking on the “Next” button to navigate to the next page. 

Considering there are p pages, we can say that the time complexity of will be O(pn). 

Other factors affecting Run-Time:

Web-scraping interactions with Selenium web elements, such as clicking to go to the next page, introduced variability in terms of run-time. Specifically, the ‘driver.get()’ function which instructs the WebDriver to open the specific URL. And the ‘driver.find_element(By.Xpath, ).click()’ which first finds the ‘Next’ button by its XPath and then clicks on it to go to the next page. This time can depend on how network lag or website load time/responsiveness. Since these are called repeatedly due to recursion, the different pages first opened, the page was scraped, the pages were closed, and that is when the script stopped running and returned all_movies. 
The overall runtime was between 65-70 seconds which scrapes 182 movies. This is the biggest shortcoming of my code. 

HOW I FIXED IT?

Note: the changes can be seen in movies_imdb_updated
Instead of using selenium to automate the clicking of the “next” button and going to the next page, I joined the base URL, that is the URL for the first page with the relative URL which is stored in the ‘next_page’ element. This URL is then passed as a parameter to the recursive call of the ‘scrape’ function. 
This simple solution decreased the runtime from 65-70 seconds to 3-5 seconds. 









