FROM python:3.8-alpine

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY src /app/src

WORKDIR /app

ENTRYPOINT ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]

