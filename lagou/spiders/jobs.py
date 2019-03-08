# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    #allowed_domains = ['sss']
    start_urls = ['https://www.lagou.com/']
    item = {}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga=GA1.2.1825342393.1551871647; user_trace_token=20190306192726-d1fb0d46-4002-11e9-9c4d-525400f775ce; LGUID=20190306192726-d1fb1192-4002-11e9-9c4d-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; _qddaz=QD.ata2qw.xzy69a.jsxd1nax; _gid=GA1.2.61206603.1552018795; JSESSIONID=ABAAABAAAFCAAEGDF9E9774505BD8F40F0729A17A77A127; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551871647,1551873989,1552056888; TG-TRACK-CODE=index_navigation; SEARCH_ID=af692b59d815485b9db6190adde2b208; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552057238; LGRID=20190308230038-ef27eb49-41b2-11e9-adab-525400f775ce',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/zhaopin/Java/?labelWords=label',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse, headers=self.headers, meta={'tag':0})

    def parse(self, response):

        selectorOne = response.xpath('//div[@class="menu_box"]')
        for s in selectorOne[:1]:
            categoryOne = s.xpath('.//h2/text()').extract_first().strip().strip('\n')
            selectorTwo = s.xpath('./div[@class="menu_sub dn"]/dl/dt')
            categoryTwo = selectorTwo.xpath('./span/text()').extract()
            self.item[categoryOne] = {q: {} for q in categoryTwo}
            for q in selectorTwo[:1]:
                s = q.xpath('./span/text()').extract_first()
                selectorThree = q.xpath('./following-sibling::dd')
                categoryThree = selectorThree.xpath('./a/text()').extract()
                self.item[categoryOne][s] = {q: {} for q in categoryThree}
                for m in selectorThree[:1]:
                    selectorFour = m.xpath('./a')
                    for n in selectorFour[:1]:
                        p = n.xpath('./text()').extract_first()
                        href = m.xpath(f'./a[contains(text(),"{p}")]/@href').extract_first()
                        self.item[categoryOne][s][p] = {}
                        yield Request(href, callback=self.parseItem, headers=self.headers, meta={'href': href, 'a': categoryOne, 'b': s, 'c': p, 'tag':0})
        with open('cat.json', 'w', encoding='utf-8') as f:
            json.dump(self.item, f, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)

    def parseItem(self, response):
        links = response.xpath('//ul[@class="item_con_list"]/li//a[@class="position_link"]/@href').extract()
        for link in links[:2]:
            yield Request(link,  callback=self.parsePlus, meta={'href': response.meta['href'], 'a': response.meta['a'], 'b': response.meta['b'], 'c': response.meta['c'], 'tag':0})

    def parsePlus(self, response):
        a = response.meta['a']
        b = response.meta['b']
        c = response.meta['c']
        position = response.xpath('//div[@class="job-detail"]/p/text()').extract_first().split(':')[-1]
        company = response.xpath('//div[@class="job-name"]/div[@class="company"]/text()').extract_first()
        salary = response.xpath('//dd[@class="job_request"]//span[@class="salary"]/text()').extract_first()
        place = response.xpath('//dd[@class="job_request"]//span[2]/text()').extract_first().replace("/", "")
        experience = response.xpath('//dd[@class="job_request"]//span[3]/text()').extract_first().replace("/", "")
        diplomat = response.xpath('//dd[@class="job_request"]//span[4]/text()').extract_first().replace("/", "")
        workTime = response.xpath('//dd[@class="job_request"]//span[5]/text()').extract_first().replace("/", "")
        jobAdvantage = response.xpath('//dd[@class="job-advantage"]/p/text()').extract_first()
        jobInfo = response.xpath('string(//div[@class="job-detail"]/p)').extract_first()
        self.item[a][b][c] = {
            'position': position,
            'company': company,
            'salary': salary,
            'palce': place,
            'experience': experience,
            'diplomat': diplomat,
            'workTime': workTime,
            'jobAdvantage': jobAdvantage,
            'jobInfo': jobInfo,
        }
        print(self.item[a][b][c])

