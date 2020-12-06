from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings
warnings.filterwarnings('ignore')

def init_browser():
    # Setup splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)



# scrape function
def scrape():
    browser = init_browser()
    mars_info = {}

    #Mars News scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Mars image scraped
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
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


