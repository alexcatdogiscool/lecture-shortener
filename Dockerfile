

FROM python:3.8-slim

WORKDIR /wrk

COPY ./app .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python3 ./app/app.py"]
