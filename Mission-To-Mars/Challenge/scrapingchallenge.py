# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment (# Set up Splinter)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_results = hemispheres(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_results,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# ## Mars News Scrape

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')
        #slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():

    try:
    # Use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #df

    return df.to_html()


# ## Hemispheres Challenge

def hemispheres(browser):

# Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

# Create a list to hold the images and titles (output to disply in #4 below).
    hemisphere_image_urls = []

# Write code to retrieve the image urls and titles for each hemisphere.
    #Since the main page has only thumbnails, we have to click into each one...
    #then grab each item (each image, each title), 
    #then add them together into the hemisphere_image_urls

    try:
        
        for content in range(4):
    
            #click each link... https://splinter.readthedocs.io/en/latest/elements-in-the-page.html
            browser.links.find_by_partial_text('Hemisphere')[content].click()
            
            #using soup to parse (jupycell 4, above)
            html = browser.html
            hemisphere_soup = soup(html, 'html.parser')
            
            #scrape the interior page...
            title = hemisphere_soup.find('h2', class_='title').text
            img_url = hemisphere_soup.find('li').a.get('href')
            
            #define dictionary, define dictionary items
            hemisphere_content = {}
            hemisphere_content['title']=title
            hemisphere_content['img_url']= f'https://marshemispheres.com/{img_url}' 
            
            #add scraped stuff together into hemisphere_image_urls
            hemisphere_image_urls.append(hemisphere_content)
            browser.back()  #<<LOOP

    except AttributeError:
        return None

    # Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())