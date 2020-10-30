FROM python:3.8.1

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./
WORKDIR /app

CMD python main.py
