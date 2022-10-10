FROM python:3.7

# Configure the app
RUN mkdir /app
COPY . /app 
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN python /app/setup.py

# Set up the crontab for auto sign-in
RUN apt-get update \
&&apt-get -y install cron
COPY cxsign-cron /etc/cron.d/cxsign-cron
RUN chmod 0644 /etc/cron.d/cxsign-cron
RUN crontab /etc/cron.d/cxsign-cron
WORKDIR /app

CMD ["/bin/bash","run.sh"]