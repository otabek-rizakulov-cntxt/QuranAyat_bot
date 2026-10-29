FROM python:3.10.6

# Unbuffered stdout/stderr so logs show up live in the platform's log viewer.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# The corpora in data/ are found relative to the code, not the cwd;
# --app-dir puts src/ on the import path for `main:app`.
# Shell form so ${PORT} (injected by Railway/Render/etc.) is expanded; falls back to 8000 locally.
CMD uvicorn main:app --app-dir src --host 0.0.0.0 --port ${PORT:-8000}
