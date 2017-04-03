# -*- coding: utf-8 -*-
import json
import scrapy

# following https://doc.scrapy.org/en/latest/intro/tutorial.html
class MemegeneratorSpider(scrapy.Spider):
    name = "memegenerator"
    allowed_domains = ["version1.api.memegenerator.net"]
    start_urls = ['http://version1.api.memegenerator.net/']

    custom_settings = {
            'DNS_TIMEOUT': 5,
    }

    # first pass: use Memegenerator API
    def start_requests(self):
        # use the Popular Page generator first
        # id_generator = self.get_pages_by_id(9000000, 9001000)
        id_generator = self.get_pages_by_id(9000000, 9001000)
        for url in id_generator:
            yield scrapy.Request(url=url, callback=self.parse)

    # tries to get all pages in the range [start, end)
    def get_pages_by_id(self, start, end):
        pageid = start
        while pageid < end:
            yield 'http://version1.api.memegenerator.net/Instance_Select?instanceID='+str(pageid)
            pageid += 1

    # iterate over popular pages
    def get_popular_page_url(self, max_page):
        page_index = 50
        while page_index < max_page:
            yield 'http://version1.api.memegenerator.net/Instances_Select_ByPopular?languageCode=en&urlName=&days=&pageIndex='+str(page_index)
            page_index += 1

    # parse memegenerator API response and put into JSON file
    def parse(self, response, filename='memes_id.txt'):
        page = response.url
        json_response = json.loads(response.body)
        if json_response['success']:
            # successfully got JSON, parse and write to file
            result = json_response['result']
            with open(filename, 'a') as f:
                if type(result) is list:
                    for meme in result:
                        json.dump(meme, f)
                        f.write('\n')
                else:
                    json.dump(result, f)
                    f.write('\n')
        else:
            # failed to get JSON, log
            self.log('id %s does not exist' % page.split('=')[-1])
            self.log('error: %s' % json_response['errorMessage'])

