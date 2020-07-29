import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import json

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    ##### NASA Mars News ####

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_list = soup.find('ul', class_= 'item_list')

    news_title = news_list.find('div', class_='content_title').get_text()
    print(news_title)


    news_p = soup.find('div', class_='article_teaser_body').get_text()

    print(news_p)


    #### JPL Mars Space Images - Featured Image ####

    url_base = 'https://www.jpl.nasa.gov'
    url = f'{url_base}/spaceimages/?search=&category=Mars'
    print(url)
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_div = soup.find(id= 'full_image')

    image_url = image_div['data-fancybox-href']

    featured_image_url = f'{url_base}{image_url}'
    print(featured_image_url)


    ##### Mars Weather ####


    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_twitter = soup.find("div",{"data-testid": "tweet"})
    mars_weather = mars_twitter.find(class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").get_text()

    print(mars_weather)


    #### Mars Facts ####

    # Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    html_link = "https://space-facts.com/mars/"
    mars_facts=pd.read_html(html_link)

    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ['Mars Planet Profile', 'Measurement']
    mars_facts_df


    #  Pandas to convert the data to a HTML table string
    mars_facts_html = mars_facts_df.to_html(index=False)
    mars_facts_html_final = mars_facts_html.replace('\n', '')
    mars_facts_html_final


    #### Mars Hemispheres ####

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Hemisphere titles list 

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_titles = soup.find_all('h3')

    img_title_list = []
    for title in image_titles:
        img_title_list.append(title.text)

    print(img_title_list)

    # Hemisphere pages to obtain the url images  
    pages_for_url = soup.find_all('div',class_='description')

    print('----------------------------------------------------------------------------------------------------------')
    print(pages_for_url)

    # Hemisphere url images list

    image_urls = []
    for image in pages_for_url:
        link = image.a['href']
        url = f'https://astrogeology.usgs.gov{link}'
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_url_soup = soup.find('img', class_= 'wide-image')
        url_append = image_url_soup['src']
        image_urls.append(f'https://astrogeology.usgs.gov{url_append}')

    print('----------------------------------------------------------------------------------------------------------')
    print(image_urls)
    
    # Json with hemisphere titles and images 

    hemisphere_image_urls = []

    for i in range(0,len(img_title_list)):
        hemisphere_image_urls.append({"title" : img_title_list[i], "img_url" : image_urls[i]})

    json.dumps(hemisphere_image_urls, indent = 1)

    print('----------------------------------------------------------------------------------------------------------')
    print(hemisphere_image_urls)


    # Dictionary with all the scraped information to return 


    all_scraping = {}

    all_scraping.update({'news_title':news_title,'news_text':news_p,'feature_img':featured_image_url,
                        'mars_weather_desc':mars_weather,"facts_table":mars_facts_html_final,"img_title_list":img_title_list,"image_urls":image_urls})

    print('----------------------------------------------------------------------------------------------------------')
    print(all_scraping)
    print('----------------------------------------------------------------------------------------------------------')
    
    return all_scraping

