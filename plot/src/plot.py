import pandas as pd
import matplotlib.pyplot as plt
import time
import os

LOG_PATH = './logs/metric_log.csv'
IMAGE_PATH = './logs/error_distribution.png'

def plot_error_distribution():
    # Если файл логов не существует, просто выходим
    if not os.path.exists(LOG_PATH):
        return

    # Загружаем данные из CSV
    df = pd.read_csv(LOG_PATH)
    
    # Строим гистограмму абсолютных ошибок
    plt.figure(figsize=(10, 6))
    plt.hist(df['absolute_error'], bins=20, edgecolor='black')
    plt.title('Распределение абсолютных ошибок')
    plt.xlabel('Абсолютная ошибка')
    plt.ylabel('Частота')
    
    # Сохраняем изображение
    plt.savefig(IMAGE_PATH)
    plt.close()

def main():
    while True:
        plot_error_distribution()
        time.sleep(5)  # Обновляем каждый 5 секунд

if __name__ == "__main__":
    main()
