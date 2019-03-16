FROM python:3.5.6-alpine3.9
ADD . /code
WORKDIR /code
RUN apk add ffmpeg
RUN apk add pkgconfig freetype-dev g++ make cmake jpeg-dev
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
