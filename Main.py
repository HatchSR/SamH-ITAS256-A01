import json
import re
import asyncio
import time
from classes.Scraper import Scraper
from classes.AI_shortener import AI_shortening
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

total_jobs = []
alljobs = []
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def setup_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    # Add user agent to act more like a regular browser
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    return webdriver.Chrome(options=chrome_options)

def scrape_techtalent():
    driver = setup_selenium_driver()
    try:
        print("Starting TechTalent scraping...")
        driver.get('https://jobs.techtalent.ca/?k=information%20technology&l=British%20Columbia,%20Canada')
        
        # Wait for page load
        time.sleep(5)  # Give  page time to load
        
        print("Page loaded, looking for job listings...")
        
        
        possible_selectors = [
            ('class name', 'jobContainer'),
            ('class name', 'job-post-summary'),
            ('css selector', '.job-list-item'),
            ('css selector', '[data-testid="job-listing"]'),
            ('xpath', "//div[contains(@class, 'job')]")
        ]
        
        jobs_data = []
        for selector_type, selector in possible_selectors:
            try:
                print(f"Trying to find elements with {selector_type}: {selector}")
                if selector_type == 'class name':
                    elements = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, selector))
                    )
                elif selector_type == 'css selector':
                    elements = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                    )
                elif selector_type == 'xpath':
                    elements = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.XPATH, selector))
                    )
                
                print(f"Found {len(elements)} elements with {selector}")
                
                # If found elements, try to extract job information
                for element in elements:
                    try:
                        # Print elements HTML to debug
                        print(f"Element HTML: {element.get_attribute('outerHTML')}")
                        
                        #different ways to get title
                        title = None
                        try:
                            title = element.find_element(By.CSS_SELECTOR, 'h2.job-post-summary__title').text
                        except NoSuchElementException:
                            try:
                                title = element.find_element(By.TAG_NAME, 'h2').text
                            except NoSuchElementException:
                                title = element.find_element(By.CSS_SELECTOR, '[class*="title"]').text
                        
                        # different ways to get location
                        location = None
                        try:
                            location = element.find_element(By.CSS_SELECTOR, 'span.flex.flex-shrink.items-center').text
                        except NoSuchElementException:
                            try:
                                location = element.find_element(By.CSS_SELECTOR, '[class*="location"]').text
                            except NoSuchElementException:
                                location = "British Columbia"  # Default if not found
                        
                        # different ways to get link
                        link = None
                        try:
                            link = element.find_element(By.CSS_SELECTOR, 'a.job-post-summary').get_attribute('href')
                        except NoSuchElementException:
                            try:
                                link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                            except NoSuchElementException:
                                continue  # Skip if no link found
                        
                        if title and link:  # Only add if at least title and link
                            print(f"Found job: {title} - {location}")
                            jobs_data.append({
                                title: {
                                    'location': location,
                                    'link': link
                                }
                            })
                    except Exception as e:
                        print(f"Error processing job element: {str(e)}")
                        continue
                
                if jobs_data:  # If found jobs, break loop
                    break
                    
            except TimeoutException:
                print(f"Timeout trying selector: {selector}")
                continue
            except Exception as e:
                print(f"Error with selector {selector}: {str(e)}")
                continue
        
        if not jobs_data:
            print("No jobs found with any selector")
            
        return jobs_data
            
    except Exception as e:
        print(f"Major error in scrape_techtalent: {str(e)}")
        return []
    finally:
        print("Closing browser...")
        driver.quit()


techtalent_jobs = scrape_techtalent()
print(f"Found {len(techtalent_jobs)} jobs")

def dump_content(product):
    try:
        with open('data/joblist.json', 'r', encoding='utf-8') as joblist:
            existing_data = json.load(joblist)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []
   
    existing_data.append(product)
   
    with open('data/joblist.json', 'w', encoding='utf-8') as joblist:
        json.dump(existing_data, joblist, ensure_ascii=False, indent=4)

# ITJobs scraping
page_num = 1
while True:
    itjobs_url = f'https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page={page_num}'
   
    scraperITjobs = Scraper(itjobs_url, 'div', 'content-wrapper', 'div', 'result-info-wrapper')
    starting = scraperITjobs.scraper_start()
    getting_wrapper = scraperITjobs.def_wrapper(starting)
    getting_content = scraperITjobs.def_content(getting_wrapper, 'a', 'offer-name', 'a', 'location')
   
    alljobs.extend(getting_content)
    page_num += 1
   
    if page_num > 2:
        break

# TechTalent scraping using Selenium
techtalent_jobs = scrape_techtalent()
alljobs.extend(techtalent_jobs)

dump_content(alljobs)

# job description processing
async def get_all_descriptions():
    with open('data/joblist.json', 'r', encoding='utf-8') as joblist:
        data = json.load(joblist)
       
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
            data = data[0]
       
        for job_object in data:
            if isinstance(job_object, dict):
                for job_title, job_details in job_object.items():  
                    scraperfull_job_descript = Scraper(
                        job_details['link'], 'div', 'offer-wrapper', 'section', 'main-description-section'
                    )
                    start_job_descript = scraperfull_job_descript.scraper_start()
                    full_job_descript_getting_wrapper = scraperfull_job_descript.def_wrapper(start_job_descript)
                    cleaned_descript = re.sub(CLEANR, '', str(full_job_descript_getting_wrapper))
                    ai_summary = AI_shortening(cleaned_descript)
                    job_details['info'] = await ai_summary.get_response()
                   
    with open('data/joblist.json', 'w', encoding='utf-8') as joblist:
        json.dump([data], joblist, indent=4, ensure_ascii=False)

asyncio.run(get_all_descriptions())