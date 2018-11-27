#############################################################
# Dependencies
#############################################################
import pymongo
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
import lxml.html
import re
import datetime


#############################################################
# Define Path
#############################################################
def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

#############################################################
# Define Scrape Function
#############################################################
def scrape():
    # browser = init_browser function
    browser = init_browser()

    # Create a timestamp
    timeNow = datetime.datetime.utcnow()

    ### URL's to be scraped
    # NASA Mars News Site - collect the latest News Title and Paragraph Text
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    nasa_homeurl = 'https://mars.nasa.gov'
    # JPL Mars Space Images
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    PIAStart = "https://www.jpl.nasa.gov/spaceimages/images/largesize/"
    PIAEnd = "_hires.jpg"
    # Mars Weather - grab latest weather from Mars Weather twitter account
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    # Mars Facts - use Pandas to scrape the table containing facts (more details below)
    facts_url = 'https://space-facts.com/mars/'
    # Mars Hemisphere Image - create a dictionary with the image url string and the hemisphere title to a list (more details below)
    # Hems_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgsStart = "https://astrogeology.usgs.gov"

    
    ###############################################################################################
    ##### NASA Mars News
    ##### Using new_url, find the top featured title and teaser for the story
    
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'lxml-xml')

    featured_title =  soup.find('div', class_='content_title').a.text
    featured_teaser = soup.find('div', class_='article_teaser_body').text
    nasa_titlelink = re.findall('href="([^ ]*)/', str(soup.find('div', class_='content_title')))
    featured_link = nasa_homeurl+nasa_titlelink[0]

    ###############################################################################################
    ######### JPL Mars Space Image URL (Largesize jpg)
    browser.visit(jpl_url)
    html = browser.html
    soup = bs(html, 'lxml-xml')
    picurlraw = soup.find('div', class_='carousel_items')

    for link in picurlraw.find_all('a'):
        test99 = (link.get('data-fancybox-href'))

    aspos = test99.find('PIA')
    PIA = test99[aspos : (test99.find('_', aspos))]

    featured_image_url = PIAStart + PIA + PIAEnd
    
    ###############################################################################################
    ######### Mars Twitter Weather URL
    browser.visit(weather_url)
    html = browser.html
    soup = bs(html, 'lxml-xml')
    tweetraw = soup.find('div', class_='js-tweet-text-container')

    tweetfix = tweetraw.find('p')
    tweetwords = []
    for x in tweetfix:
        tweetwords.append(str(x))
    mars_weather = tweetwords[0]

    ###############################################################################################
    ######### Mars Facts - Scrape table with pandas

    browser.visit(facts_url)
    html = browser.html
    soup = bs(html, 'lxml-xml')
    tableraw = soup.find('table', attrs={'id':'tablepress-mars'})
    table_rows = tableraw.find_all('tr')

    dataList = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        dataList.append(row)
    marsDF = pd.DataFrame(dataList, columns=["A", "B"])
    marsHTML = marsDF.to_html()
    
    ###############################################################################################
    ######### Images of Mars Hemispheres ###############
    HemisphereTitles = []
    HemisphereLinks = []

    # Cerverus
    cerberusUrl = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    browser.visit(cerberusUrl)
    html = browser.html
    soup = bs(html, 'lxml-xml')
    cerberusHome = soup.find('img', class_='wide-image')
    cerberusStrRaw = (str(cerberusHome))
    cerberusPart = cerberusStrRaw[(cerberusStrRaw.find('/cache')):(cerberusStrRaw.find('jpg')+3)]
    cerberusLink = usgsStart + cerberusPart
    cerberusTitle = soup.find('h2', class_='title').text
    HemisphereTitles.append(cerberusTitle)
    HemisphereLinks.append(cerberusLink)

    #Schiaparelli
    schiaparelliUrl = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    browser.visit(schiaparelliUrl)
    html = browser.html
    soup = bs(html, 'lxml-xml')
    schiaparelliHome = soup.find('img', class_='wide-image')
    schiapStrRaw = (str(schiaparelliHome))
    schiapPart = schiapStrRaw[(schiapStrRaw.find('/cache')):(schiapStrRaw.find('jpg')+3)]
    schiapLink = usgsStart + schiapPart
    schiapTitle = soup.find('h2', class_='title').text
    HemisphereTitles.append(schiapTitle)
    HemisphereLinks.append(schiapLink)

    #Syrtis
    SyrtisUrl = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    browser.visit(SyrtisUrl)
    html = browser.html
    soup = bs(html, 'lxml-xml')
    SyrtisHome = soup.find('img', class_='wide-image')
    SyrtisStrRaw = (str(SyrtisHome))
    SyrtisPart = SyrtisStrRaw[(SyrtisStrRaw.find('/cache')):(SyrtisStrRaw.find('jpg')+3)]
    SyrtisLink = usgsStart + SyrtisPart
    SyrtisTitle = soup.find('h2', class_='title').text
    HemisphereTitles.append(SyrtisTitle)
    HemisphereLinks.append(SyrtisLink)

    #Valles
    VallesUrl = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    browser.visit(VallesUrl)
    html = browser.html
    soup = bs(html, 'lxml-xml')
    VallesHome = soup.find('img', class_='wide-image')
    VallesStrRaw = (str(VallesHome))
    VallesPart = VallesStrRaw[(VallesStrRaw.find('/cache')):(VallesStrRaw.find('jpg')+3)]
    VallesLink = usgsStart + VallesPart
    VallesTitle = soup.find('h2', class_='title').text
    HemisphereTitles.append(VallesTitle)
    HemisphereLinks.append(VallesLink)

    #### Create List of Dictionaries for Hemispheres
    hemisphere_image_urls = []
    hemisphere_image_urls.append({"title":cerberusTitle, "img_url":cerberusLink})
    hemisphere_image_urls.append({"title":schiapTitle, "img_url":schiapLink})
    hemisphere_image_urls.append({"title":SyrtisTitle, "img_url":SyrtisLink})
    hemisphere_image_urls.append({"title":VallesTitle, "img_url":VallesLink})

    ###############################################################################################
    #### Create Dictionary
    mongoCurrent = {
        'hemisphere_images' : hemisphere_image_urls,
        'featured_title' : featured_title,
        'featured_teaser' : featured_teaser,
        'featured_link' : featured_link,
        'featured_image_url' : featured_image_url,
        'mars_weather' : mars_weather,
        'marsHTML' : marsHTML,
        'timestamp' : timeNow
    }
    return mongoCurrent