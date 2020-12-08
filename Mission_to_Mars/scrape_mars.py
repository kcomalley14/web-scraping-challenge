from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import pymongo
import warnings
warnings.filterwarnings('ignore')

def init_browser():
    # Setup splinter
    executable_path = {"executable_path": "/Users/kyleomalley/Downloads/chromedriver"}
    return Browser('chrome', **executable_path, headless=False)

# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

# scrape function
def scrape():
    print("We are getting the data")
    browser = init_browser()

    # print(mars_dict)
    #Mars News scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Mars image scraped
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    find_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = image_url + find_image_url

    # Mars Facts scraped
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    
    read_table = pd.read_html(facts_url)
    mars_facts = read_table[0]
    mars_facts.columns = ['Description', 'Value']
    facts_html_table = mars_facts.to_html(index= False, justify='left')
    facts_html_table.replace('\n', '')

    # Hemisphere Images scraped
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemis = soup.find_all('div', class_='item')
    main_url = 'https://astrogeology.usgs.gov'
    hemis_image_urls = []

    for img in hemis:
        title = img.find('h3').text
        
        # need link to full res image
        specific_url = img.find('a', class_='itemLink product-item')['href']
        
        # visit link for image
        browser.visit(main_url + specific_url)
        
        # Now get html for page to find src to add to url list
        specific_url_html = browser.html
        
        soup = BeautifulSoup(specific_url_html, 'html.parser')
        
        imageurl = main_url + soup.find('img', class_='wide-image')['src']
        
        hemis_image_urls.append({"title": title, "img_url": imageurl})
        
# Dictionary for Scraped html
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "facts_html_table": facts_html_table,
        "hemisphere_image_urls": hemis_image_urls
        }
    return mars_dict