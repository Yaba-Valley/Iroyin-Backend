import asyncio


class Scraper:
    def __init__(self, scraper_name):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Cookie': 'tnw_morph=973357127; tfv=2022-09-29T18:52:23.395+01:00; gdpr-auditId=fad5b09eed7c4dfb855caaaaa25eb995; __gads=ID=358254a7976f22ff:T=1664473946:S=ALNI_MZNOlKY6jdXhmMEFheTmuSSWNQRtg; __gpi=UID=00000af0d6b42650:T=1664473946:RT=1664473946:S=ALNI_MYHrIOXf1xBZo_gtbQmLFrsy_z5rQ; __hstc=111399067.cc4094bf9ee50368559c2ffc942bc67e.1664473954009.1664473954009.1664473954009.1; hubspotutk=cc4094bf9ee50368559c2ffc942bc67e; tlv=2022-09-29T18:56:02.713+01:00; _ga=GA1.1.1246751966.1664473946; _ga_1FX48DMMCB=GS1.1.1664473947.1.1.1664475231.0.0.0'
        }
        self.name = scraper_name

    # def run_test(self, test_case_object):
    #     news = []

    #     asyncio.run(fetch_news_async(self(), news))

    #     test_case_object.assertNotEqual(
    #         len(news), 0, "{0} does not return anything".format(self.name))
