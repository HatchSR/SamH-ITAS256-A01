from bs4 import BeautifulSoup     
import requests
import certifi  
       
        #info for the new beautiful soup entity
       
class Soup:
    def __init__(self,url):
        self.url = url
       
    def create_soup(self):   
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        headers={'User-Agent': USER_AGENT}
        page= requests.get(self.url,headers=headers, verify=certifi.where())
        soup=BeautifulSoup(page.text, "html.parser")        
        return soup