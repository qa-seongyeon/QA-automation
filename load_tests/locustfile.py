from locust import HttpUser, task, between

class AutomationExerciseUser(HttpUser):
    host = "https://automationexercise.com"
    wait_time = between(1, 3)

# 상품 조회 트래픽이 가장 많을 것으로 판단되어 가중치를 3으로 설정
    @task(3)  
    def get_products_list(self):
        self.client.get("/api/productsList")

        