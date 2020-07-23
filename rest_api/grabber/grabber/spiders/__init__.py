import datetime
import re
import scrapy
from rest_api.grabber.grabber.items import ScrapyNewsItem
from rest_api.models import NewsItem, University

const_headers = {
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


# scrapy crawl caltech_news
class CaltechSpider(scrapy.Spider):
    name = "caltech_news"
    universityId = 6
    lastTitle = "--"

    start_urls = [
        'https://www.caltech.edu/about/news?&p=1',
    ]

    url = 'https://www.caltech.edu/about/news?&p={}'
    page = 1

    headers = const_headers

    def parse_news_page(self, response):
        title = response.css(
            'div.simple-news-header-block.mb-5.py-5 h1.simple-news-header-block__title.mb-3::text').get()
        if title is None or title == 'None' or title == '':
            title = response.css(
                'h1.news-hero-header-block__info__title::text').get()
        description = response.css('div.rich-text p::text').get()
        if description is None or description == 'None' or description == '':
            description = str(response.css('div.rich-text p span::text').get())
            if description is None or description == 'None' or description == '':
                description = str(response.css('div.video-block__info__caption.px-4::text').get())
                if description is None or description == 'None' or description == '':
                    description_array = response.css('div.rich-text div::text').getall()
                    description = ' '.join(str(d) for d in description_array)
        description = description.strip()
        regex = re.compile(r'[\n\r\t]|  +')
        description = (regex.sub("", description)).strip()
        datatime_ruw = response.css('div.publish-date-block__date::text').get().strip()  # 'July 16, 2020'
        datatime = str(datetime.datetime.strptime(datatime_ruw, '%B %d, %Y'))
        newsUrl = response.request.url
        full_text_array = response.css('div.rich-text *::text').getall()
        full_text = ' '.join(str(d).strip() for d in full_text_array)
        full_text = (regex.sub("", full_text))
        if len(description) < 100:
            description = description + ' ' + full_text[0:][:100]
        if description != "":
            item = ScrapyNewsItem()
            item['title'] = title.strip()
            item['description'] = description
            item['full_text'] = full_text
            item['link'] = newsUrl
            item['pub_date'] = datatime
            universityItem = University(id=self.universityId)
            item['university'] = universityItem
            yield item

    def parse(self, response):
        news_item = NewsItem.objects.filter(university_id=self.universityId).order_by('-pub_date')
        if news_item:
            self.lastTitle = (news_item[0]).title
        for quote in response.css('div.article-teaser__info'):
            title = quote.css('div.article-teaser__title a::text').get().strip()
            if title == self.lastTitle:
                exit(0)
            newsURL = quote.css('div.article-teaser__title a.article-teaser__link::attr(href)').get()
            if newsURL[0] == '/':
                yield scrapy.Request('https://www.caltech.edu{}'.format(newsURL), headers=self.headers,
                                     callback=self.parse_news_page)

        last_page = 'https://www.caltech.edu{}'.format(response.css(
            'a.news-article-list__paginator__link-box.news-article-list__paginator__last-page::attr(href)').get())
        self.page += 1
        next_page = self.url.format(self.page)

        if next_page != last_page:
            yield response.follow(next_page, callback=self.parse)


class CambridgeSpider(scrapy.Spider):
    name = "cambridge_news"
    universityId = 7
    lastTitle = "--"

    start_urls = [
        'https://www.cam.ac.uk/news?page=0',
    ]

    headers = const_headers

    def parse_news_page(self, response):
        title = str(response.css('h1.cam-sub-title::text').get()).strip()
        description_array = response.css(
            'div.field-name-field-content-summary div.field-items div.field-item.even *::text').getall()
        description = ' '.join(str(d).strip() for d in description_array)
        full_text_array = response.css('div.field-name-body div.field-items div.field-item.even *::text').getall()
        full_text = ' '.join(str(d).strip() for d in full_text_array)
        if full_text == '':
            full_text_array = response.css('div.field-name-body div.field-items div.field-item.even p *::text').getall()
            full_text = ' '.join(str(d).strip() for d in full_text_array)
        regex = re.compile(r'[\n\r\t]|  +')
        full_text = (regex.sub("", full_text))
        newsUrl = response.request.url
        datatime = '2000-01-01 01:01:01'
        datatime_ruw = str(response.css(
            'div.view-content div.views-row div.view-image-credit span::text').get()).strip()  # '05 June 2020'
        if datatime_ruw != 'None' and datatime_ruw != '' and datatime_ruw != None:
            datatime = str(datetime.datetime.strptime(datatime_ruw, '%d %b %Y'))
        if len(description) < 100:
            description = description + ' ' + full_text[0:][:100]
        if not (title == 'None' and description == ' ' and full_text == ''):
            item = ScrapyNewsItem()
            item['title'] = title.strip()
            item['description'] = description
            item['full_text'] = full_text
            item['link'] = newsUrl
            item['pub_date'] = datatime
            universityItem = University(id=self.universityId)
            item['university'] = universityItem
            yield item

    def parse(self, response):
        news_item = NewsItem.objects.filter(university_id=self.universityId).order_by('-pub_date')
        if news_item:
            self.lastTitle = (news_item[0]).title
        for quote in response.css('article.clearfix.cam-horizontal-teaser.cam-teaser'):
            title = str(quote.css('h3.cam-teaser-title a::text').get()).strip()
            if title == self.lastTitle:
                exit(0)
            newsUrl = quote.css('h3.cam-teaser-title a::attr(href)').get().strip()
            if newsUrl[1] != 's':
                yield scrapy.Request('https://www.cam.ac.uk{}'.format(newsUrl), headers=self.headers,
                                     callback=self.parse_news_page)

        next_page = response.css('li.pager-next.last a::attr(href)').get()
        if next_page is not None:
            yield response.follow('https://www.cam.ac.uk{}'.format(next_page), callback=self.parse)


# scrapy crawl harvard_news
class HarvardSpider(scrapy.Spider):
    name = "harvard_news"
    universityId = 4
    lastTitle = "--"
    start_urls = [
        'https://news.harvard.edu/gazette/section/news_plus',
    ]
    headers = const_headers

    def parse_news_page(self, response):
        title = response.css('div.article-titles__titles h1.article-titles__title::text').get()
        description_array = response.css('div.article-body.basic-text p::text').getall()
        description = (' '.join(str(d) for d in description_array))
        regex = re.compile(r'[\n\r\t]|  +')
        description = (regex.sub("", description)).strip()
        if description is None or description == 'None' or description == '':
            description_array = response.css('div.article-body.basic-text p span::text').getall()
            description = (' '.join(str(d) for d in description_array))
            description = (regex.sub("", description)).strip()
        full_text_array = response.css('div.article-body.basic-text *::text').getall()
        full_text = (' '.join(str(d).strip() for d in full_text_array))
        full_text = (regex.sub("", full_text))
        datatime_ruw = response.css(
            'p.article-posted-on time.timestamp::attr(datetime)').get().strip()  # 2020-06-04T08:39:24-04:00
        datatime = str(datetime.datetime.strptime(datatime_ruw, '%Y-%m-%dT%H:%M:%S%z'))[0:][:19]
        newsUrl = response.request.url
        if len(description) < 100:
            description = description + ' ' + full_text[0:][:100]
        item = ScrapyNewsItem()
        item['title'] = title.strip()
        item['description'] = description
        item['full_text'] = full_text
        item['link'] = newsUrl
        item['pub_date'] = datatime
        universityItem = University(id=self.universityId)
        item['university'] = universityItem
        yield item

    def parse(self, response):
        news_item = NewsItem.objects.filter(university_id=self.universityId).order_by('-pub_date')
        if news_item:
            self.lastTitle = (news_item[0]).title
        for quote in response.css('div.tz-article-image__meta'):
            title = quote.css('h2.tz-article-image__title a::text').get().strip()
            if title == self.lastTitle:
                exit(0)
            newsURL = quote.css('h2.tz-article-image__title a::attr(href)').get()

            yield scrapy.Request(newsURL, headers=self.headers,
                                 callback=self.parse_news_page)

        next_page = response.css('div.nav-previous a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


class ItmoSpider(scrapy.Spider):
    name = "itmo_news"
    universityId = 8
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

        'https://news.itmo.ru/en/university_live/ratings/',
        'https://news.itmo.ru/en/university_live/achievements/',
        'https://news.itmo.ru/en/university_live/leisure/',
        'https://news.itmo.ru/en/university_live/ads/',
        'https://news.itmo.ru/en/university_live/social_activity/',

    ]

    headers = const_headers

    def parse_news_page(self, response, item):
        # title = response.css('div.article article h1::text').get()
        description_array = response.css('div.article article strong::text').getall()
        description = ' '.join(str(d) for d in description_array)
        regex = re.compile(r'[\n\r\t]|  +')
        description = (regex.sub("", description))
        full_text_array = response.css('div.post-content *::text').getall()
        full_text = (' '.join(str(d).strip() for d in full_text_array))
        full_text = (regex.sub("", full_text))
        datatime_ruw = response.css(
            'div.news-info-wrapper time::attr(datetime)').get().strip()  # 2020-06-04T08:39:24-04:00
        datatime = str(datetime.datetime.strptime(datatime_ruw, '%Y-%m-%dT%H:%M:%S%z'))[0:][:19]
        newsUrl = response.request.url
        if len(description) < 100:
            description = description + ' ' + full_text[0:][:100]
        item['title'] = item['title']
        item['description'] = description
        item['full_text'] = full_text
        item['link'] = newsUrl
        item['pub_date'] = datatime
        universityItem = University(id=self.universityId)
        item['university'] = universityItem
        yield item

    def parse(self, response):
        news_items = NewsItem.objects.filter(university_id=self.universityId).order_by('-pub_date')
        lastTitles = [None] * 252
        if news_items:
            l = len(news_items)
            if l > 0:
                if l > 250:
                    l = 250
                news = news_items[0:][:l]
                for i in range(0, l):
                    lastTitles[i] = news[i].title
        for quote in response.css('ul.triplet li'):
            title = quote.css('h4 a::text').get().strip()
            if title in lastTitles:
                exit(0)
            newsURL = quote.css('h4 a::attr(href)').get()
            item = ScrapyNewsItem()
            item['title'] = title.strip()
            yield scrapy.Request('https://news.itmo.ru{}'.format(newsURL), headers=self.headers,
                                 callback=self.parse_news_page, cb_kwargs=dict(item=item))

        next_page = response.css('ul.pagination-custom.row.flex-center div.col-1 a::attr(href)').getall()
        if next_page:
            if len(next_page) > 1:
                yield response.follow(next_page, callback=self.parse)


# scrapy crawl nsu_news
class NsuSpider(scrapy.Spider):
    name = "nsu_news"
    universityId = 3
    lastTitle = "--"
    start_urls = [
        'https://english.nsu.ru/news-events/news/',
    ]

    url = 'https://english.nsu.ru/news-events/news/?PAGEN_1={}'
    page_num = 1

    headers = const_headers

    def parse_news_page(self, response):
        title = str(response.css('div.col-lg-9 h1::text').get()).strip()
        description = str(response.css('div.detail_text p::text').get()).strip()
        full_text_array = response.css('div.detail_text *::text').getall()
        full_text = (' '.join(str(d).strip() for d in full_text_array))
        regex = re.compile(r'[\n\r\t]|  +')
        full_text = (regex.sub("", full_text))
        if description == '':
            description = full_text[0:][:100]
        datatime_ruw = response.css('div.news-date-time.nowrap::text').get().strip()  # '21.03.2020'
        datatime = str(datetime.datetime.strptime(datatime_ruw, '%d.%m.%Y'))
        newsUrl = response.request.url
        if len(description) < 100:
            description = description + ' ' + full_text[0:][:100]
        item = ScrapyNewsItem()
        item['title'] = title.strip()
        item['description'] = description
        item['full_text'] = full_text
        item['link'] = newsUrl
        item['pub_date'] = datatime
        universityItem = University(id=self.universityId)
        item['university'] = universityItem
        yield item

    def parse(self, response):
        news_item = NewsItem.objects.filter(university_id=self.universityId).order_by('-pub_date')
        if news_item:
            self.lastTitle = (news_item[0]).title
        for quote in response.css('div.news-card'):
            title = str(quote.css('a.name::text').get()).strip()
            if title == self.lastTitle:
                exit(0)
            newsUrl = 'https://english.nsu.ru{}'.format(quote.css('a.name::attr(href)').get())
            yield scrapy.Request(newsUrl, headers=self.headers,
                                 callback=self.parse_news_page)
        next_page = response.css('a.moreNewsList.loadMoreButton').get()
        self.page_num += 1
        if next_page is not None:
            yield response.follow(self.url.format(self.page_num), callback=self.parse)


# scrapy crawl nus_news
class NusSpider(scrapy.Spider):
    name = "nus_news"
    universityId = 9
    lastTitle = "--"

    start_urls = [
        'https://news.nus.edu.sg/highlights?field_categories_target_id=All&page=0',
    ]

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
    }

    headers = const_headers

    def parse_news_page(self, response):
        title = str(response.css('h1.page-header span::text').get()).strip()
        regex = re.compile(r'[\n\r\t]|  +')
        description = (
            regex.sub("", str(response.css('div.field.field--name-field-caption-format.field--type-text-long.'
                                           'field--label-hidden.landingimg-caption.field--item  p::text').get())))
        full_text_array = response.css('div.content *::text').getall()
        full_text = (' '.join(str(d).strip() for d in full_text_array))
        full_text = (regex.sub("", full_text))
        datatime = '2000-01-01 01:01:01'
        array = response.css('article.highlights.full.clearfix *::text').getall()
        array_press_releases = response.css('article.press-releases-1.full.clearfix *::text').getall()
        if array:
            datatime_ruw = str(array[1]).strip()  # '03 July 2020'
            if len(datatime_ruw) > 3:
                datatime_ruw = datatime_ruw[0:][:-3]
                datatime = str(datetime.datetime.strptime(datatime_ruw, '%d %B %Y'))
        if datatime == '2000-01-01 01:01:01':
            if array_press_releases:
                datatime_ruw = str(array_press_releases[1]).strip()  # '03 July 2020'
                if len(datatime_ruw) > 3:
                    datatime_ruw = datatime_ruw[0:][:-3]
                    datatime = str(datetime.datetime.strptime(datatime_ruw, '%d %B %Y'))
        newsUrl = response.request.url
        if len(description) < 100:
            description = description + ' ' + full_text[0:][:100]
        if not (title == 'None' and description == 'None ' and full_text == ''):
            item = ScrapyNewsItem()
            item['title'] = title.strip()
            item['description'] = description
            item['full_text'] = full_text
            item['link'] = newsUrl
            item['pub_date'] = datatime
            universityItem = University(id=self.universityId)
            item['university'] = universityItem
            yield item

    def parse(self, response):
        news_item = NewsItem.objects.filter(university_id=self.universityId).order_by('-pub_date')
        if news_item:
            self.lastTitle = (news_item[0]).title
        for quote in response.css('div.col-lg-6.col-md-6.col-sm-6.col-xs-12.highlight-top'):
            title = str(quote.css('h2.highlight-title a::text').get()).strip()
            if title == self.lastTitle:
                exit(0)
            newsUrl = quote.css('h2.highlight-title a::attr(href)').get()
            if newsUrl[0] == 'h':
                yield scrapy.Request(newsUrl, headers=self.headers,
                                     callback=self.parse_news_page)
            else:
                yield scrapy.Request('https://news.nus.edu.sg{}'.format(newsUrl), headers=self.headers,
                                     callback=self.parse_news_page)

        next_page = response.css('li.pager__item--next a::attr(href)').get()
        if next_page is not None:
            yield response.follow('https://news.nus.edu.sg/highlights{}'.format(next_page), callback=self.parse)


# scrapy crawl spbu_news
class SpbuSpider(scrapy.Spider):
    name = "spbu_news"
    universityId = 10
    lastTitle = "--"

    start_urls = [
        'https://english.spbu.ru/news',
    ]

    headers = const_headers

    def parse_news_page(self, response):
        title = response.css('div.page-header h2::text').get().strip()
        full_text_array = response.css('div[itemprop = "articleBody"] *::text').getall()
        full_text = (' '.join(str(d).strip() for d in full_text_array))
        regex = re.compile(r'[\n\r\t]|  +')
        full_text = (regex.sub("", full_text))
        datatime_ruw = response.css(
            'dd.published time::attr(datetime)').get().strip()  # '2020-07-15T16:30:00+03:00'
        datatime = str(datetime.datetime.strptime(datatime_ruw, '%Y-%m-%dT%H:%M:%S%z'))[0:][:19]
        newsUrl = response.request.url
        description = full_text[0:][:100]
        item = ScrapyNewsItem()
        item['title'] = title.strip()
        item['description'] = description
        item['full_text'] = full_text
        item['link'] = newsUrl
        item['pub_date'] = datatime
        universityItem = University(id=self.universityId)
        item['university'] = universityItem
        yield item

    def parse(self, response):
        news_item = NewsItem.objects.filter(university_id=self.universityId).order_by('-pub_date')
        if news_item:
            self.lastTitle = (news_item[0]).title
        quots0 = response.css('tr.cat-list-row0')
        quots1 = response.css('tr.cat-list-row1')
        qupts = quots0 + quots1
        for quote in qupts:
            title = quote.css('td.list-title a::text').get().strip()
            if title == self.lastTitle:
                exit(0)
            newsURL = quote.css('td.list-title a::attr(href)').get()
            yield scrapy.Request('https://english.spbu.ru{}'.format(newsURL), headers=self.headers,
                                 callback=self.parse_news_page)

        next_page = response.css('li.pagination-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow('https://english.spbu.ru{}'.format(next_page), callback=self.parse)


# scrapy crawl stanford_news
class StanfordSpider(scrapy.Spider):
    name = "stanford_news"
    universityId = 5
    lastTitles = ['', '', '', '', '', '']

    start_urls = [
        'http://med.stanford.edu/news/all-news.html?main_news_builder_start=0',
    ]

    headers = const_headers

    def parse_news_page(self, response, item):
        # title = str(response.css('div.news-title hgroup.section-header h1::text').get()).strip()
        description = str(response.css('p.news-excerpt::text').get()).strip()
        full_text_array = response.css('div.main.parsys div div *::text').getall()
        full_text = (' '.join(str(d).strip() for d in full_text_array))
        regex = re.compile(r'[\n\r\t]|  +')
        full_text = (regex.sub("", full_text))
        date_day = str(response.css('span.publication-day::text').get()).strip()
        date_year = str(response.css('span.publication-year::text').get()).strip()
        datatime_ruw = date_day + ' ' + date_year  # Jul 14 2020
        datatime = '2000-01-01 00:00:00'
        if not (date_day == date_year == 'None'):
            datatime = str(datetime.datetime.strptime(datatime_ruw, '%b %d %Y'))
        newsUrl = response.request.url
        if len(description) < 100:
            description = description + ' ' + full_text[0:][:100]
        if not (description == 'None ' and full_text == '' and datatime == '2000-01-01 00:00:00'):
            item['title'] = item['title']
            item['description'] = description
            item['full_text'] = full_text
            item['link'] = newsUrl
            item['pub_date'] = datatime
            universityItem = University(id=self.universityId)
            item['university'] = universityItem
            yield item

    def parse(self, response):
        news_items = NewsItem.objects.filter(university_id=self.universityId).order_by('-pub_date')
        self.lastTitles = [None] * 31
        if news_items:
            l = len(news_items)
            if l > 0:
                if l > 30:
                    l = 30
                news = news_items[0:][:l]
                for i in range(0, l):
                    self.lastTitles[i] = news[i].title
        for quote in response.css('li.newsfeed-item.row'):
            checkdescription = quote.css('p.newsfeed-item-excerpt::text').get()
            if checkdescription != 'None' and checkdescription != None and checkdescription != '':
                title = str(quote.css('h3.newsfeed-item-title::text').get()).strip()
                if title in self.lastTitles:
                    exit(0)
                newsUrl = quote.css('div.col-xs-9.col-sm-8 a::attr(href)').get()
                if newsUrl == 'None' or newsUrl == None:
                    newsUrl = quote.css('div.col-sm-12 a::attr(href)').get()
                newsUrl = newsUrl.strip()
                newsUrl = 'http://med.stanford.edu{}'.format(newsUrl)
                item = ScrapyNewsItem()
                item['title'] = title.strip()
                yield scrapy.Request(newsUrl, headers=self.headers, callback=self.parse_news_page,
                                     cb_kwargs=dict(item=item))

        next_page = response.css('div.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow('http://med.stanford.edu{}'.format(next_page), callback=self.parse)


# scrapy crawl tpu_news
class TpuSpider(scrapy.Spider):
    name = "tpu_news"
    universityId = 1
    lastTitle = "--"

    start_urls = [
        'https://news.tpu.ru/en/news/',
    ]

    headers = const_headers

    def parse_news_page(self, response):
        title = str(response.css('h1.title::attr(title)').get()).strip()
        regex = re.compile(r'[\n\r\t]|  +')
        description = (regex.sub("", str(response.css('div.description p span strong::text').get()))).strip()
        full_text_array = response.css('div.description *::text').getall()
        full_text = (' '.join(str(d).strip() for d in full_text_array))
        full_text = (regex.sub("", full_text))
        if description is None or description == 'None' or description == '':
            description = full_text[0:][:100]
        datatime = response.css('div.date time::attr(datetime)').get()  # '2020-05-29 12:31:00'
        newsUrl = response.request.url
        if len(description) < 100:
            description = description + ' ' + full_text[0:][:100]
        item = ScrapyNewsItem()
        item['title'] = title.strip()
        item['description'] = description
        item['full_text'] = full_text
        item['link'] = newsUrl
        item['pub_date'] = datatime
        universityItem = University(id=self.universityId)
        item['university'] = universityItem
        yield item

    def parse(self, response):
        news_item = NewsItem.objects.filter(university_id=self.universityId).order_by('-pub_date')
        if news_item:
            self.lastTitle = (news_item[0]).title
        for quote in response.css('div.row div.col-lg-9.item-body'):
            title = str(quote.css('h3.title::attr(title)').get()).strip()
            if title == self.lastTitle:
                exit(0)
            newsUrl = quote.css('a::attr(href)').get()
            yield scrapy.Request(newsUrl, headers=self.headers,
                                 callback=self.parse_news_page)
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


# scrapy crawl tsu_news
class TsuSpider(scrapy.Spider):
    name = "tsu_news"
    universityId = 2
    lastTitle = "--"

    start_urls = [
        # 'http://en.tsu.ru/?page_38=1',
        'http://en.tsu.ru/?page_38=669',
    ]

    headers = const_headers

    def parse_news_page(self, response):
        title = response.css('div.news_name::text').get()
        description = str(response.css('div.preview_text ::text').get()).strip()
        if description == '':
            description = str(response.css('div.preview_text p::text').get()).strip()
        full_text_array = response.css('div.preview_text *::text').getall()
        full_text = (' '.join(str(d).strip() for d in full_text_array))
        regex = re.compile(r'[\n\r\t]|  +')
        full_text = (regex.sub("", full_text))
        if description is None or description == 'None' or description == '':
            description = full_text[0:][:100]
        datatime_ruw = response.css('div.news-detail-date::text').get().strip()  # '08.07.2020'
        datatime = str(datetime.datetime.strptime(datatime_ruw, '%d.%m.%Y'))
        newsUrl = response.request.url
        if len(description) < 100:
            description = description + ' ' + full_text[0:][:100]
        item = ScrapyNewsItem()
        item['title'] = title.strip()
        item['description'] = description
        item['full_text'] = full_text
        item['link'] = newsUrl
        item['pub_date'] = datatime
        universityItem = University(id=self.universityId)
        item['university'] = universityItem
        yield item

    def parse(self, response):
        news_item = NewsItem.objects.filter(university_id=self.universityId).order_by('-pub_date')
        if news_item:
            self.lastTitle = (news_item[0]).title
        for quote in response.css('div.news_item.col-xs-12.col-sm-6.col-lg-3 div.news_name'):
            title = quote.css('div.news_name a::text').get()
            if title is None or title == 'None' or title == '':
                title = quote.css('div.news_name a p::text').get()
            title = title.strip()
            if title == self.lastTitle:
                exit(0)
            newsURL = quote.css('a::attr(href)').get()
            yield scrapy.Request('http://en.tsu.ru{}'.format(newsURL), headers=self.headers,
                                 callback=self.parse_news_page)
