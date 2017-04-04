# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.mail import MailSender
import socket

# gets a short hostname of the computer
def get_host():
    hn = socket.gethostname()
    return hn.split('.')[0]

# following https://doc.scrapy.org/en/latest/intro/tutorial.html
class MemegeneratorSpider(scrapy.Spider):
    name = "memegenerator"
    allowed_domains = ["version1.api.memegenerator.net"]
    start_urls = ['http://version1.api.memegenerator.net/']
    custom_settings = {
            'DNS_TIMEOUT': 5,
            'MAIL_FROM': 'scrapy@'+get_host()
    }

    def __init__(self, lower='0', upper='0', filename='memes.txt', *args, **kwargs):
        super(MemegeneratorSpider, self).__init__(*args, **kwargs)
        self.lower = int(lower)
        self.upper = int(upper)
        self.filename = filename
        self.total = 0
        self.success = 0
        self.mailer = MailSender()

    # first pass: use Memegenerator API
    def start_requests(self):
        # get memes by memeID
        id_generator = self.get_pages_by_id(self.lower, self.upper)
        for url in id_generator:
            yield scrapy.Request(url=url, callback=self.parse)

    def close(self):
        # email done status update
        self.email_status_update(done=True)
    
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
    def parse(self, response):
        self.total += 1
        page = response.url
        json_response = json.loads(response.body)
        if json_response['success']:
            self.success += 1
            # successfully got JSON, parse and write to file
            result = json_response['result']
            with open(self.filename, 'a') as f:
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
        if self.total % 100000 == 0:
            self.email_status_update()

    def email_status_update(self, done=False):
        total = self.total
        success = self.success
        to = 'jthurst3@u.rochester.edu'
        subject = '[MemeCaptcha automatic message] Scrape status for ' + get_host() + ':'
        body = ''
        if done:
            body += 'Done scraping.'
        else:
            body += 'In the middle of scraping.'
        body += ' Stats:\n'
        body += '\tStart ID      : ' + str(self.lower) + '\n'
        body += '\tEnd ID        : ' + str(self.upper) + '\n'
        body += '\tCurrent ID    : ' + str(self.lower+total) + '\n'
        body += '\tSuccessful IDs: ' + str(success) + '\n'
        body += '\tSuccess rate  : ' + str(float(success)/total) + '\n'
        body += '\tProgress      : ' + str(float(total)/(self.upper-self.lower)) + '\n'

        self.mailer.send(to=[to], subject=subject, body=body)
        

