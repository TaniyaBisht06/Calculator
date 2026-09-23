FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY calculator2.py .

EXPOSE 5000

CMD ["python", "calculator2.py"]
