FROM ubuntu:16.04

WORKDIR /usr/src/

COPY requirements.txt ./

RUN apt-get update && apt-get install -y python3-dev python-pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install -y ffmpeg libav-tools

CMD [ "python", "./download_videos.py" ]
