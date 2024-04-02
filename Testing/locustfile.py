from locust import HttpUser, task, between


class WebsiteTestUser(HttpUser):
    wait_time = between(0.5, 5.0)

    def on_start(self):
        self.client.post('http://localhost:80/login_admin', {'username': '@prokhorkot', 'password': 'qwerty1234'})

    @task(1)
    def get_pg(self):
        self.client.get('http://localhost:80/manage_clients')

    @task(2)
    def get_redis(self):
        self.client.get('http://localhost:80/shopping_cart')

    @task(3)
    def get_cassandra(self):
        self.client.get('http://localhost:80/products')

    @task(4)
    def post_pg(self):
        self.client.post('http://localhost:80/maange_clients', {})

    @task(5)
    def post_cassandra(self):
        self.client.post('http://localhost:80/products', {})
