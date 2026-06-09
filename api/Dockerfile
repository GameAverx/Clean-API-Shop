FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/api

ENV PYTHONPATH=/app

EXPOSE 8001
CMD ["python", "-m", "api.server"]

# docker build api/.
# docker run -p 8080:8001 =id=
# удаление = rm
# docker image rm =id=

# # 1. Остановить старый контейнер
# docker stop my-api-container
# docker rm my-api-container

# 2. Пересобрать образ
# docker build -t api-image .

# 3. Запустить новый контейнер
# docker run -d -p 8080:8001 --name my-api-container api-image
# логи в контейнере
#  docker logs -f my-api-container