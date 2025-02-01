# Используем официальный образ Python 3.13
FROM python:3.13-slim

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    TZ=Asia/Bishkek

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

# Обновляем репозитории и устанавливаем зависимости системы
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    gcc \
    python3-dev \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект в контейнер
COPY . .

# Открываем порты
EXPOSE 8000 8001

# Команда запуска по умолчанию
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:8000 & daphne -b 0.0.0.0 -p 8001 config.asgi:application"]
