import os

from bottle import (
    route,
    run,
    template,
    static_file,
    post,
    request,
    default_app
)
from celery.result import AsyncResult

from sitemap.settings import settings, BASE_DIR
from sitemap.tasks import start_crawler
from sitemap.tasks import app as celery

app = default_app()


@route('/')
def index():
    """
    Render index page
    :return:
    """
    return template("index")


@post('/generate')
def run_crawler():
    """
    Run crawler
    :return:
    """
    task = start_crawler.s(request.json).apply_async()
    return {'uuid':task.id}


@route('/<uuid>')
def get_results(uuid: str):
    """
    Get results from celery
    :param uuid:
    :return:
    """
    results: AsyncResult = celery.AsyncResult(uuid)
    return {'status': results.status, 'results': results.result}


@route('/static/<filepath:path>')
def serve_static(filepath):
    """
    Serve static files (we can do it through nginx or whitenoise also)
    :param filepath:
    :return:
    """
    return static_file(filepath, root=os.path.abspath(os.path.join(BASE_DIR, 'views', 'static')))


if __name__ == "__main__":
    run(**settings)
