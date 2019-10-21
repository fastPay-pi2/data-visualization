FROM python:3.6-alpine

WORKDIR /usr/src/app

COPY ./src  /usr/src/app/

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "seed_elastic.py"]