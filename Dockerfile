FROM python:3.5.6-alpine3.9
LABEL maintainer = "Jose Pablo Domingo Aramburo Sanchez <josepablo.aramburo@laziness.rocks>"

ARG CONTAINER_TIMEZONE=America/Mazatlan

WORKDIR /code
ADD . .

RUN apk add ffmpeg

RUN apk add --no-cache --virtual .build-deps pkgconfig freetype-dev g++ make cmake jpeg-dev tzdata && \
cp /usr/share/zoneinfo/America/Mazatlan /etc/localtime && \
echo $CONTAINER_TIMEZONE > /etc/timezone && \
pip install -r requirements.txt && \
apk del .build-deps

CMD ["python", "app.py"]
