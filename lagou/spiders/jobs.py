# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    #allowed_domains = ['sss']
    start_urls = ['https://www.lagou.com/']
    item = {}
    headers = {
        'Vary': 'Accept-Encoding',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.2.1825342393.1551871647; user_trace_token=20190306192726-d1fb0d46-4002-11e9-9c4d-525400f775ce; LGUID=20190306192726-d1fb1192-4002-11e9-9c4d-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; _qddaz=QD.ata2qw.xzy69a.jsxd1nax; JSESSIONID=ABAAABAAAFCAAEGDF9E9774505BD8F40F0729A17A77A127; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551871647,1551873989,1552056888; TG-TRACK-CODE=index_navigation; _gid=GA1.2.829201508.1552201558; LGSID=20190310170738-f40e9adc-4313-11e9-9a2c-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; SEARCH_ID=f69e7547c810405c91b94ae0c2c2463c; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552210362; LGRID=20190310173241-73bae9ad-4317-11e9-90b4-5254005c3644; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216966f27e0d3e-03bfafc9590fd7-18211c0a-1225080-16966f27e0e14f%22%2C%22%24device_id%22%3A%2216966f27e0d3e-03bfafc9590fd7-18211c0a-1225080-16966f27e0e14f%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=f239d3746485bc49bec7deadfb33731065dca12bdad8507dbc0d2f59a02d5350; _putrc=906B4DAEF0CEB1B2123F89F2B170EADC; login=true; unick=%E4%B9%A0%E9%83%81%E8%8D%86; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=13; gate_login_token=1f65a269138b36dcdb9f597a64102d91e9f2c86a747feae3e4879920a3ef3ddb',
        #'Cookie': '_ga=GA1.2.1825342393.1551871647; user_trace_token=20190306192726-d1fb0d46-4002-11e9-9c4d-525400f775ce; LGUID=20190306192726-d1fb1192-4002-11e9-9c4d-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; _qddaz=QD.ata2qw.xzy69a.jsxd1nax; JSESSIONID=ABAAABAAAFCAAEGDF9E9774505BD8F40F0729A17A77A127; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551871647,1551873989,1552056888; TG-TRACK-CODE=index_navigation; _gid=GA1.2.829201508.1552201558; PRE_UTM=; PRE_HOST=; LGSID=20190310150558-f4800688-4302-11e9-994c-525400f775ce; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5599887.html; SEARCH_ID=602a99dcf0074fbb8c4ae8fa0dfc78f2; _gat=1; LGRID=20190310153158-969051fd-4306-11e9-90ad-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552203119',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/',
        #'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse, headers=self.headers, meta={'tag':0}, dont_filter=True)

    def parse(self, response):
        selectorOne = response.xpath('//div[@class="menu_box"]')
        for s in selectorOne:
            categoryOne = s.xpath('.//h2/text()').extract_first().strip().strip('\n')
            selectorTwo = s.xpath('./div[@class="menu_sub dn"]/dl/dt')
            categoryTwo = selectorTwo.xpath('./span/text()').extract()
            self.item[categoryOne] = {q: {} for q in categoryTwo}
            for q in selectorTwo:
                s = q.xpath('./span/text()').extract_first()
                selectorThree = q.xpath('./following-sibling::dd')
                categoryThree = selectorThree.xpath('./a/text()').extract()
                self.item[categoryOne][s] = {q: {} for q in categoryThree}
                for m in selectorThree:
                    selectorFour = m.xpath('./a')
                    for n in selectorFour:
                        p = n.xpath('./text()').extract_first()
                        href = m.xpath(f'./a[contains(text(),"{p}")]/@href').extract_first()
                        self.item[categoryOne][s][p] = {}
                        yield Request(href, callback=self.parseItem, headers=self.headers, meta={'href': href, 'a': categoryOne, 'b': s, 'c': p, 'tag':0}, dont_filter=True)


    def parseItem(self, response):
        links = response.xpath('//ul[@class="item_con_list"]/li//a[@class="position_link"]/@href').extract()
        headers = {
            'Vary': 'Accept-Encoding',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '_ga=GA1.2.1825342393.1551871647; user_trace_token=20190306192726-d1fb0d46-4002-11e9-9c4d-525400f775ce; LGUID=20190306192726-d1fb1192-4002-11e9-9c4d-525400f775ce; _qddaz=QD.ata2qw.xzy69a.jsxd1nax; JSESSIONID=ABAAABAAAFCAAEGDF9E9774505BD8F40F0729A17A77A127; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551871647,1551873989,1552056888; _gid=GA1.2.829201508.1552201558; LGSID=20190310170738-f40e9adc-4313-11e9-9a2c-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216966f27e0d3e-03bfafc9590fd7-18211c0a-1225080-16966f27e0e14f%22%2C%22%24device_id%22%3A%2216966f27e0d3e-03bfafc9590fd7-18211c0a-1225080-16966f27e0e14f%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=f239d3746485bc49bec7deadfb33731065dca12bdad8507dbc0d2f59a02d5350; _putrc=906B4DAEF0CEB1B2123F89F2B170EADC; login=true; unick=%E4%B9%A0%E9%83%81%E8%8D%86; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=13; gate_login_token=1f65a269138b36dcdb9f597a64102d91e9f2c86a747feae3e4879920a3ef3ddb; index_location_city=%E6%B7%B1%E5%9C%B3; _gat=1; TG-TRACK-CODE=index_navigation; SEARCH_ID=04c453a8debe4a0597f9a7b13988ed10; LGRID=20190310181312-1cc17b1d-431d-11e9-9a7c-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552212793',
            #'Cookie': '_ga=GA1.2.1825342393.1551871647; user_trace_token=20190306192726-d1fb0d46-4002-11e9-9c4d-525400f775ce; LGUID=20190306192726-d1fb1192-4002-11e9-9c4d-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; _qddaz=QD.ata2qw.xzy69a.jsxd1nax; JSESSIONID=ABAAABAAAFCAAEGDF9E9774505BD8F40F0729A17A77A127; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551871647,1551873989,1552056888; TG-TRACK-CODE=index_navigation; _gid=GA1.2.829201508.1552201558; PRE_UTM=; PRE_HOST=; LGSID=20190310150558-f4800688-4302-11e9-994c-525400f775ce; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5599887.html; SEARCH_ID=602a99dcf0074fbb8c4ae8fa0dfc78f2; _gat=1; LGRID=20190310153158-969051fd-4306-11e9-90ad-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552203119',
            'Host': 'www.lagou.com',
            'Referer': f'{response.url}',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        for link in links:
            yield Request(link,  headers=headers, callback=self.parsePlus, meta={'href': response.meta['href'], 'a': response.meta['a'], 'b': response.meta['b'], 'c': response.meta['c'], 'tag':0}, dont_filter=True)

    def parsePlus(self, response):
        a = response.meta['a']
        b = response.meta['b']
        c = response.meta['c']
        position = response.xpath('//span[@class="name"]/text()').extract_first()
        company = response.xpath('//div[@class="job-name"]/div[@class="company"]/text()').extract_first()
        salary = response.xpath('//dd[@class="job_request"]//span[@class="salary"]/text()').extract_first()
        place = response.xpath('//dd[@class="job_request"]//span[2]/text()').extract_first().replace("/", "")
        experience = response.xpath('//dd[@class="job_request"]//span[3]/text()').extract_first().replace("/", "")
        diplomat = response.xpath('//dd[@class="job_request"]//span[4]/text()').extract_first().replace("/", "")
        workTime = response.xpath('//dd[@class="job_request"]//span[5]/text()').extract_first().replace("/", "")
        jobAdvantage = response.xpath('//dd[@class="job-advantage"]/p/text()').extract_first()
        jobInfo = response.xpath('string(//div[@class="job-detail"]/p)').extract_first()
        self.item[a][b][c][position] = {
            'company': company,
            'salary': salary,
            'palce': place,
            'experience': experience,
            'diplomat': diplomat,
            'workTime': workTime,
            'jobAdvantage': jobAdvantage,
            'jobInfo': jobInfo,
        }
        rexcel = open_workbook("position.xls")  
        rows = rexcel.sheets()[0].nrows 
        excel = copy(rexcel)  
        table = excel.get_sheet(0) 
        row = rows
        table.write(row, 0, a)
        table.write(row, 1, b)
        table.write(row, 2, c)
        table.write(row, 3, position)
        excel.save("position.xls")
        print(self.item[a][b][c])
        with open('cat.json', 'w', encoding='utf-8') as f:
            json.dump(self.item, f, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)

