import pika
import pickle
import numpy as np
import json
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_diabetes

# 1. Обучаем модель, если файл не существует
try:
    with open('myfile.pkl', 'rb') as pkl_file:
        regressor = pickle.load(pkl_file)
    print("Модель загружена из файла.")
except FileNotFoundError:
    print("Файл модели не найден, обучаем новую модель...")
    
    # Загружаем датасет
    X, y = load_diabetes(return_X_y=True)
    
    # Обучаем модель
    regressor = LinearRegression()
    regressor.fit(X, y)
    
    # Сохраняем модель в файл
    with open('myfile.pkl', 'wb') as pkl_file:
        pickle.dump(regressor, pkl_file)
    print("Модель обучена и сохранена в файл myfile.pkl.")

# Подключение к очереди RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Создаем очереди
channel.queue_declare(queue='features')
channel.queue_declare(queue='y_pred')

# Функция обработки сообщений
def callback(ch, method, properties, body):
    print(f'Получен вектор признаков {body}')
    features = json.loads(body)
    
    # Предсказание
    pred = regressor.predict(np.array(features).reshape(1, -1))
    
    # Отправка предсказания
    message = {
        'id': properties.message_id,  # Используем ID из сообщения
        'body': pred[0]
    }
    channel.basic_publish(exchange='', routing_key='y_pred', body=json.dumps(message))
    print(f'Предсказание {pred[0]} отправлено в очередь y_pred')

# Подключаем функцию к очереди
channel.basic_consume(queue='features', on_message_callback=callback, auto_ack=True)

print('Ожидание сообщений...')

channel.start_consuming()

