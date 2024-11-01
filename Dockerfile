FROM python:3.12

WORKDIR /application

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 2000
ENV API_HOST="0.0.0.0"
ENTRYPOINT [ "sh", "entrypoint.sh" ]
