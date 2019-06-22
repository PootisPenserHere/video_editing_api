FROM python:3.5.6-alpine3.9
LABEL maintainer = "Jose Pablo Domingo Aramburo Sanchez <josepablo.aramburo@laziness.rocks>"

WORKDIR /code
ADD . .

RUN apk --no-cache add ffmpeg tzdata

RUN apk add --no-cache --virtual .build-deps pkgconfig freetype-dev g++ make cmake jpeg-dev && \
pip install --no-cache-dir -r requirements.txt && \
apk del .build-deps

CMD ["gunicorn" , "-b", "0.0.0.0:5000", "--reload", "app:app"]
