import scrapy

class MySpider(scrapy.Spider):
    name = 'wencai_spider'
    start_urls = ['http://example.com']

    def parse(self, response):
        print("寄哪里")
        # 提取页面上的标题和链接
        titles = response.css('h1::text').extract()
        links = response.css('a::attr(href)').extract()

        # 打印提取的信息
        for title, link in zip(titles, links):
            print(f'Title: {title}, Link: {link}')

        # 可以继续爬取下一页的链接
        next_page = response.css('a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
