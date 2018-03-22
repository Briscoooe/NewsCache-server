FROM python:3.6-alpine

#ARG news_api_key
#ENV NEWS_API_KEY=$news_api_kkey

RUN apk update
RUN pip3 install pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY newscache ./newscache

RUN pipenv --three 
RUN pipenv install 

EXPOSE 5000
CMD "/usr/src/app/startup.sh"