FROM python:3.8
RUN pip install --no-cache-dir gunicorn

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD [ "bash", "run_prod.sh", "--bind", "0.0.0.0:80" ]
