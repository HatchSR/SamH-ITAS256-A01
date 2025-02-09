import requests
import certifi
from bs4 import BeautifulSoup
from json import dumps,loads
import classes.AI_shortener as AI_shortener
class Scraper:
    def __init__(self,url,wrapper_tag_type,wrapper_tag_class,content_tag_type,content_tag_class):
        self.url = url
        self.content_tag_type = content_tag_type
        self.content_tag_class = content_tag_class
        self.wrapper_tag_type= wrapper_tag_type
        self.wrapper_tag_class = wrapper_tag_class
        
    def scraper_start(self):
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        headers={'User-Agent': USER_AGENT}
        page= requests.get(self.url,headers=headers, verify=certifi.where())
        soup=BeautifulSoup(page.text, "html.parser")        
        return soup
    
    def def_wrapper(self,wrapper):
        results = wrapper.find(self.wrapper_tag_type, class_=self.wrapper_tag_class)
        return results
        
        #TODO: Take the content and find the proper tags, add them to their own dictionary,
        # assign the smaller dicitinoary to a larger one and return the larger dictionary made up of all the other dictionaries
    def def_content(self,content,title_tag,title_class,info_tag,info_class,location_tag,location_class):
        all_content = content.find_all(self.content_tag_type,class_=self.content_tag_class)
        all_jobs={}
        
        for job in all_content:
            
            job_title = job.find(title_tag,title_class).text.strip().strip('\\n')
            job_info = job.find(info_tag,info_class).text
            job_location= job.find(location_tag,location_class).text
            all_jobs.update({job_title:{'Location':job_location,'info':job_info}})
            
            
        return all_jobs
    
    def dump_content(self,product):

        with open('data/joblist.json','w') as joblist:
            joblist.write(dumps(str(product)))
            
            
        
