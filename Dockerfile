FROM python:3.8-slim

RUN apt-get update && apt-get install build-essential -y

COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock
RUN pip install pipenv
RUN pipenv install --system

WORKDIR /app
EXPOSE 8080
CMD ["python","-m","sitemap.server"]