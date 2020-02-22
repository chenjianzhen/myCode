import scrapy
from tutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):      # 继承scrapy.Spider类
    name = "quotes"     # 每个项目唯一的名称，用来区分不同的Spider
    allowed_domains = ['quotes.toscrape.com']       # 允许爬取的域名
    start_urls = ['http://quotes.toscrape.com/']    # Spider在启动时爬取的url列表，初始请求由它来定义

    def parse(self, response):
        """
        Spider的一个方法。默认调用start_urls的链接构成的请求完成下载，返回的响应会作为唯一的参数(response)传递给
        这个函数。该方法负责解析返回的响应、提取数据或者进一步生成要处理的请求。
        :param response:
        :return:
        """
        quotes = response.css(".quote")
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css(".text::text").extract_first()     # 获取列表里的第一个元素
            item['author'] = quote.css(".author::text").extract_first()     # 获取列表里的第一个元素
            item['tags'] = quote.css(".tags .tag::text").extract()      # 获取列表里的所有标签

        # 获取下一个页面的URL
        next_url = response.css('.pager .next a::attr(href)').extract_first()
        # 使用urljoin()方法把相对URL构造成绝对URL
        url = response.urljoin(next_url)
        # url和callback函数构造一个新的请求，回调函数使用parse()方法
        yield scrapy.Request(url=url, callback=self.parse)



