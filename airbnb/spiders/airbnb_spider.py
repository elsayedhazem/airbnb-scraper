import scrapy
import datetime
import sys
sys.path.append('..')
from airbnb.items import Listing


class AirbnbSpider(scrapy.Spider):
    name = "AirbnbSpider"
    counter = 0
    custom_settings = {
        'ITEM_PIPELINES': {
            'airbnb.pipelines.CsvExportPipeline': 300,
            'airbnb.pipelines.JsonExportPipeline': 500,
            }
    }

    def __init__(self, destinations=['doha'], adults=0, children=0, offset=100):
        super(AirbnbSpider, self).__init__()
        if type(destinations) is list:
            self.destinations = [destination.capitalize() for destination in destinations]
        else:
            self.destinations = [dest.strip(' ').capitalize() for dest in destinations.split(',')]
        self.adults = adults
        self.offset = int(offset)
        self.children = children
        self.start_urls = [self.get_url(destination.lower(), self.adults, self.children) for destination in self.destinations]


    extract_next_page = lambda self, response: response.xpath('//a[@class="_1li8g8e"][@aria-label="Next"]/@href').get()
    extract_results_from_response = lambda self, response: response.css("div._8ssblpx")
    extract_title = lambda self, selector: selector.css("div._167qordg::text").get()
    extract_rating = lambda self, selector: selector.css("div._vaj62s span._10fy1f8::text").get()
    extract_description = lambda self, selector: selector.css("div._kqh46o::text").getall()
    extract_price_per_night = lambda self, selector: selector.css("div._l2ulkt8 span._1p7iugi::text").get()
    extract_link = lambda self, selector: selector.css("a::attr(href)").get()


    def get_url(self, destination='doha', adults=0 , children=0):
        """Get Airbnb search url with given query parameters"""

        optional_params = {
        'adults':str(adults) if adults > 0 else '',
        'children':str(children) if children > 0 else ''
        }
        params = [f"&{k}={v}" for k,v in optional_params.items() if v != '']
        url = f"https://www.airbnb.com/s/{destination}/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=search_query"
        return url + ''.join(params)


    def parse(self, response):
        selectors = self.extract_results_from_response(response)
        current_destination = response.url.split('/')[4].capitalize()
        if len(selectors) is not 0:
            selectors = self.extract_results_from_response(response)
            titles = [self.extract_title(x) for x in selectors]
            guests = [self.extract_description(x)[0] for x in selectors]
            features = [' · '.join(self.extract_description(x)[1:]) for x in selectors]
            prices_per_night = [self.extract_price_per_night(x) for x in selectors]
            ratings = [self.extract_rating(x) for x in selectors]
            links = [("https://www.airbnb.com" + self.extract_link(x)) if self.extract_link(x) is not None else '' for x in selectors]
            next_page = self.extract_next_page(response)

            for i in range(len(selectors)):
                if self.counter < self.offset:
                    listing = Listing()
                    listing['Title'] = titles[i]
                    listing['Guests'] = guests[i]
                    listing['Features'] = '' if features[i] is None else features[i].replace('Â', '')
                    listing['Price'] = '' if prices_per_night[i] is None else prices_per_night[i].replace('Â', '')
                    listing['Rating'] = 0 if ratings[i] is None else float(ratings[i])
                    listing['Link'] = links[i]
                    listing['Destination'] = current_destination
                    yield listing
                    self.counter +=1
                else:
                    next_page = None
                    break


            if next_page is not None:
                yield response.follow(next_page, self.parse)

        else:
            self.logger.info('Could not get Airbnb Listings for given destination "%s". Try entering a more accurate string' % current_destination)
            yield None
