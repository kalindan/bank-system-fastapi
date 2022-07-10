FROM python:3.10

WORKDIR /code

COPY ./prod-requirements.txt /code/prod-requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/prod-requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
