FROM python:3.9-slim

RUN mkdir /streamlit

RUN pip install --upgrade pip==21.3.1

COPY requirements.txt /streamlit

WORKDIR /streamlit

RUN pip install -r requirements.txt

COPY . /streamlit

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]