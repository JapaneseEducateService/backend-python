FROM python:3.9

ENV PYTHONIOENCODING=utf-8

WORKDIR /app

COPY ./app .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install gunicorn

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:5000", "app:app"]