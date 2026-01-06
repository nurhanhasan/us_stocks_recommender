# Python script docker image
FROM python:3.10-slim

WORKDIR /app

COPY app/ /app/app/
COPY db_results/ /app/db_results/
COPY cmd/ /app/cmd/
COPY requirements.txt /app/requirements.txt
COPY main.py /app/main.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]