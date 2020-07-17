import os
from threading import Thread

from django.template.backends import django
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

from multiprocessing.context import Process

from twisted.internet import reactor
from twisted.internet.error import ReactorAlreadyRunning
from twisted.internet.selectreactor import SelectReactor

from rest_api.grabber.grabber.spiders import CaltechSpider, TpuSpider

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aggregator.settings")
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import sys
import os
from scrapy.utils.project import get_project_settings


from scrapy import signals

from scrapy.crawler import Crawler

# def run_spider(spider):
#     configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
#
#     settings = Settings()
#     os.environ['SCRAPY_SETTINGS_MODULE'] = 'rest_api.grabber.grabber.settings'
#     settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
#     settings.setmodule(settings_module_path, priority='project')
#     def f(q):
#         try:
#             runner = crawler.CrawlerRunner()
#             deferred = runner.crawl(spider)
#             deferred.addBoth(lambda _: reactor.stop())
#             reactor.run()
#             q.put(None)
#         except Exception as e:
#             q.put(e)
#
#     q = Queue()
#     p = Process(target=f, args=(q,))
#     p.start()
#     result = q.get()
#     p.join()


# def crawl():
#     configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
#
#     settings = Settings()
#     os.environ['SCRAPY_SETTINGS_MODULE'] = 'rest_api.grabber.grabber.settings'
#     settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
#     settings.setmodule(settings_module_path, priority='project')
#
#     crawler = CrawlerProcess(settings)
#     crawler.crawl(TpuSpider)
#     #crawler.crawl(CaltechSpider)
#     crawler.start()



# def run_crawl():
#     """
#     Run a spider within Twisted. Once it completes,
#     wait 5 seconds and run another spider.
#     """
#     runner = CrawlerRunner({
#         'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
#         })
#     deferred = runner.crawl(TpuSpider)
#     # you can use reactor.callLater or task.deferLater to schedule a function
#     deferred.addCallback(reactor.callLater, 5, run_crawl)
#     return deferred

# class CrawlRunner:
#
#     def __init__(self):
#         self.running_crawlers = []
#
#     def spider_closing(self, spider):
#
#         self.running_crawlers.remove(spider)
#         if not self.running_crawlers:
#             reactor.stop()
#
#     def run(self):
#
#         #sys.path.append(os.path.join(os.path.curdir, "crawl/somesite"))
#
#
#         settings = Settings()
#         os.environ['SCRAPY_SETTINGS_MODULE'] = 'rest_api.grabber.grabber.settings'
#         settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
#         settings.setmodule(settings_module_path, priority='project')
#
#         to_crawl = [TpuSpider]
#
#         for spider in to_crawl:
#
#             crawler = Crawler(settings)
#             crawler_obj = spider()
#             self.running_crawlers.append(crawler_obj)
#
#             crawler.signals.connect(self.spider_closing, signal=signals.spider_closed)
#             crawler.configure()
#             crawler.crawl(crawler_obj)
#             crawler.start()
#
#         reactor.run()

# def main():
#     configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
#     settings = Settings()
#     os.environ['SCRAPY_SETTINGS_MODULE'] = 'rest_api.grabber.grabber.settings'
#     settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
#     settings.setmodule(settings_module_path, priority='project')
#     runner = CrawlerRunner(settings)
#
#     @defer.inlineCallbacks
#     def crawl():
#         yield runner.crawl(TpuSpider)
#         # yield runner.crawl(MySpider2)
#         #reactor.stop()
#
#     crawl()
#     reactor.run()

    # cr = CrawlRunner()
    # cr.run()

    # process = Process(target=crawl)
    # process.start()
    # process.join()

    # run_spider(TpuSpider)

    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    # settings = Settings()
    # os.environ['SCRAPY_SETTINGS_MODULE'] = 'rest_api.grabber.grabber.settings'
    # settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    # settings.setmodule(settings_module_path, priority='project')
    # runner = CrawlerRunner(settings)
    # #d = runner.crawl(CaltechSpider)
    # d = runner.crawl(TpuSpider)
    # d = runner.join()
    # d.addBoth(lambda _: reactor.stop())
    # try:
    #     reactor.run()  # the script will block here until the crawling is finished
    # except ReactorAlreadyRunning:
    #     pass





# def runGrabbers():
#     # import django
#     #
#     # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregator.settings')
#     # os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
#     # django.setup()
#     main()
#
# if __name__ == '__main__':
#     main()

class RunGrabber:
    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'rest_api.grabber.grabber.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')
    runner = CrawlerRunner(settings)

    def __init__(self):
        thread = Thread(target=self.run)
        thread.start()

    def runGrabbers(self):

        #d = runner.crawl(CaltechSpider)
        #reactor.callWhenRunning(self.runner.crawl(TpuSpider))

        # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        # d = self.runner.crawl(TpuSpider)

        #d.addBoth(lambda _: reactor.stop())

        # settings = Settings()
        # os.environ['SCRAPY_SETTINGS_MODULE'] = 'rest_api.grabber.grabber.settings'
        # settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        # settings.setmodule(settings_module_path, priority='project')
        # runner = CrawlerRunner(settings)

        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        reactor.callWhenRunning(self.addCrawlers)
        self.runner.join()
        # d = runner.crawl(TpuSpider)
        # d.addBoth(lambda _: reactor.stop())




        # if(reactor.running == False):
        #     reactor.run(installSignalHandlers=0)

        # reactor.run(installSignalHandlers=0)
        #d = self.runner.join()
        #d.addBoth(lambda _: reactor.stop())

    def run(self):
        reactor.run(installSignalHandlers=0)

    def addCrawlers(self):
        d = self.runner.crawl(TpuSpider)
        # reactor.run(installSignalHandlers=0)
        # d.addBoth(lambda _: reactor.stop())