# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo[c][0]=1']

    def parse(self, response):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css('div._3zucV div.f-test-vacancy-item a.icMQ_._3dPok::attr(href)').extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacansy_parse)


    def vacansy_parse(self, response: HtmlResponse):
        url = response.url
        name = response.css('div._3zucV h1::text').extract_first()
        salary = ''.join(response.css('div._3zucV span.PlM3e span::text').extract())
        employer = response.css('div.Ghoh2 a.icMQ_ h2::text').extract_first()
        yield JobparserItem(name=name, salary=salary, url=url, employer=employer)