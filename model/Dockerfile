# Используем официальный Python образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей (requirements.txt) в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код в контейнер
COPY src /app/src

# Устанавливаем переменные окружения для логирования
ENV PYTHONUNBUFFERED=1

# Команда по умолчанию для запуска вашего приложения
CMD ["python", "src/model.py"]

