from typing import Iterable, List
from datetime import datetime
import re, subprocess

from scrapy import Spider, Request
from scrapy.cmdline import execute
from scrapy.linkextractors import LinkExtractor
from scrapy.responsetypes import Response
from scrapy.crawler import CrawlerProcess
from scrapy.link import Link

try:
    from exceptions import NoDomainException
except ImportError:
    from .exceptions import NoDomainException

from sitemap.settings import logger


class SiteMapSpider(Spider):
    """
    Main spider for grabbing resources
    """
    name = "SiteMap"
    css_files = []
    js_files = []
    links = []
    domain = None

    def __init__(self, *args, **kwargs):
        self.start_urls = kwargs.get('start_urls', [])
        self.first_page_only = kwargs.get('first_page', True)

        self.domain = self.get_domain(**kwargs)
        super(SiteMapSpider, self).__init__(*args, **kwargs)

    def get_domain(self, **kwargs) -> str:
        """
        Get domain from kwargs or from started_urls
        :param kwargs:
        :return:
        """
        if self.domain:
            return self.domain

        keys = kwargs.keys()
        if 'domain' in keys:
            return kwargs['domain']

        if len(self.start_urls) > 0:
            match = re.search(r"https*://(?:www.)*([\w\d]+\.[\w\d]+)/*", kwargs['start_urls'][0])
            if match:
                return match.group(1)

        raise NoDomainException()

    def get_css_files(self, response: Response) -> Iterable:
        """
        Returns the list of css files of current page
        :param response:
        :return:
        """
        return [link.attrib['href'] for link in response.xpath("//link[@rel='stylesheet']")]

    def get_js_files(self, response: Response) -> Iterable:
        """
        Returns list of js files of current page
        :param response:
        :return:
        """
        return [
            script.attrib['src'] for script in response.xpath("//script") if script.attrib.get('src')
        ]

    def parse(self, response: Response, **kwargs):
        """
        Parse response from site
        :param response:
        :param kwargs:
        :return:
        """
        self.logger.debug("Parse")

        link_extractor = LinkExtractor(allow=rf"https*://(www\.)*{self.domain}/*")
        links: List[Link] = link_extractor.extract_links(response)

        css = self.get_css_files(response)
        js = self.get_js_files(response)

        if response.url not in self.links:
            self.links.append(response.url)
            yield {
                'page': response.url,
                'links': [link.url for link in links],
                'css': css,
                'js': js
            }

        if not self.first_page_only:
            for link in links:
                if re.sub(r"#[\w\d\-]+", "", link.url) not in self.links:
                    yield Request(link.url, callback=self.parse)


def run_spider(url: str, first_page: bool = True, filename: str = "") -> str:
    """
    Run  Scrapy spider for given url
    :param first_page: If scrap only first page
    :param url:
    :param filename:
    :return:
    """
    if not filename:
        filename = f"{datetime.timestamp(datetime.now())}.json"

    subprocess.run(
        ["scrapy", "runspider", "-o", filename, "-a", f"start_urls=[{url}]", f"first_page={first_page}", "spider.spider.py", ]
    )
    return filename
