import os
from threading import Thread
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from rest_api.grabber.grabber.spiders import CaltechSpider, TpuSpider, CambridgeSpider, HarvardSpider, TsuSpider, \
    ItmoSpider, NsuSpider, NusSpider, SpbuSpider, StanfordSpider

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
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        reactor.callWhenRunning(self.addCrawlers)
        self.runner.join()

    def run(self):
        reactor.run(installSignalHandlers=0)

    def addCrawlers(self):
        d = self.runner.crawl(TpuSpider)
        d = self.runner.crawl(CaltechSpider)
        d = self.runner.crawl(CambridgeSpider)
        d = self.runner.crawl(HarvardSpider)
        d = self.runner.crawl(ItmoSpider)
        d = self.runner.crawl(NsuSpider)
        d = self.runner.crawl(NusSpider)
        d = self.runner.crawl(SpbuSpider)
        d = self.runner.crawl(StanfordSpider)
        d = self.runner.crawl(TsuSpider)
