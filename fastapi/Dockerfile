FROM python:3.9-slim

RUN mkdir /fastapi

RUN pip install --upgrade pip==21.3.1

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt

COPY . /fastapi

EXPOSE 8008

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8008"]