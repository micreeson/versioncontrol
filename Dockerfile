FROM python:3.7.5

RUN mkdir /code \
&&apt-get update \
&&apt-get -y install freetds-dev \
&&apt-get -y install unixodbc-dev \
&&apt-get -y install vim

RUN pip install -r /code/requirements -i https://pypi.douban.com/simple

COPY service /code
COPY run.sh /code
COPY requirements /code
WORKDIR /code

CMD ["/bin/bash","run.sh"]