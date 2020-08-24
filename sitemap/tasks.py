from celery import Celery
from sitemap.spider.crawler import Crawler, SeleniumCrawler

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@app.task
def start_crawler(json: dict):
    """
    Use celery to avoid blocking in case of big tasks
    :return:
    """
    url = json.get('url')
    first_page = json.get('first_page', True)
    is_spa = json.get('is_spa', False)
    args = {
        'start_url': url,
        'first_page': first_page
    }
    crawler = SeleniumCrawler(**args) if is_spa else Crawler(**args)
    return crawler.run_crawler()
