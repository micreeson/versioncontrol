FROM python:3.7.5

RUN mkdir /code \
&&apt-get update \
&&apt-get -y install freetds-dev \
&&apt-get -y install unixodbc-dev \
&&apt-get -y install vim
COPY service /code
COPY requirements /code
RUN pip install -r /code/requirements -i https://pypi.douban.com/simple
WORKDIR /code

CMD ["/bin/bash","run.sh"]
