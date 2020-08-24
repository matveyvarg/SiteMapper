from sitemap.spider.crawler import Crawler, SeleniumCrawler

URL = "http://quotes.toscrape.com"


class TestCrawler:
    """
    Testing crawler
    """

    # Use site from 'Scrapy' example
    crawler = Crawler("http://quotes.toscrape.com", True)

    def test_crawler_get_domain(self):
        """
        Should return "quotes.toscrape.com"
        :return:
        """
        assert self.crawler.domain == "quotes.toscrape.com"

    def test_crawler_crawl(self):
        """
        Test results of crawler
        :return:
        """
        self.crawler.crawl(self.crawler.start_url)
        assert len(self.crawler.result) == 1
        assert len(self.crawler.result[0]['css']) == 2
        assert len(self.crawler.result[0]['links']) == 53
        assert len(self.crawler.result[0]['js']) == 0


class TestSeleniumCrawler:

    # Page with dynamic content loaded
    crawler = SeleniumCrawler("https://vanhack.com", True)

    def test_crawler_get_domain(self):
        """
        Should return "quotes.toscrape.com"
        :return:
        """
        assert self.crawler.domain == "vanhack.com"

    def test_crawler_crawl(self):
        """
        Test results of crawler
        :return:
        """
        self.crawler.crawl(self.crawler.start_url)
        assert len(self.crawler.result) == 1
        assert len(self.crawler.result[0]['css']) == 5
        assert len(self.crawler.result[0]['links']) == 10
        assert len(self.crawler.result[0]['js']) == 23


class TestMultiplePageParsing:
    """
    Test crawler for multiple pages
    """
    crawler = Crawler("https://devhints.io/xpath", False)

    def test_crawler_get_domain(self):
        """
        Should return "quotes.toscrape.com"
        :return:
        """
        assert self.crawler.domain == "devhints.io"

    def test_crawler_crawl(self):
        """
        Test results of crawler
        :return:
        """
        self.crawler.crawl(self.crawler.start_url)
        assert len(self.crawler.result) > 1
