import sys
import os

from webtest import TestApp
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
print(sys.path)
from sitemap.server import app as sitemap_app


def test_index():
    app = TestApp(sitemap_app)
    assert app.get('/').status_code == 200
