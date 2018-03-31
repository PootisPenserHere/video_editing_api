FROM python:3.5
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN pip install moviepy[optional]
CMD ["python", "app.py"]
