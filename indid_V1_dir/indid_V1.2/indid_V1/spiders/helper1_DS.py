import scrapy
from ..items import IndidV1Item
from datetime import datetime, timedelta
def get_date(date_string):
    try:
        if date_string and date_string.find('hour')== -1: 
            if date_string[1]=='-':        
               return int(date_string[3:5])
            else:
               return int(date_string[0:2])
    except ValueError:
        return 0
def get_state(a_location):
    if a_location and len(a_location.split(','))>1:
        return a_location.split(',')[-1][1:3]
    elif a_location and len(a_location.split(','))==1:
        return a_location.split(',')[-1]
    else:
        return None
def get_actual_date(day):
    return datetime.now()-timedelta(days = day)
def gest_city(loc_string):
    if len(loc_string.split(','))>1:
        return loc_string.split(',')[0]
    else:
        return None	
class Indeed1Spider(scrapy.Spider):
    name = 'indeed-DataScientist-weekly-update-helper'
    allowed_domains = ['indeed.com']
    
    states=['AK', 'AL', 'AR', 'AS', 'AZ', 'CO','CA', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN',\
    'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH',\
    'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UM', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']
    new_states = ['MA','MD','WA','VA','TX','PA','OH','NY','NJ','IL','FL','DC']
    start_urls = ['https://www.indeed.com/jobs?q=data+scientist&l={}&radius=0&fromage=9&sort=date&limit=50&filter=0'.format(state) for state in states]
    #start_urls =['https://www.indeed.com/jobs?q=machine+learning+engineer&l=los+angeles&radius=100&sort=date&limit=50',
    #'https://www.indeed.com/jobs?q=machine+learning+engineer&l=san+francisco&radius=35&sort=date&limit=50',
    #'https://www.indeed.com/jobs?q=machine+learning+engineer&l=san+jose&radius=25&sort=date&limit=50']

    def start_requests(self):
    
        for url in self.start_urls:
            yield scrapy.Request(url = url,
                            callback = self.parse_first_result, headers={"User-Agent": "Mozilla/5.0"},
                           meta={"proxy": "http://pxu15333-0:QvfYg4kOWGoW5plrJ$Ax@x.botproxy.net:8080"})
    def parse_first_result(self,response):
        global urls
        urls=list()
      
        urls.append(response.request.url)
      
        other_result_pgaes_links = response.xpath('//div[@class="pagination"]//a/@href').extract()
        if other_result_pgaes_links:
            print('an extra result page has found!!!')
            other_results_urls = ['https://www.indeed.com'+link for link in other_result_pgaes_links]
            urls.extend(other_results_urls[:-1])
            for url in urls:
                yield scrapy.Request(url = url,
                                 callback = self.parse_result_page,dont_filter=True, headers={"User-Agent": "Mozilla/5.0"},
                               meta={"proxy": "http://pxu15333-0:QvfYg4kOWGoW5plrJ$Ax@x.botproxy.net:8080"})
        else:
            print('the current url'+ response.request.url)
            yield scrapy.Request(url =response.request.url,
                                 callback = self.parse_result_page,dont_filter=True, headers={"User-Agent": "Mozilla/5.0"},
                               meta={"proxy": "http://pxu15333-0:QvfYg4kOWGoW5plrJ$Ax@x.botproxy.net:8080"}) 
    def parse_result_page(self, response):
        
        links = response.xpath('//h2[@class="title"]/a/@href')
    
        global links_to_follow
        links_extentions = links.extract()
    
        links_to_follow = ['https://www.indeed.com'+extention for extention in links_extentions]
        print('in '+response.request.url+ 'there exists: '+str(len(links_to_follow)))
    
        for url in links_to_follow:
        #sleep(np.random.uniform(10,32))
            yield response.follow(url = url,
                            callback = self.parse_pages, headers={"User-Agent": "Mozilla/5.0"},
                       meta={"proxy": "http://pxu15333-0:QvfYg4kOWGoW5plrJ$Ax@x.botproxy.net:8080"})                               
    def parse_pages(self,response):
        company_name = response.xpath('//div[contains(@class,"jobsearch-DesktopStickyContainer-companyrating")]/div[1]//text()').extract_first()
        date = response.xpath('//div[@class="jobsearch-JobMetadataFooter"]//text()').extract()
        if date[1] ==' - ':
            scraped_d = date[2]
        else:
            scraped_d = date[1]
        day = get_date(scraped_d)
        actual_date = get_actual_date(day).date()
        location = response.xpath('//div[contains(@class,"jobsearch-DesktopStickyContainer-companyrating")]/div[last()]/text()').extract_first()
        job_title = response.xpath('//div[contains(@class,"jobsearch-JobInfoHeader-title")]/h1/text()').extract_first()
        state = get_state(location)
        city = gest_city(location)
        job_description_list = response.xpath('//*[@id="jobDescriptionText"]//text()').extract()
        job_description = '\n'.join(job_description_list)
        job_description = job_description.replace('"','')
        item = IndidV1Item()
        item['job_title']= job_title.encode('utf-8')
        item['company'] = company_name.encode('utf-8')
        item['location'] = location.encode('utf-8') 
        item['date']=scraped_d.encode('utf-8')
        item['description']	= job_description.encode('utf-8')
        item['day']=day
        item['posted_date']	= actual_date	
        item['state']= state.encode('utf-8')
        item['search_term'] ='data scientist'
        item['city'] =city.encode('utf-8') if city else None
        yield item
		
        