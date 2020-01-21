FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /ufo_hotspots
WORKDIR /ufo_hotspots
COPY requirements.txt /ufo_hotspots/
RUN pip install -r requirements.txt
COPY . /ufo_hotspots/