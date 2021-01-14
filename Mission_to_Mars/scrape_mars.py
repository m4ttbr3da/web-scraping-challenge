# Dependencies
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
from splinter import Browser
from selenium import webdriver
import time
import os
import requests
import lxml

# Create function to initialize browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=True)

# Create dictionary for containing Mission to Mars info
mars_info = {}

#### INDIVIDUAL SCRAPER FUNCTIONS ####

# Creates function to scrape Mars news
def scrape_mars_news():
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    news_header = soup.find('li', class_='slide')
    mars_info["news_title"] = news_header.find('h3').text
    mars_info["news_p"] = news_header.find('div', class_='article_teaser_body').text.strip()

# Creates function to pull featured Mars image from Nasa
def scrape_mars_image():
#   Pulls url from the first image included
    browser = init_browser()
    news_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(news_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_header = soup.find('div', class_='SearchResultCard').a
    image_url_partial = image_header['href']
    image_url_full = 'https://www.jpl.nasa.gov' + image_url_partial
    
#   Pulls full url for the jpg of the image
    browser = init_browser()
    browser.visit(image_url_full)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_holder = soup.find('div', class_='BaseImagePlaceholder')

    mars_info["featured_image_url"] = featured_image_holder.find('img')['src']

# Creates function to pull Mars Facts
def scrape_mars_facts():
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df_facts = tables[0]
    df_facts.reset_index()
    mars_info["facts_html"] = df_facts.to_html()

# Creates function to pull Mars hemispheres data
hemisphere_image_urls = []

def scrape_mars_hemispheres():
    browser = init_browser()
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    results = soup.find_all('div', class_='item')
    
    for result in results:
        header = result.find('a')['href']
        hemi_link = 'https://astrogeology.usgs.gov/' + header

        browser.visit(hemi_link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        full_image = soup.find('img', class_='wide-image')['src']
        img_url = 'https://astrogeology.usgs.gov/' + full_image

        title_raw = soup.find('h2', class_='title').text.strip()
        title = title_raw.replace(" Enhanced","")

        temp_dict = {"title": title, "img_url": img_url}

        hemisphere_image_urls.append(temp_dict)

    mars_info["hemisphere_image_urls"] = hemisphere_image_urls

#### COMPILES SCRAPES INTO ONE FUNCTION ###

def scrape():
    scrape_mars_news()
    scrape_mars_image()
    scrape_mars_facts()
    scrape_mars_hemispheres()
    return mars_info


    




