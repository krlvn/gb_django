from locust import HttpUser, task

SERVER_ADDR = 'ovz12.j91185963.m1yvm.vps.myjino.ru'

class LoadTestingBraniacLMS(HttpUser):
    @task
    def test_some_pages_open(self):
        # Mainapp
        self.client.get(f'http://{SERVER_ADDR}/mainapp/')
        self.client.get(f'http://{SERVER_ADDR}/mainapp/news/')
        self.client.get(f'http://{SERVER_ADDR}/mainapp/news/1/')
        self.client.get(f'http://{SERVER_ADDR}/mainapp/courses/')
        self.client.get(f'http://{SERVER_ADDR}/mainapp/courses/1/')
        self.client.get(f'http://{SERVER_ADDR}/mainapp/doc_site/')
        self.client.get(f'http://{SERVER_ADDR}/mainapp/contacts/')

        # Authapp
        self.client.get(f'http://{SERVER_ADDR}/authapp/register/')
        self.client.get(f'http://{SERVER_ADDR}/authapp/login/')
