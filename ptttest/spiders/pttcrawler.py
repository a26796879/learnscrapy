import scrapy
from ..items import PtttestItem, PttImage

domain = 'http://ptt.cc'

#符合圖片格式的網址
def isImageFormat(link):
    if(link.find('.jpg') > -1 or link.find('.png') > -1 or link.find('.gif') > -1 or link.find('.jpeg') > -1):
       return True
    return False

class PttSpider(scrapy.Spider):
    name = 'pttbeauty'
    start_urls = ['https://www.ptt.cc/bbs/Beauty/index.html']

    def parse(self, response):
        items = PtttestItem()
        for content in response.css('div.r-ent'):
            items['push'] = content.css('div.nrec > span.hl::text').extract_first(),
            items['title'] = content.css('div.title > a::text').extract_first(),
            items['href'] = content.css('div.title > a::attr(href)').extract_first(),
            items['date'] = content.css('div.meta > div.date ::text').extract_first(),
            items['author'] = content.css('div.meta > div.author ::text').extract_first(),
            href_url = domain + response.css('div.title > a::attr(href)').extract_first()
            item = PttImage()
            yield scrapy.Request(href_url, callback = self.parse_images, meta={'item': item}) 
            #yield scrapy.Request(href_url, callback = self.parse_images, meta={'item': item})
            #yield items
        nextpg = 'http://ptt.cc' + response.css("div.btn-group.btn-group-paging > a.btn.wide::attr(href)").extract()[1]
        url = response.urljoin(nextpg)
        yield scrapy.Request(url, self.parse)
        
    def parse_images(self, response):  
        item = response.meta['item']
        imgurls = []
        #取得每篇文章內的 圖片
        for img in response.xpath('//a/@href'):
            url = img.extract()
            if(isImageFormat(url)):
                imgurls.append(url)
            item['image_urls'] = imgurls
        return item

    def isImageFormat(link):
        if(link.find('.jpg') > -1 or link.find('.png') > -1 or link.find('.gif') > -1 or link.find('.jpeg') > -1):
            return True;
        return False;

