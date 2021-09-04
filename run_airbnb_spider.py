from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from airbnb.spiders.airbnb_spider import AirbnbSpider

def run(destinations_to_scrape=[], offset=100):
    settings = get_project_settings()

    if destinations_to_scrape == []:
        destinations = input("Enter comma seperated destinations to scrape:\n")
        _offset = int(input('Enter number of listings to scrape per destination \n'))
    else:
        destinations = destinations_to_scrape
        _offset = offset

    destinations = [dest.strip(' ') for dest in destinations.split(',')]
    process = CrawlerProcess(settings=settings)

    process.crawl(AirbnbSpider, destinations=destinations, offset=_offset)
    process.start()

if __name__ == '__main__':
    run()
