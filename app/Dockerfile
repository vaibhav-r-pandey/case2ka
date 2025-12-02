FROM python:3.11-slim

WORKDIR /opt/app-root/src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 8080

USER 1001

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]