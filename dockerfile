FROM python:3.9

ENV PYTHONIOENCODING=utf-8

WORKDIR /app

COPY ./app .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]