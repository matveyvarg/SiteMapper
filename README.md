# SITE MAPPER

Generate site's map in json and visualize it with d3 library

### JSON FORMAT:
```
{
    "page": <str> -- url of page
    "links": [] -- list of links in this page
    "css": [] --list of css files in this page
    "js": [] --list of js files in this page
}
```
\*Robot skip files inside `iframe`

### USAGE
The easiest way to run robot - docker:
```
docker-compose up
```
Or you can manually install **Redis** and dependencies (using **Pipenv**):
```
pipenv install
```
then run separately:
```
python -m sitemap.server
```

```
celery -A sitemap.tasks worker
```
