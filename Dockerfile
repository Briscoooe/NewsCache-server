LABEL maintainer="Briscoooe"
FROM python:3.6-alpine

RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl git
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN pip3 install pipenv==11.9.0

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock startup.sh ./
COPY newscache ./newscache

RUN pipenv --three 
RUN pipenv install 

EXPOSE 5000
CMD "/usr/src/app/startup.sh"