FROM python:3.10.6

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt && pip install -U python-dotenv

COPY . .

CMD [ "python", "src/main.py" ]