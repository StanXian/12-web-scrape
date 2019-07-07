from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time


def init_browser():

    executable_path = {"executable_path": "C:/Users/stanx/.wdm/chromedriver/75.0.3770.90/win32/chromedriver"}
    
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()
    
    mars_data = {}

    #NASA mars news
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.find('div', class_="content_title").find('a').text
    
    news_p = soup.find('div', class_="rollover_description_inner").text

    mars_data['news_title'] = news_title

    mars_data['news_p'] = news_p


    #JPL mars space images

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    base_url = (url.split('/spaceimages'))[0]

    description_page = soup.find_all('a', class_='button fancybox')[0]['data-link']

    description_url = base_url + description_page

    browser.visit(description_url)

    image = browser.html

    soup = BeautifulSoup(image, 'html.parser')

    img = soup.find('img', class_="main_image")['src']

    featured_image_url = base_url + img

    mars_data['featured_image_url'] = featured_image_url


    #Mars weather

    url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url)

    html = browser.html

    soup = BeautifulSoup(html, "html.parser")

    weather_tweets = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    for tweet in weather_tweets:

        mars_weather = tweet.text
        if "pic.twitter" in mars_weather:
            mars_weather = mars_weather.split('pic.twitter')[0]
        else:
            pass
        
        if "sol" and "pressure" in mars_weather:
            print(mars_weather)

            mars_data['mars_weather'] = mars_weather
            break
        else:
            pass


    # Mars hemispheres

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    base_url= (url.split('/search'))[0]

    hemispheres = soup.find_all('div', class_='description')

    for hemisphere in hemispheres:
       
        hemisphere_info = {}
        
        hem_title = hemisphere.find('h3').text
        
        hemisphere_info['title'] = hem_title.split(' Enhanced')[0]
        
        hem_route = hemisphere.find('a', class_='itemLink product-item')['href']
        
        hemisphere_link = base_url + hem_route
        
        browser.visit(hemisphere_link)
        
        html = browser.html
        
        soup = BeautifulSoup(html, 'html.parser')
        
        image_url = soup.find('div', class_='downloads').find('ul').find('li').find('a')['href']
        
        hemisphere_info['img_url'] = image_url
        
        hemisphere_image_urls.append(hemisphere_info)

        mars_data["image_urls"] = hemisphere_image_urls


    #MARS Facts

    url = 'https://space-facts.com/mars/'
   
    tables = pd.read_html(url)

    df = tables[0]

    df.columns = ['Description','Value']

    df.set_index('Description', inplace=True)

    html_table = df.to_html()

    html_table.replace('\n', '')

    mars_data['html_table'] = html_table

    browser.quit()

    return mars_data