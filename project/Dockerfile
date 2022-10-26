FROM python:latest

RUN mkdir /mydirectory

WORKDIR /mydirectory

COPY scraper.py details.py data_storage.py project.py /mydirectory/

ENTRYPOINT ["python3", "project.py"]