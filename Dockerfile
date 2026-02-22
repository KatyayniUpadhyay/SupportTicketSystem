FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# 🔹 Give execution permissions to the script
RUN chmod +x /app/start.sh

EXPOSE 8000

# 🔹 Use the script instead of the direct runserver command
CMD ["sh", "/app/start.sh"]