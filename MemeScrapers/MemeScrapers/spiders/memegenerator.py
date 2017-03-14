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
        popular_generator = self.get_popular_page_url(500)
        for url in popular_generator:
            yield scrapy.Request(url=url, callback=self.parse)

    # iterate over popular pages
    def get_popular_page_url(self, max_page):
        page_index = 0
        while page_index < max_page:
            yield 'http://version1.api.memegenerator.net/Instances_Select_ByPopular?languageCode=en&urlName=&days=&pageIndex='+str(page_index)
            page_index += 1

    # parse memegenerator API response and put into JSON file
    def parse(self, response):
        page = response.url
        json_response = json.loads(response.body)
        if json_response['success']:
            # successfully got JSON, parse and write to file
            memes = json_response['result']
            with open('first_memes.txt', 'a') as f:
                for meme in memes:
                    json.dump(meme, f)
                    f.write('\n')
        else:
            # failed to get JSON, log
            self.log('Failed to get JSON from URL %s' % url)

