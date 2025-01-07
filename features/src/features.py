import pika
import numpy as np
import json
import time
from datetime import datetime
from sklearn.datasets import load_diabetes

# Создаём подключение к очереди RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Создаем очереди
channel.queue_declare(queue='y_true')
channel.queue_declare(queue='features')

# Загружаем датасет
X, y = load_diabetes(return_X_y=True)

while True:
    try:
        # Генерация случайного индекса
        random_row = np.random.randint(0, X.shape[0] - 1)
        
        # Генерация уникального ID для сообщения
        message_id = datetime.timestamp(datetime.now())
        
        # Формируем сообщение для y_true
        message_y_true = {
            'id': message_id,
            'body': y[random_row]
        }
        # Отправка сообщения в очередь y_true
        channel.basic_publish(exchange='', routing_key='y_true', body=json.dumps(message_y_true))
        print(f"Сообщение с правильным ответом {y[random_row]} отправлено в очередь")

        # Формируем сообщение для features
        message_features = {
            'id': message_id,
            'body': list(X[random_row])
        }
        # Отправка сообщения в очередь features
        channel.basic_publish(exchange='', routing_key='features', body=json.dumps(message_features))
        print(f"Сообщение с признаками {X[random_row]} отправлено в очередь")

        # Задержка
        time.sleep(1)

    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
