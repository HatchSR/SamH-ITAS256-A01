import requests
import certifi
from bs4 import BeautifulSoup
import json
from classes.AI_shortener import AI_shortening
from classes.Soup import Soup

#TODO: 1.use beautiful soup to go to the site of each of the offers,
#       2.get the description and 
#       3.send it off to the ai shortener
#       4.stick it into the description dictionary entry

class Scraper:
    #initialize the scraper with the main information
    def __init__(self,url,wrapper_tag_type,wrapper_tag_class,content_tag_type,content_tag_class,stupid_links=False):
        self.url = url
        self.content_tag_type = content_tag_type
        self.content_tag_class = content_tag_class
        self.wrapper_tag_type= wrapper_tag_type
        self.wrapper_tag_class = wrapper_tag_class
        self.stupid_links = stupid_links
        

        
    #sends the scraper out to the wanted site
    def scraper_start(self):
        soup_start =  Soup(self.url)
        soup_find = soup_start.create_soup()
        return soup_find

    
    #finds the wrapper of the wanted content
    def def_wrapper(self,wrapper):
 
        results = wrapper.find(self.wrapper_tag_type, class_=self.wrapper_tag_class)
        
        return results
        
    #finds the content and retreives the needed information
    def def_content(self,content,title_tag,title_class,info_tag,info_class,location_tag,location_class,job_link_tag=None,job_link_class=None):
        
        # wrapper_str = str(content)
        # with open('data/check.txt', 'w', encoding='utf-8') as checking:
        #     checking.write(f'content is {(dumps(wrapper_str, indent=4))}') 
        
        all_content = content.find_all(self.content_tag_type,class_=self.content_tag_class)
        all_jobs=[]
        
        for job in all_content:
            if self.stupid_links == False:
                job_title_tag = job.find(title_tag,title_class)
                
                job_title=job_title_tag.find(text=True, recursive=False).strip()
                
                job_link = job.find(title_tag)['href']
                
                job_info = job.find(info_tag,info_class).text.strip()
                
                job_location= job.find(location_tag,location_class).text.strip()
                            
                all_jobs.append({job_title:{'Location':job_location,'info':job_info,'link':job_link}})
                
            elif self.stupid_links == True:
                        print("stupid link")
                        print(f'title tag: {job_link_tag}')
                        #print(job)
                        base_link = input('What is the base link of the site? ')
                        
                        job_href = job.find(job_link_tag)['href']


                        user_check = input(f'The found parent link is ({job_href}) does this look correct? (y/n): ')

                        if user_check.lower() == 'y':
                            print(job_link_tag,job_link_class)
                            job_title_tag = job.find(job_link_tag, job_link_class)
                            print(job_title_tag)
                            job_title = job_title_tag.find(text=True, recursive=False).strip()
                            job_link = base_link + job_href  # Ensure proper formatting
                            job_info = job.find(info_tag, info_class).text.strip() if job.find(info_tag, info_class) else "info not found"
                            job_location = job.find(location_tag, location_class).text.strip() if job.find(location_tag, location_class) else "location not found"

                            all_jobs.append({job_title: {'Location': job_location, 'info': job_info, 'link': job_link}})

                        elif user_check.lower() == 'n':
                            print("Skipping this link.")
                        else:
                            print('Please input "y" or "n".')

                                            
                            
                
            
        return all_jobs
    
    # def summarize_description(self,jobs):
        
        
    #     soup_job_info =  Soup(url)
    #     soup_find_info = soup_job_info.create_soup()
        
    
    #writes the content to joblist.json


    def dump_content(self, product):
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