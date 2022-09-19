FROM python:3.8.1

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
EXPOSE 8115

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./api
WORKDIR /api/app
CMD python main.py
