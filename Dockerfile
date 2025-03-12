# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем переменную окружения для отображения вывода в консоли
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.pip /app/
RUN pip install --no-cache-dir -r requirements.pip

# Копируем все содержимое текущей директории в контейнер в /app
COPY . /app/
