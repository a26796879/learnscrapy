import scrapy

class PttSpider(scrapy.Spider):
    name = 'pttbeauty'
    start_urls = ['https://www.ptt.cc/bbs/Beauty/index.html']

    def parse(self, response):
        titles = response.css("div.r-ent > div.title > a::text").extract()
        votes = response.css("div.r-ent > div.nrec > span::text").extract()
        authors = response.css("div.r-ent > div.meta > div.author::text").extract()

        for item in zip(titles,votes,authors):
            scraped_info = {
                "title" : item[0],
                "vote" : item[1],
                "author": item[2],
            }
            yield scraped_info

        nextpg = response.css("div.btn-group.btn-group-paging > a.btn.wide::attr(href)").extract()[1]
        print(nextpg)