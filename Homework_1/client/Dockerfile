FROM python:3.13.0a4-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY 200MB.txt 200MB.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]