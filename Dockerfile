FROM python:3.5.6-alpine3.9
LABEL maintainer = "Jose Pablo Domingo Aramburo Sanchez <josepablo.aramburo@laziness.rocks>"

WORKDIR /code
ADD . .

RUN apk add ffmpeg tzdata

RUN apk add --no-cache --virtual .build-deps pkgconfig freetype-dev g++ make cmake jpeg-dev && \
pip install --no-cache-dir -r requirements.txt && \
apk del .build-deps

CMD ["python", "app.py"]
