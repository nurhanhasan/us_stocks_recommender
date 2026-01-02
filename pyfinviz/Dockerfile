# Python script docker image
FROM python:3.10-slim

WORKDIR /app

COPY pyfinviz_ext/ /app/pyfinviz_ext/
COPY main.py /app/main.py
COPY config.py /app/config.py
COPY requirements.txt /app/requirements.txt

RUN mkdir -p /app/db

EXPOSE 4000

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]