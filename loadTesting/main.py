import requests
import time
import matplotlib.pyplot as plt


# Функция для отправки запросов к API
def send_request(url):
    start_time = time.time()
    requests.get(url)
    end_time = time.time()
    return end_time - start_time

# Функция для выполнения тестирования для заданного количества запросов и URL
def run_test(url, num_requests):
    times = []
    for _ in range(num_requests):
        time_taken = send_request(url)
        times.append(time_taken)
    return times


# Функция для построения графика
def plot_results(results, num_instances):
    plt.bar(range(len(results)), results, align='center')
    plt.xticks(range(len(results)), ['Request {}'.format(i + 1) for i in range(len(results))])
    plt.xlabel('Request')
    plt.ylabel('Time (seconds)')
    plt.title('Average Time Taken for Each Request with {} Instances'.format(num_instances))
    plt.show()


if __name__ == "__main__":
    # Задаем URL
    api_url = 'http://example.com/api'

    # Задаем количество запросов для тестирования
    num_requests = 10

    # Выполняем тестирование
    times = run_test(api_url, num_requests)

    # Построение графика
    plot_results(times, 1)  # Для одного экземпляра
