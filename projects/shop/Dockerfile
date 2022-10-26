FROM python:3.10.8-alpine3.16

WORKDIR /code

COPY . /code/

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.presentation.api.asgi:asgi", "--host", "0.0.0.0", "--port", "8000"]
