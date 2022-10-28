FROM python:bullseye

ENV PYTHONBUFFERED 1

# download warp 
RUN curl -o /etc/cloudflare_warp_2022_9_591_1_amd64_3e650240f8.deb https://pkg.cloudflareclient.com/uploads/cloudflare_warp_2022_9_591_1_amd64_3e650240f8.deb 
# updates linux packages
RUN apt upgrade -y
RUN apt update -y
# install systemctl to start warp service
RUN apt install systemctl -y
# install warp 
RUN apt install -y /etc/cloudflare_warp_2022_9_591_1_amd64_3e650240f8.deb

#Set up selenium Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN apt-get install -yqq unzip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY scraper.py details.py project.py data_storage.py /app/

ENTRYPOINT ["python3", "project.py"]