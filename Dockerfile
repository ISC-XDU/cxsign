FROM python:3.7

# Configure the app
RUN mkdir /app
COPY . /app 
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN python /app/setup.py

# Configure apt
RUN apt-get update  \
&&apt-get -y install cron

# Correct time region to the current area
RUN rm -f /etc/localtime    \
    && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# Set up the crontab for auto sign-in
COPY cxsign-cron /etc/cron.d/cxsign-cron
RUN chmod 0644 /etc/cron.d/cxsign-cron
RUN crontab /etc/cron.d/cxsign-cron
WORKDIR /app

CMD ["/bin/bash","run.sh"]