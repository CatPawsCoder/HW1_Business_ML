import pika
import pickle
import numpy as np
import json

# Загружаем модель
with open('myfile.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

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
