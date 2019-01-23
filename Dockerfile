FROM python:3.6-alpine3.6

WORKDIR /app

ENV http_proxy http://proxy.noc.kochi-tech.ac.jp:3128
ENV https_proxy http://proxy.noc.kochi-tech.ac.jp:3128

COPY ./requirements.txt /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]]