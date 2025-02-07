'''
Class:356
Name:Sam Hatch
Description: a webscraping application that scrapes job posting sites
'''
import requests
import certifi
from bs4 import BeautifulSoup

page_num=1
url=(f'https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page={page_num}')

#TODO: look at source code for wbesite, looking for div class named result-info-wrapper
#







USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

headers={'User-Agent': USER_AGENT}

page= requests.get(url,headers=headers, verify=certifi.where())


soup=BeautifulSoup(page.text, "html.parser")


results = soup.find('div', class_='results-info-wrapper')


print(results)