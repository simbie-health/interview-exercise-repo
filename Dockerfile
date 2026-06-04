FROM python:3.13-slim

WORKDIR /app

# Don't buffer stdout/stderr — needed so the interactive prompts show up immediately
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
