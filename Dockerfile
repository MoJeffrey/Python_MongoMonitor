FROM python:3.9

ADD . /code

WORKDIR /code

RUN pip install -r requirement.txt

CMD ["python", "main.py"]
