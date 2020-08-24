import re
import platform
import os
import time
from typing import Iterable

from requests import Session
from requests.status_codes import codes

from bs4 import BeautifulSoup

from selenium import webdriver

from sitemap.settings import logger, BASE_DIR
from sitemap.spider.exceptions import NoDomainException, GettingPageException


class BaseCrawler:
    """
    Base class for Selenium and Default Crawler
    """
    __slots__ = [
        'start_url',
        'first_page_only',
        'domain',
        'raise_errors',
        'filter_regex',
        'result',
        'visited_links',
        'schema'
    ]

    def crawl(self, url: str):
        """
        Abstract method, should be overrided
        :param url: Url to crawl
        :return:
        """
        raise NotImplemented

    def __init__(self, start_url: str = None, first_page_only: bool = True, **kwargs):
        """
        Constructor
        :param start_url:
        :param first_page_only:
        """
        self.start_url = start_url
        self.first_page_only = first_page_only
        self.domain, self.schema = self._get_domain_and_schema(**kwargs)
        self.raise_errors = kwargs.get('raise_errors', True)
        self.filter_regex = self.compile_regex()

        self.result = []
        self.visited_links = []

    def _get_domain_and_schema(self, **kwargs) -> tuple:
        """
        Get domain from kwargs or from started_urls
        :param kwargs:
        :return:
        """
        if getattr(self, 'domain', None):
            return self.domain

        keys = kwargs.keys()

        if 'domain' in keys:
            return kwargs['domain']

        if self.start_url:
            print(self.start_url)
            match = re.search(r"(https*)://(?:www.)*([\w\d.\-]+)/*", self.start_url)
            print(match)
            if match:
                return match.group(2), match.group(1)

        raise NoDomainException()

    def compile_regex(self):
        """
        Compile regex for filtering out links
        :return:
        """
        return re.compile(rf"(?:https*://(?:www.)*(?:{self.domain}))*/[\w\d\-/]*")

    def parse(self, body: str):
        """
        Parse body of response with BeautifulSoap
        :param body:
        :return:
        """
        tree = BeautifulSoup(body)
        links = self.get_links(tree.find_all("a"))
        css = self.get_css_files(tree)
        js = self.get_js_files(tree)

        return {
            'links': links,
            'css': css,
            'js': js
        }

    def get_css_files(self, tree: BeautifulSoup) -> Iterable:
        """
        Returns the list of css files of current page
        :param tree:
        :return:
        """
        return [
            link['href'] for link in tree.find_all(
                lambda tag: tag.name == "link" and tag.has_attr('href') and 'stylesheet' in tag.attrs.get('rel')
            )
        ]

    def get_js_files(self, tree: BeautifulSoup) -> Iterable:
        """
        Returns list of js files of current page
        :param tree:
        :return:
        """
        return [
            script['src'] for script in tree.find_all("script") if script.attrs.get('src')
        ]

    def get_links(self, links: Iterable):
        """
        Filter out links to other domains
        :param links:
        :return:
        """
        def add_domain(link: str) -> str:
            if not link.startswith('http'):
                return f"{self.schema}://{self.domain}{link}" if link.startswith('/') else f"{self.schema}://{self.domain}/{link}"
            return link

        return list(map(add_domain, [link['href'] for link in links if self.filter_regex.match(link.attrs.get('href', ''))]))


class Crawler(BaseCrawler):
    """
    Simple Crawler class
    Crawl with requests lib
    """

    session = Session()

    def crawl(self, url: str):
        """
        get page and parse it
        :param url:
        :return:
        """
        response = self.session.get(url)
        logger.debug(f"RESPONSE:<{response.status_code}>{url} ")
        if response.status_code != codes.ok and (not self.visited_links or self.raise_errors):
            raise GettingPageException(f"Page status: {response.status_code}")

        self.visited_links.append(url)

        data = self.parse(response.text)
        self.result.append({**data, 'page': url})

        # Return
        if not self.first_page_only:
            for link in data['links']:
                time.sleep(2)
                self.crawl(link)

    def run_crawler(self) -> list:
        """
        Start crawling pages
        :return:
        """
        self.crawl(self.start_url)
        return self.result


class SeleniumCrawler(BaseCrawler):
    """
    Crawler which use selenium and chromedriver for crawling
    """

    def compile_regex(self):
        return re.compile(rf"(?:https*://(?:www.)*(?:{self.domain}))*[/#]+[\w\d\-/]*")

    def _instantiate_webdriver(self):
        """
        Create new instance of Chrome webdriver for parsing spa
        :return:
        """
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        system = platform.system()

        if system == 'Windows':
            filename = 'chromedriver.exe'
        elif system == 'Darwin':
            filename = 'chromedriver-darwin'
        else:
            filename = 'chromedriver'
        chromedriver_path = os.path.join(BASE_DIR, "chromedriver", filename)
        self.webdriver = webdriver.Chrome(options=options, executable_path=chromedriver_path)

    def crawl(self, url: str):
        """
        If page is dynamically loaded, try parse it with selenium
        :param url:
        :return:
        """
        if not getattr(self, "webdriver", None):
            self._instantiate_webdriver()

        self.webdriver.get(url)
        html = self.webdriver.page_source
        data = self.parse(html)
        self.result.append({**data, 'page': url})

        # Return
        if not self.first_page_only:
            for link in data['links']:
                self.crawl(link)


