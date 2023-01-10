import asyncio


class Scraper:
    def __init__(self, scraper_name):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        self.name = scraper_name

    # def run_test(self, test_case_object):
    #     news = []

    #     asyncio.run(fetch_news_async(self(), news))

    #     test_case_object.assertNotEqual(
    #         len(news), 0, "{0} does not return anything".format(self.name))
