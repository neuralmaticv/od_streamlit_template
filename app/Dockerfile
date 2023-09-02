FROM python:3.9.13

WORKDIR /opt/app

ADD ./app /opt/app
RUN pip install --upgrade pip
RUN pip install -r /opt/app/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
