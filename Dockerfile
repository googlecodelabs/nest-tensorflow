FROM python:2.7-slim
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code
CMD ["python", "app.py"]
