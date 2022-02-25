from distutils.command.config import config
from operator import itemgetter, le
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pandas as pd 
import json
import sqlite3 as sql
import os

class ScrapProductSpider(CrawlSpider):
    current_location= os.getcwd()+'/product_search'
    print(current_location)
    #deleting existing data if  present, in future it can be appending 
    if os.path.exists(current_location+"/Database/product_details.db"):
        os.remove(current_location+"/Database/product_details.db")
        
    conn=sql.connect(current_location+"/Database/product_details.db")
        
    
    # reading product details file 
    product_df= pd.read_excel(current_location+'/Configurations/product_details.xlsx',header=0)
    print("Product Details to search",product_df)
   
    # reading configuration file 
    with open(current_location+'/Configurations/config.json') as json_file:
        config_details = json.load(json_file)

    name = 'scrap_product'
    #domain to crawl 
    allowed_domains = config_details['allowed_domains']
    start_urls = config_details['start_urls']

    #creating rules
    rules=[]
    for i,selector in enumerate(config_details['restrict_css']):
        print(i,selector)
        link_extract= LinkExtractor(restrict_css=selector)
        callback= ['parse_item' if config_details["callback"][i]==True else None][0]
        follow= [True if config_details["follow"][i]==True else False][0]
        print(callback,follow)
        rules.append(Rule(link_extract,callback=callback,follow=follow))
    rules= tuple(rules)
    
# parsing items
    def parse_item(self, response):
        print("##############")
        print("Parsing Data")
        print("##############")
        self.logger.info(f'parsing the current book detail from this {response.url}')
        item = {}
      
        #getting brand name for verification
        if self.config_details['brand_name']['response']=='css':
            print(self.config_details['brand_name']["selector"])
            brand_name=response.css(self.config_details['brand_name']["selector"]).get()
        # incase of xpath
        elif self.config_details['brand_name']['response']=='xpath' :
            brand_name=response.xpath(self.config_details['brand_name']["selector"]).get()
            
        print(brand_name,self.product_df['Brand'].values)   
             
        #first verification
        if brand_name in self.product_df['Brand'].values:
            print("##############")
            print("Brand Name Matched")
            print("##############")
       
            #second verification
            if self.config_details['product_name']['response']=='css':
                product_name=response.css(self.config_details['product_name']['selector']).get()
            # incase of xpath
            else:
                product_name=response.xpath(self.config_details['product_name']['selector']).get()
            # print("ProductName", product_name)
            
            for p in self.product_df[self.product_df['Brand']==brand_name]['Name'].values:
                if p in product_name:
                    print("##############")
                    print("Product Matched")
                    print("##############")     
                                
                    item['Product_Name']=' '.join(product_name.split(' ')[1:])
                    item['Brand']= brand_name
                    product_details= self.config_details['product_details']
                    for key in product_details.keys():
                        product_info=product_details[key]  
                        if product_info=="NA" :
                           item[key]='NA'
                        elif product_info['response']=='css':
                            item[key]=response.css(product_info['selector']).get()
                            # incase of xpath
                        else:
                            item[key]=response.xpath(product_info['selector']).get() 
                    item['url']= response.url

        else:
            return 
        if len(item.keys())==0:
            return
        else:
            print("##############")
            print('Creating/Adding in Database')
            print("##############")
            #creating it in the database
            
            print(type(item),item)
            df= pd.DataFrame(item,index=[0])
            df.to_sql('product_details',self.conn, if_exists='append',index=False)
            print(pd.read_sql("SELECT * FROM product_details", self.conn))
            yield item  

        
            
 
        
