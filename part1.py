'''
Class:356
Name:Sam Hatch
Description: a webscraping application that scrapes job posting sites
'''
import json
import re
from classes.Scraper import Scraper

total_jobs = []

page_num=1
itjobs_url=(f'https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page={page_num}')
techTalent_url = ('https://jobs.techtalent.ca/?k=information%20technology&l=British%20Columbia,%20Canada')
#TODO: look at source code for wbesite, looking for div class named result-info-wrapper


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
        
        

#self,url,wrapper_tag_type,wrapper_tag_class,content_tag_type,content_tag_class

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

getting_content = scraperITjobs.def_content(getting_wrapper,title_tag,title_class,info_tag,info_class,location_tag,location_class)
#scraperITjobs.dump_content(getting_content)



scraperTechTalent = Scraper(techTalent_url,'div','jobContainer','a','job-post-summary',True)
start_tech = scraperTechTalent.scraper_start()
getting_wrapper_tech = scraperTechTalent.def_wrapper(start_tech)

pattern = r'href="([^"]+)"'
match = re.findall(pattern,str(getting_wrapper_tech))
filtered_links = [link for link in match if "/cdn-cgi" not in link and "http" not in link]
# print(f'filtered_links: {filtered_links}')

base_link = 'https://jobs.techtalent.ca'
title_tag = 'h2'
title_class = 'job-post-summary__title'
info_tag = 'span'
info_class = 'job-post-summary__header'
location_tag = 'span'
location_class = 'flex flex-shrink items-center'

alljobs = []


    
getting_content_tech = scraperTechTalent.def_content(getting_wrapper_tech, title_tag, title_class, info_tag, info_class, location_tag, location_class, base_link,filtered_links)

    
    #print(f'Job content: {getting_content_tech}')
    
alljobs.append(getting_content)
alljobs[0].extend(getting_content_tech)

# for each in alljobs[0]:
#     print(f'JOB: {each}\n')

dumped = alljobs[0]


dump_content(dumped)


with open('data/joblist.json', 'r', encoding='utf-8') as joblist:
        data = json.load(joblist)
        for job_list in data:
            for job in job_list:
                for job_title, job_details in job.items():
                    print({job_title}, {job_details['link']})
                    full_job_descript=Scraper(job_details['link'].strip(),)


#full_job_descript = Scraper()

