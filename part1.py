'''
Class:356
Name:Sam Hatch
Description: a webscraping application that scrapes job posting sites
'''
import requests
import certifi
from bs4 import BeautifulSoup
from classes.Scraper import Scraper

page_num=1
url=(f'https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page={page_num}')

#TODO: look at source code for wbesite, looking for div class named result-info-wrapper

#self,url,wrapper_tag_type,wrapper_tag_class,content_tag_type,content_tag_class

scraperITjobs= Scraper(url,'div','content-wrapper','div','result-info-wrapper')

starting = scraperITjobs.scraper_start()
getting_wrapper = scraperITjobs.def_wrapper(starting)

#tags and classes in order for simplicity
title_tag='a'
title_class='offer-name'
info_tag='p'
info_class='offer-description'
location_tag='a'
location_class='location' 

# title_tag = input(str("what is the job's title tag?"))
# title_class = input(str("what is the job's title class?"))
# info_tag = input(str("what is the job's info tag?"))
# info_class = input(str("what is the job's info class?"))
# location_tag = input(str("what is the job's location tag?"))
# location_class = input(str("what is the job's location class?"))

getting_content = scraperITjobs.def_content(getting_wrapper,title_tag,title_class,info_tag,info_class,location_tag,location_class)
scraperITjobs.dump_content(getting_content)
