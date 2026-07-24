FROM python:3.10.6

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt && pip install -U python-dotenv

COPY . .

# cwd stays /app so the Quran corpus files (quran-data.xml, en.ahmedraza, ...)
# resolve; --app-dir puts src/ on the import path for `main:app`.
CMD ["uvicorn", "main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]