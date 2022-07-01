FROM python:3-slim-buster

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]