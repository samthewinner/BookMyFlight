FROM python:3.11-alpine

WORKDIR /code

ENV DATABASE_URL="mysql+mysqlconnector://root:root@host.docker.internal:3306/test"

ENV REDIS_HOST=redis

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "8081"]