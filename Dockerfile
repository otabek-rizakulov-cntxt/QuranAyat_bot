FROM python:3.10.6

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt && pip install -U python-dotenv

COPY . .

EXPOSE 8000

# cwd stays /app so the Quran corpus files (quran-data.xml, en.ahmedraza, ...)
# resolve; --app-dir puts src/ on the import path for `main:app`.
# Shell form so ${PORT} (injected by Railway/Render/etc.) is expanded; falls back to 8000 locally.
CMD echo "Starting uvicorn on port ${PORT:-8000}" && uvicorn main:app --app-dir src --host 0.0.0.0 --port ${PORT:-8000}