import requests
import time
import matplotlib.pyplot as plt


# Функция для отправки GET запроса к API
def send_get_request(session, url):
    start_time = time.time()
    req = session.get(url)
    end_time = time.time()
    print(req.content)
    return end_time - start_time


# Функция для отправки POST-запросов к API
def send_post_request(session, url, data):
    start_time = time.time()
    req = session.post(url, data=data)
    end_time = time.time()
    print(req.content)
    return end_time - start_time


# Функция для выполнения тестирования для заданного количества запросов и URL
def run_test(url, num_requests, session):
    times = []
    for _ in range(num_requests):
        time_taken = send_get_request(session, url)
        times.append(time_taken)

    print(f'average time for response: {sum(times) / len(times)}')
    return times


# Функция для построения графика
def plot_results(results):
    plt.bar(range(len(results)), results, align='center')
    plt.ylabel('Time (seconds)')
    plt.title('Time taken for each request')
    plt.show()


if __name__ == "__main__":
    curr_session = requests.Session()
    login = curr_session.post(url='http://localhost:80/login_admin', data={'username': '@prokhorkot',
                                                                           'password': 'qwerty1234'})
    print(login.content)

    # Задаем URL
    api_url = 'http://localhost:80/manage_clients'

    # Задаем количество запросов для тестирования
    num_requests = 10

    # Выполняем тестирование
    times = run_test(api_url, num_requests, curr_session)

    # Построение графика
    plot_results(times)
