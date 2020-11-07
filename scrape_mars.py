#Dependicies
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from config import path

def init_browser():

    executable_path = {"executable_path":f"{path}"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    browser=init_browser()
    mars_dict={}
    time.sleep(2)
    #Mars news URL to be scraped
    mars_news_page='https://mars.nasa.gov/news/'
    browser.visit(mars_news_page)

    html=browser.html
    news_soup=bs(html,'html.parser')
    #Retrieve Title and teaser paragraph
    news_title=news_soup.find_all('div',class_='content_title')[1].text
    news_p=news_soup.find_all('div',class_="article_teaser_body")[0].text

    #JPL image URL to be scraped
    jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html=browser.html
    image_soup=bs(html,'html.parser')
    #Retrieve Image URL
    relative_img_path=image_soup.find_all('img')[3]['src']
    featured_image=f"https://www.jpl.nasa.gov{relative_img_path}"

    #Retrieve Mars facts table
    facts_url='https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_facts_df=tables[0]
    mars_facts_df.columns =['Description','Value']
    mars_fact_html=mars_facts_df.to_html(classes='table table-striped', index=False)
    mars_fact_html.replace('\n','')

    #Mars Hemisphere names and images scraped
    hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    html=browser.html
    hemi_soup=bs(html,'html.parser')
    hemi_url=[]

    items = hemi_soup.find_all('div', class_='item')

    for i in items:
        hemisphere = i.find('div',class_='description')
        title = hemisphere.h3.text
        
        hemisphere_link=hemisphere.a['href']
        browser.visit(f'https://astrogeology.usgs.gov{hemisphere_link}')
        
        image_html=browser.html
        image_soup=bs(image_html,'html.parser')
        
        image_url=image_soup.find('div',class_='downloads').find('li').a['href']
        
        hemi_url.append({'title':title,'img_url':image_url})
    
    #put it all together
    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image,
        "fact_table":str(mars_fact_html),
        "hemisphere_images":hemi_url
    }

    return mars_dict