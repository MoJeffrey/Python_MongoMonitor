FROM python:3.9

ADD . /code

WORKDIR /code/src

RUN pip install -r requirement.txt

CMD ["python", "app.py"]
