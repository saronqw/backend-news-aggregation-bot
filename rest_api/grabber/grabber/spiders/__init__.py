# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import re
import sys

import scrapy


# scrapy crawl caltech_news
from rest_api.grabber.grabber.items import ScrapyNewsItem, ScrapyUniversityItem
from rest_api.models import University, NewsItem


class CaltechSpider(scrapy.Spider):
    name = "caltech_news"
    universityId = 6
    lastTitle = (NewsItem.objects.filter(university_id=universityId).order_by('-pub_date')[0]).title
    start_urls = [
        'https://www.caltech.edu/about/news?&p=1',
    ]
    url = 'https://www.caltech.edu/about/news?&p={}'
    page = 1

    date = sys.argv[0]

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    def parseNewsPage(self, response):

        title = response.css(
            'div.simple-news-header-block.mb-5.py-5 h1.simple-news-header-block__title.mb-3::text').get()
        if title is None:
            title = response.css(
                'h1.news-hero-header-block__info__title::text').get()
        description = response.css('div.rich-text p::text').get().strip()
        if description is None or description == 'None' or description == '':
            description = str(response.css('div.rich-text p span::text').get()).strip()
            if description is None or description == 'None' or description == '':
                description = str(response.css('div.video-block__info__caption.px-4::text').get()).strip()
                if description is None or description == 'None' or description == '':
                    description_array = response.css('div.rich-text div::text').getall()
                    description = ' '.join(str(d) for d in description_array)

        regex = re.compile(r'[\n\r\t]|  +')
        description = (regex.sub("", description)).strip()
        datatime = response.css('div.publish-date-block__date::text').get()
        newsUrl = response.request.url

        if description != "":
            yield {
                'title': (title).strip(),
                'description': (description),
                'link': newsUrl,
                'pub_date': (datatime).strip(),
                'university_id': '56',
            }

    def parse(self, response):
        for quote in response.css('div.article-teaser'):
            newsURL = quote.css('div.article-teaser__title a.article-teaser__link::attr(href)').get()
            news_date = quote.css('span.article-teaser__published-date__date::text').get()
            # date = DT.datetime.strptime(text, '%Y%m%d').date()
            yield scrapy.Request('https://www.caltech.edu{}'.format(newsURL), headers=self.headers,
                                 callback=self.parseNewsPage)

        last_page = 'https://www.caltech.edu{}'.format(response.css(
            'a.news-article-list__paginator__link-box.news-article-list__paginator__last-page::attr(href)').get())
        self.page += 1
        next_page = self.url.format(self.page)

        # if next_page != last_page:
        # yield response.follow(next_page, callback=self.parse)




# scrapy crawl cambridge_news

class CambridgeSpider(scrapy.Spider):
    name = "cambridge_news"
    universityId = 7
    lastTitle = (NewsItem.objects.filter(university_id=universityId).order_by('-pub_date')[0]).title
    start_urls = [
        'https://www.cam.ac.uk/news?page=0',
    ]

    def parse(self, response):
        for quote in response.css('article.clearfix.cam-horizontal-teaser.cam-teaser'):
            title = str(quote.css('h3.cam-teaser-title a::text').get()).strip()
            description = str(quote.css('div.field-item.even::text').get()).strip()
            if description is None or description == 'None' or description == '':
                description = str(quote.css('div.field-item.even p::text').get()).strip()
                if description is None or description == 'None' or description == '':
                    description = str(quote.css('div.field-item.even p span::text').get()).strip()
                    if description is None or description == 'None' or description == '':
                        description = str(quote.css('div.field-item.even div::text').get()).strip()
                        if description is None or description == 'None' or description == '':
                            description = str(quote.css('div.field-item.even p strong b::text').get()).strip()
                            if description is None or description == 'None' or description == '':
                                description = str(quote.css('div.field-item.even strong::text').get()).strip()
                                if description is None or description == 'None' or description == '':
                                    description = str(quote.css('div.field-item.even em::text').get()).strip()
            regex = re.compile(r'[\n\r\t]|  +')
            description = (regex.sub("", description))
            datatime = quote.css('span.cam-datestamp::text').get()
            newsUrl = quote.css('h3.cam-teaser-title a::attr(href)').get()
            yield {
                'title': title,
                'description': description,
                'link': 'https://www.cam.ac.uk{}'.format(newsUrl),
                'pub_date': datatime,
                'university_id': '199',
            }

        next_page = response.css('li.pager-next.last a::attr(href)').get()
        #if next_page is not None:
            #yield response.follow('https://www.cam.ac.uk{}'.format(next_page), callback=self.parse)


# scrapy crawl harvard_news

class HarvardSpider(scrapy.Spider):
    name = "harvard_news"
    universityId = 4
    lastTitle = (NewsItem.objects.filter(university_id=universityId).order_by('-pub_date')[0]).title
    start_urls = [
        'https://news.harvard.edu/gazette/section/news_plus',
    ]

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    def parseNewsPage(self, response):

        title = response.css('div.article-titles__titles h1.article-titles__title::text').get()
        description_array = response.css('div.article-body.basic-text p::text').getall()
        description = (' '.join(str(d) for d in description_array))
        regex = re.compile(r'[\n\r\t]|  +')
        description = (regex.sub("", description)).strip()
        if description is None or description == 'None' or description == '':
            description_array = response.css('div.article-body.basic-text p span::text').getall()
            description = (' '.join(str(d) for d in description_array))
            regex = re.compile(r'[\n\r\t]|  +')
            description = (regex.sub("", description)).strip()

        datatime = response.css('p.article-posted-on time.timestamp::attr(datetime)').get()
        newsUrl = response.request.url
        yield {
            'title': title,
            'description': description,
            'link': newsUrl,
            'pub_date': datatime,
            'university_id': '4',
        }

    def parse(self, response):
        for quote in response.css('div.tz-article-image__meta'):
            newsURL = quote.css('h2.tz-article-image__title a::attr(href)').get()

            yield scrapy.Request(newsURL, headers=self.headers,
                                 callback=self.parseNewsPage)

        next_page = response.css('div.nav-previous a::attr(href)').get()
        # if next_page is not None:
        # yield response.follow(next_page, callback=self.parse)



class ItmoSpider(scrapy.Spider):
    name = "itmo_news"
    universityId = 8
    lastTitle = (NewsItem.objects.filter(university_id=universityId).order_by('-pub_date')[0]).title
    start_urls = [
        'https://news.itmo.ru/en/science/it/',
        'https://news.itmo.ru/en/science/photonics/',
        'https://news.itmo.ru/en/science/cyberphysics/',
        'https://news.itmo.ru/en/science/new_materials/',
        'https://news.itmo.ru/en/science/life_science/',

        'https://news.itmo.ru/en/education/cooperation/',
        'https://news.itmo.ru/en/education/trend/',
        'https://news.itmo.ru/en/education/students/',
        'https://news.itmo.ru/en/education/ministry_of_education/',
        'https://news.itmo.ru/en/education/official/',

        'https://news.itmo.ru/en/startups_and_business/business_success/',
        'https://news.itmo.ru/en/startups_and_business/innovations/',
        'https://news.itmo.ru/en/startups_and_business/startup/',
        'https://news.itmo.ru/en/startups_and_business/partnership/',
        'https://news.itmo.ru/en/startups_and_business/initiative/',

        'https://news.itmo.ru/ru/university_live/ratings/',
        'https://news.itmo.ru/ru/university_live/achievements/',
        'https://news.itmo.ru/ru/university_live/leisure/',
        'https://news.itmo.ru/ru/university_live/ads/',
        'https://news.itmo.ru/ru/university_live/social_activity/',

    ]

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }


    def parseNewsPage(self, response):
        title = response.css('div.article article h1::text').get()
        description_array = response.css('div.article article strong::text').getall()
        description = ' '.join(str(d) for d in description_array)
        regex = re.compile(r'[\n\r\t]|  +')
        description = (regex.sub("", description))
        datatime = response.css('div.news-info-wrapper time::attr(datetime)').get()
        newsUrl = response.request.url

        yield {
            'title': title,
            'description': description,
            'link': newsUrl,
            'pub_date': datatime,
            'university_id': '7',
        }

    def parse(self, response):
        for quote in response.css('ul.triplet li'):
            newsURL = quote.css('h4 a::attr(href)').get()
            yield scrapy.Request('https://news.itmo.ru{}'.format(newsURL), headers=self.headers,
                                 callback=self.parseNewsPage)

        next_page = response.css('ul.pagination-custom.row.flex-center div.col-1 a::attr(href)').getall()[1]
        #if next_page is not None:
            #yield response.follow(next_page, callback=self.parse)


# scrapy crawl nsu_news

class NsuSpider(scrapy.Spider):
    name = "nsu_news"
    universityId = 3
    lastTitle = (NewsItem.objects.filter(university_id=universityId).order_by('-pub_date')[0]).title
    start_urls = [
        'https://english.nsu.ru/news-events/news/',
    ]

    url = 'https://english.nsu.ru/news-events/news/?PAGEN_1={}'
    page_num = 1
    '''
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }
    '''

    def parse(self, response):
        for quote in response.css('div.news-card'):
            title = str(quote.css('a.name::text').get()).strip()
            description = str(quote.css('p::text').get()).strip()
            datatime = quote.css('div.date::text').get()
            newsUrl = 'https://english.nsu.ru{}'.format(quote.css('a.name::attr(href)').get())
            yield {
                'title': title,
                'description': description,
                'link': newsUrl,
                'pub_date': datatime,
                'university_id': '3',
            }

        next_page = response.css('a.moreNewsList.loadMoreButton').get()
        self.page_num += 1
        #if next_page is not None:
            #yield response.follow(self.url.format(self.page_num), callback=self.parse)


# scrapy crawl nus_news



class NusSpider(scrapy.Spider):
    name = "nus_news"
    universityId = 9
    lastTitle = (NewsItem.objects.filter(university_id=universityId).order_by('-pub_date')[0]).title
    start_urls = [
        'https://news.nus.edu.sg/highlights?field_categories_target_id=All&page=0',
    ]

    def parse(self, response):
        for quote in response.css('div.col-lg-6.col-md-6.col-sm-6.col-xs-12.highlight-top'):
            title = str(quote.css('h2.highlight-title a::text').get()).strip()
            regex = re.compile(r'[\n\r\t]|  +')
            description = (regex.sub("", str(quote.css('div.field-content.introtxt p::text').get()))).strip()
            if description is None or description == 'None' or description == '':
                description_array = response.css('div.field-content.introtxt p span span::text').getall()
                description = ' '.join(str(d) for d in description_array)
                regex = re.compile(r'[\n\r\t]|  +')
                description = (regex.sub("", description))

            datatime = quote.css('span.views-field.views-field-created span.field-content::text').get()
            newsUrl = quote.css('h2.highlight-title a::attr(href)').get()
            yield {
                'title': title,
                'description': description,
                'link': newsUrl,
                'pub_date': datatime,
                'university_id': '153',
            }

        next_page = response.css('li.pager__item--next a::attr(href)').get()
        #if next_page is not None:
            #yield response.follow('https://news.nus.edu.sg/highlights{}'.format(next_page), callback=self.parse)


# scrapy crawl spbu_news

class SpbuSpider(scrapy.Spider):
    name = "spbu_news"
    universityId = 10
    lastTitle = (NewsItem.objects.filter(university_id=universityId).order_by('-pub_date')[0]).title
    start_urls = [
        'https://spbu.ru/news-events/novosti',
    ]

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    def parseNewsPage(self, response):

        title = response.css('h1.post__title::text').get()
        description = str(response.css('p.post__desc ::text').get()).strip()
        if description is None or description == 'None' or description == '':
            description = str(response.css('div.editor.editor--medium p::text').get()).strip()
        datatime = response.css('span.date-display-single::attr(content)').get()
        newsUrl = response.request.url
        if title != "   \n                            Материалы ректорского совещания                      " and description != 'None':
            yield {
                'title': title,
                'description': description,
                'link': newsUrl,
                'pub_date': datatime,
                'university_id': '4',
        }

    def parse(self, response):
        for quote in response.css('div.card-context'):
            newsURL = quote.css('a.card__media::attr(href)').get()


            yield scrapy.Request('https://spbu.ru{}'.format(newsURL), headers=self.headers,
                                 callback=self.parseNewsPage)

        next_page = response.css('li.pagination__item.pagination__next.last a::attr(href)').get()
        #if next_page is not None:
            #yield response.follow(next_page, callback=self.parse)


# scrapy crawl stanford_news

class StanfordSpider(scrapy.Spider):
    name = "stanford_news"
    universityId = 5
    lastTitle = (NewsItem.objects.filter(university_id=universityId).order_by('-pub_date')[0]).title
    start_urls = [
        'http://med.stanford.edu/news/all-news.html?main_news_builder_start=0',
    ]

    def parse(self, response):
        for quote in response.css('li.newsfeed-item.row'):
            title = str(quote.css('h3.newsfeed-item-title::text').get()).strip()
            description = str(quote.css('p.newsfeed-item-excerpt::text').get()).strip()
            datatime = quote.css('div.pull-left time::attr(datetime)').get()
            newsUrl = 'http://med.stanford.edu{}'.format(quote.css('div.col-xs-9.col-sm-8 a::attr(href)').get())
            if description != 'None' and datatime is not None:
                yield {
                    'title': title,
                    'description': description,
                    'link': newsUrl,
                    'pub_date': datatime,
                    'university_id': '5',
                }

        next_page = response.css('div.next a::attr(href)').get()
        #if next_page is not None:
            #yield response.follow('http://med.stanford.edu{}'.format(next_page), callback=self.parse)


# scrapy crawl tpu_news
# ломаные
# TPU delegation at WSEC-2017
# TPU – only Russian university presented in national exposition at Astana Expo 2017
#from rest_api.grabber.grabber.grabber_runer import getLastNewsTitleByID


class TpuSpider(scrapy.Spider):
    name = "tpu_news"
    universityId = 1
    lastTitle = (NewsItem.objects.filter(university_id=universityId).order_by('-pub_date')[0]).title
    start_urls = [
        'https://news.tpu.ru/en/news/',
    ]

    def parse(self, response):

        for quote in response.css('div.row div.col-lg-9.item-body'):
            title = str(quote.css('h3.title::attr(title)').get()).strip()
            regex = re.compile(r'[\n\r\t]|  +')
            description = (regex.sub("", str(quote.css('div.description::text').get()))).strip()
            datatime = quote.css('div.date time::attr(datetime)').get()
            newsUrl = quote.css('a::attr(href)').get()
            if title == self.lastTitle:
                return
            item = ScrapyNewsItem()
            item['title'] = title
            item['description'] = description
            item['link'] = newsUrl
            item['pub_date'] = datatime
            universityItem = University(id=1)
            item['university'] = universityItem
            yield item

        next_page = response.css('li.next a::attr(href)').get()
        #if next_page is not None:
           # yield response.follow(next_page, callback=self.parse)



# scrapy crawl tsu_news

class TsuSpider(scrapy.Spider):
    name = "tsu_news"
    universityId = 2
    lastTitle = (NewsItem.objects.filter(university_id=universityId).order_by('-pub_date')[0]).title
    start_urls = [
        'http://en.tsu.ru/?page_38=1',
        #'http://en.tsu.ru/?page_38=669',
    ]

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    def parseNewsPage(self, response):

        title = response.css('div.news_name::text').get()
        description = str(response.css('div.preview_text ::text').get()).strip()
        if description == '':
            description = str(response.css('div.preview_text p::text').get()).strip()
        datatime = response.css('div.news-detail-date::text').get()
        newsUrl = response.request.url

        yield {
            'title': title,
            'description': description,
            'link': newsUrl,
            'pub_date': datatime,
            'university_id': '2',
        }

    def parse(self, response):
        for quote in response.css('div.news_item.col-xs-12.col-sm-6.col-lg-3 div.news_name'):
            newsURL = quote.css('a::attr(href)').get()

            # response.follow(newsURL, callback=self.parseNewsPage)
            yield scrapy.Request('http://en.tsu.ru{}'.format(newsURL), headers=self.headers,
                                 callback=self.parseNewsPage)
