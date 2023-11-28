FROM python:3.10.9-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /Nobita-Filter-Bot
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
WORKDIR /Nobita-Filter-Bot
COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]
