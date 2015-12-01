FROM ubuntu:14.04
MAINTAINER Ashok Raja <ashokraja.r@gmail.com>

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ADD . /app
RUN pip3 install -r /app/requirements.txt

EXPOSE 5000
WORKDIR /app

ENTRYPOINT ["gunicorn", "mylife:app"]
CMD ["-b", "0.0.0.0:5000"]
