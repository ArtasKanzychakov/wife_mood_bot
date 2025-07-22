# Берём официальный образ Python 3.9
FROM python:3.9-slim

# Устанавливаем системные зависимости для lxml/psycopg2
RUN apt-get update && \
    apt-get install -y libxml2-dev libxslt-dev python3-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда запуска
CMD ["python", "app/webhook.py"]
