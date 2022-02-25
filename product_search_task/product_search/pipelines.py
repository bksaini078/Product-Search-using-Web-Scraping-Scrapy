# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3 as sql
import pandas as pd


class ProductSearchPipeline:
    def process_item(self, item, spider):
        '''
        This part particularly related to pre-processing steps. 
        '''
       
        return item
