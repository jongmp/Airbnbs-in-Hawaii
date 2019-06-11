# Import libraries
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import re
from urllib.request import urlopen, Request
import csv
from time import sleep

# Import dataframe with all the website names
listing = pd.read_csv('/Users/jpar746/Desktop/Work/Airbnb/listings_info.csv')

print(listing.head())
# defining the url page
reg_url = listing['listing_url'][0:200]

pd.set_option('display.max_columns', 100)
pic_url = []
# Looping through the DataFrame
for li in reg_url:
    # Getting the link
    req = Request(url=li, headers={'User-Agent': 'Chrome/41.0.2228.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    img_link = soup.find('meta', property = 'og:image')
    link = img_link['content']
    pic_url.append(link)
    sleep(1)

pic_url = pd.Series(pic_url)
pic_df = pd.concat([listing['id'], pic_url], axis=1)
print(pic_df)

export_csv = pic_df.to_csv (r'/Users/jpar746/Desktop/Work/Airbnb/pic_df.csv', index = None, header=True)
