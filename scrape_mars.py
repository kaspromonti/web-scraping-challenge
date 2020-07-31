from splinter import Browser
from bs4 import BeautifulSoup
import re
import os
import requests
import time
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_all():
    browser = init_browser()

    #PULLING NASA MARS NEWS TITLES
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')


    results = soup.find_all('div', class_='list_text')
    for result in results:
        title = result.find('div', class_='content_title')
        news_title = title.a.text
        news = result.find('div', class_='article_teaser_body')
        news_p = news.text.strip()

    #PULL FULL IMAGES OF HEMISPHERES
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)

    browser.click_link_by_partial_text('more info')

    html2 = browser.html
    img_soup = BeautifulSoup(html2, 'html.parser')

    try:
        results = img_soup.find('figure', class_='lede')
    except:
        print("image not found")

    featured_image_url = results.a['href']

    absolute_url = f'https://www.jpl.nasa.gov{featured_image_url}'
    
    #**********************
    #MARS WEATHER (TWITTER)
    #**********************

    # MARS HEMISPHERES
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')

    hemi_img_links = []
    list_of_hemi_dicts = []
    names = hemi_soup.find_all('div', class_='description')

    for x in names:
        hemi_dict = {}
        
        # find the name of each hemi and append to list
        h3 = x.find('h3').text.strip("Enhanced")
        
        # find the link to the page with the full size image and save in links list
        img_link = x.find('a')['href']
        hemi_img_links.append(img_link)


        # Loop thru the links to parse the browser and pull the name src of the full size image
        for i in hemi_img_links:
            browser.visit("https://astrogeology.usgs.gov" + i)
            time.sleep(2)
            img_html = browser.html
            hemi_img_soup = BeautifulSoup(img_html, 'html.parser')
            full_img = hemi_img_soup.find('img', class_="wide-image")['src']
            img_url = "https://astrogeology.usgs.gov" + full_img
        
        hemi_dict["Title"] = h3
        hemi_dict["ImageURL"] = img_url
        list_of_hemi_dicts.append(hemi_dict)
        
        fact_url = 'https://space-facts.com/mars/'
        tables = pd.read_html(fact_url)
        df = tables[0]
        df.columns=['description', 'value']
        mars_facts_table = df.to_html(classes='data table', index=False, header=False, border=0)

    #DICTIONARY OF SCRAPED DATA RESULTS
    data = {"Title" : news_title,
            "News" : news_p,
            "Featured_URL": absolute_url,
            "Hemispheres_Images" : list_of_hemi_dicts, 
            "Mars_facts" : mars_facts_table
            }
    
    print(data)
    
    browser.quit()
    return data

if __name__ == "__main__":

    print(scrape_all())

