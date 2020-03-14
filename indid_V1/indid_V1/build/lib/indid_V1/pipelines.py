# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class IndidV1Pipeline(object):
    def __init__(self):
        host = "database-job-posts.c1qytdm4eno0.us-east-1.rds.amazonaws.com"

        port =int(3306)
        dbname="job_posts"
        user="timaun4db"
        password="WSsmdIep4db2e"
        self.conn = pymysql.connect(host, user=user,port=port, passwd=password, db=dbname)
        self.curr = self.conn.cursor()
    def store_db(self, item):
        self.curr.execute("""INSERT INTO primary_job_posts(job_title, company, location, date,description,\
            day,posted_date, state, city, term)\
            VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")"""\
            .format(item['job_title'],item['company'],item['location'],item['date'],item['description']\
                   ,item['day'],item['posted_date'], item['state'],item['city'],item['search_term']))
        self.conn.commit()
		
    def process_item(self, item, spider):
        self.store_db(item)
        return item