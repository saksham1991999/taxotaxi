FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt ./
ADD . /usr/src/app/
RUN pip install -r requirements.txt
RUN python manage.py migrate