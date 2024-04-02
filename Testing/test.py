import requests
import threading
import time
import random
import matplotlib.pyplot as plt

# Функция для отправки GET-запросов к API
def send_get_request(session, url, user_agent):
    start_time = time.time()
    session.headers.update({'User-Agent': user_agent})
    session.get(url)
    end_time = time.time()
    return end_time - start_time

# Функция для отправки POST-запросов к API
def send_post_request(session, url, data, user_agent):
    start_time = time.time()
    session.headers.update({'User-Agent': user_agent})
    response = session.post(url, data=data)
    end_time = time.time()
    return end_time - start_time

# Функция для выполнения тестирования для заданного количества запросов и URL
def run_test(url, num_requests, user_agents):
    times = []
    for i in range(num_requests):
        session = requests.Session()
        user_agent = random.choice(user_agents)
        if i % 2 == 0:
            time_taken = send_get_request(session, url, user_agent)
        else:
            # Для примера, отправляем пустые данные
            time_taken = send_post_request(session, url, {}, user_agent)
        times.append(time_taken)
    return times

# Функция для отправки запросов с разных устройств одновременно
def send_requests_concurrently(url, num_requests, user_agents):
    # Создаем потоки для отправки запросов
    threads = []
    for i in range(num_requests):
        thread = threading.Thread(target=run_test, args=(url, 7, user_agents))
        threads.append(thread)

    # Запускаем все потоки
    for thread in threads:
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # Задаем URL
    api_url = 'http://example.com/api'

    # Задаем количество запросов для тестирования
    num_requests = 10

    # Список пользовательских агентов
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.3'
    ]

    # Выполняем тестирование
    send_requests_concurrently(api_url, num_requests, user_agents)

    # Выводим гистограмму времени выполнения
    plt.hist(times, bins=10)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency')
    plt.title('Time Taken for Each Request')
    plt.show()
