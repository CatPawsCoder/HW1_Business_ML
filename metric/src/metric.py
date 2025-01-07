import pika
import json
import pandas as pd
from datetime import datetime

# Подключение к очереди RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Создаем очереди
channel.queue_declare(queue='y_true')
channel.queue_declare(queue='y_pred')

# Инициализируем DataFrame для логирования
df = pd.DataFrame(columns=['id', 'y_true', 'y_pred', 'absolute_error'])

# Функция для расчета абсолютной ошибки
def calculate_absolute_error(y_true, y_pred):
    return abs(y_true - y_pred)

# Функция обработки сообщений
def callback(ch, method, properties, body):
    global df
    
    # Получаем данные из очереди
    message = json.loads(body)
    message_id = message['id']
    value = message['body']
    
    if method.routing_key == 'y_true':
        y_true = value
        # Добавляем данные в DataFrame
        df = df.append({'id': message_id, 'y_true': y_true}, ignore_index=True)
    elif method.routing_key == 'y_pred':
        y_pred = value
        # Находим соответствующую строку по ID
        df.loc[df['id'] == message_id, 'y_pred'] = y_pred
        # Вычисляем абсолютную ошибку
        df.loc[df['id'] == message_id, 'absolute_error'] = calculate_absolute_error(y_true, y_pred)
    
    # Сохраняем в CSV
    df.to_csv('./logs/metric_log.csv', index=False)

# Подключаем функции к очередям
channel.basic_consume(queue='y_true', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue='y_pred', on_message_callback=callback, auto_ack=True)

print('Ожидание сообщений...')

channel.start_consuming()
