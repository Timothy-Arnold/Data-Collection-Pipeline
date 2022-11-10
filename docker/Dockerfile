FROM python:bullseye

RUN apt update -y

#Set up selenium Chrome

RUN apt-get install -y wget 
RUN apt-get install -y gnupg2
RUN apt-get install -y curl
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN apt-get install -yqq unzip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN wget -O cloudflare_warp_2022_9_591_1_amd64_ba53b9eb5d.deb https://pkg.cloudflareclient.com/uploads/cloudflare_warp_2022_9_591_1_amd64_3e650240f8.deb 
RUN apt-get install -y systemctl
RUN apt-get install -y libcap2
RUN apt-get install -y nftables
RUN apt-get install -y libcap2-bin
RUN apt-get install -y libdbus-1-3
RUN apt-get install -y desktop-file-utils
RUN dpkg -i cloudflare_warp_2022_9_591_1_amd64_ba53b9eb5d.deb
RUN rm cloudflare_warp_2022_9_591_1_amd64_ba53b9eb5d.deb
RUN systemctl start warp-svc.service

RUN mkdir /app

WORKDIR /app

COPY scraper.py details.py project.py data_storage.py /app/

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

CMD ["python3", "project.py"]