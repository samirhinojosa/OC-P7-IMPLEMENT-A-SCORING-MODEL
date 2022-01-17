FROM python:3.9-slim

RUN mkdir /fastapi

RUN pip install --upgrade pip==21.3.1

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt

COPY . /fastapi

EXPOSE 8008

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8008"]

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1