FROM python:3.12-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py /opt/
COPY templates /opt/templates


EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]
