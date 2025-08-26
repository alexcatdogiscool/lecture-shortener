

FROM python:3.8

WORKDIR /wrk
COPY . .

RUN apt-get update && apt-get install -y ffmpeg

CMD ["sh", "-c", "ffmpeg -version > out"]
