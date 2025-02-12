'''
Class:356
Name:Sam Hatch
Description: a webscraping application that scrapes job posting sites
'''
import json
import re
from classes.Scraper import Scraper
from classes.AI_shortener import AI_shortening
import asyncio

total_jobs = []
alljobs = []
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

page_num=1
itjobs_url=(f'https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page={page_num}')
techTalent_url = ('https://jobs.techtalent.ca/?k=information%20technology&l=British%20Columbia,%20Canada')



def dump_content(product):
    try:
        # Read the existing data from the file if it exists
        with open('data/joblist.json', 'r', encoding='utf-8') as joblist:
            existing_data = json.load(joblist)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, start with an empty list
        existing_data = []
    
    # Append the new data to the existing data
    existing_data.append(product)
    
    # Write the combined data back to the file
    with open('data/joblist.json', 'w', encoding='utf-8') as joblist:
        json.dump(existing_data, joblist, ensure_ascii=False, indent=4)


for page in range(8):
    scraperITjobs= Scraper(itjobs_url,'div','content-wrapper','div','result-info-wrapper')

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

    getting_content = scraperITjobs.def_content(getting_wrapper,title_tag,title_class,location_tag,location_class)
    page_num+=1

scraperTechTalent = Scraper(techTalent_url,'div','jobContainer','a','job-post-summary',True)
start_tech = scraperTechTalent.scraper_start()
getting_wrapper_tech = scraperTechTalent.def_wrapper(start_tech)

pattern = r'href="([^"]+)"'
match = re.findall(pattern,str(getting_wrapper_tech))
filtered_links = [link for link in match if "/cdn-cgi" not in link and "http" not in link]

base_link = 'https://jobs.techtalent.ca'
title_tag = 'h2'
title_class = 'job-post-summary__title'
location_tag = 'span'
location_class = 'flex flex-shrink items-center'

getting_content_tech = scraperTechTalent.def_content(getting_wrapper_tech, title_tag, title_class, location_tag, location_class, base_link,filtered_links)
    
alljobs.append(getting_content)
alljobs[0].extend(getting_content_tech)

dumped = alljobs[0]


dump_content(dumped)

async def process_job_description(job_details):
    ai_shortener = AI_shortening(job_details['description'])
    job_details['info'] = await ai_shortener.get_response()
    return job_details

async def get_all_descriptions():
    with open('data/joblist.json', 'r', encoding='utf-8') as joblist:
            data = json.load(joblist)
            for job_list in data:
                for job in job_list:
                    for job_title, job_details in job.items():
                        if 'techtalent' in job_details['link']:
                            scraperfull_job_descript=Scraper(job_details['link'],'div','job-page__description','div','job-description-html',)
                            start_job_descript=scraperfull_job_descript.scraper_start()
                            full_job_descript_getting_wrapper=scraperfull_job_descript.def_wrapper(start_job_descript)
                            cleaned_descript= re.sub(CLEANR, '', str(full_job_descript_getting_wrapper))
                            ai_summary = AI_shortening(cleaned_descript)
                            job_details['info'] = await ai_summary.get_response()
                            
                        else:
                            scraperfull_job_descript=Scraper(job_details['link'],'div','offer-wrapper','section','main-description-section',)
                            start_job_descript=scraperfull_job_descript.scraper_start()
                            full_job_descript_getting_wrapper=scraperfull_job_descript.def_wrapper(start_job_descript)
                            cleaned_descript= re.sub(CLEANR, '', str(full_job_descript_getting_wrapper))
                            ai_summary = AI_shortening(cleaned_descript)
                            job_details['info'] = await ai_summary.get_response()



    with open('data/joblist.json', 'w', encoding='utf-8') as joblist:
        json.dump(data, joblist, indent=4, ensure_ascii=False)

asyncio.run(get_all_descriptions())