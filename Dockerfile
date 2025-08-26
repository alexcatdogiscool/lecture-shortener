

FROM python:3.8

WORKDIR /wrk
COPY ./poc.py .

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python3 poc.py 5 true input/video.mpv 2>error"]
