
import json

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
    def def_content(self,content,title_tag,title_class,location_tag,location_class,base_link='',job_link_array=[]):
        
        # wrapper_str = str(content)info_tag,info_class,
        # with open('data/check.txt', 'w', encoding='utf-8') as checking:
        #     checking.write(f'content is {(dumps(wrapper_str, indent=4))}') 
        
        all_content = content.find_all(self.content_tag_type,class_=self.content_tag_class)
        all_jobs=[]
        #print(all_content)
        array_spot = 0
        
        for job in all_content:
            #print(f'processing job: {str(job)[:50]}')

            if self.stupid_links==True:

                # print('stupid links triggered')
                job_title_tag = job.find(title_tag,title_class)
                job_title=job_title_tag.find(text=True, recursive=False).strip()
            
                full_job_link = base_link+str(job_link_array[array_spot])

                job_info =' job_info_request.get_response()'
                
                job_location= job.find(location_tag,location_class).text.strip()
                            
                all_jobs.append({job_title:{'Location':job_location,'info':job_info,'link':full_job_link}})
                array_spot+=1
        
                    
                
            else:
                # print('stupid links not triggered')
                job_title_tag = job.find(title_tag,title_class)
                
                
                # Let ED cook the chicken
                job_title=job_title_tag.find(text=True, recursive=False).strip()
            
                full_job_link = job.find(title_tag)['href']
                
                job_info =' job_info_request.get_response()'
                
                job_location= job.find(location_tag,location_class).text.strip()
                            
                all_jobs.append({job_title:{'Location':job_location,'info':job_info,'link':full_job_link}})
    

                


                                            
                            
                
            
        return all_jobs
    
    
        
    


