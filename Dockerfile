FROM python:3.7

RUN mkdir /app \
&&apt-get update \
&&apt-get -y install cron
COPY . /app 
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN crontab -l | { cat; echo "50 7 * * * python /app/core/main.py"; } | crontab -                  asc            \
    &&  crontab -l | { cat; echo "30 13 * * * python /app/core/main.py"; } | crontab -
RUN python /app/setup.py
WORKDIR /app

CMD ["/bin/bash","run.sh"]