FROM python:3.11

WORKDIR /rlpmdb

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY cogs cogs
COPY db db
COPY models models
COPY __init__.py .
COPY main.py .
COPY .env .

CMD ["python3", "main.py"]
