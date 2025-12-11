from configs.config import Config
from utils.session import UseSession
from utils.tools import log_retry_error
from tenacity import retry, stop_after_attempt, wait_exponential
import time

class RecaptchaSolver:
    def __init__(self, client_json: dict):
        self.session = UseSession().get_session()
        self.client_json = Config().get_client_json()
        self.api_key = self.client_json.get("api_key")
        self.api_url = self.client_json.get("api_url")
        self.captcha_type = self.client_json.get("captcha_type")

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=3, min=6, max=9), retry_error_callback=log_retry_error)
    def get_balance(self) -> float:
        resp = self.session.get(
            url=f"{self.api_url}/getBalance",
            json={
                "clientKey": self.api_key,
            }
        )
        return resp.json()["balance"]

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=3, min=6, max=9), retry_error_callback=log_retry_error)
    def create_task(self, task_type: str, website_url: str, website_key: str) -> str:
        resp = self.session.post(
            url=f"{self.api_url}/createTask",
            json={
                "clientKey": self.api_key,
                "task": {
                    "type": task_type,
                    "websiteURL": website_url,
                    "websiteKey": website_key
                }
            }
        )
        return resp.json()["taskId"]

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=3, min=6, max=9), retry_error_callback=log_retry_error)
    def get_task_result(self, task_id: str) -> dict:
        resp = self.session.get(
            url=f"{self.api_url}/getTaskResult",
            json={
                "clientKey": self.api_key,
                "taskId": task_id
            }
        )
        return resp.json()
    
    def solve_recaptcha(self, website_url: str, website_key: str) -> str:
        balance = self.get_balance()
        print(f"Balance: {balance}")
        if balance < 0.1:
            raise ValueError("Insufficient balance")

        task_id = self.create_task("ReCaptchaTaskProxyLess", website_url, website_key)

        while True:
            task_result = self.get_task_result(task_id)
            if task_result.get("status") == "ready":
                return task_result.get("solution").get("gRecaptchaResponse")
            else:
                print(f"Task {task_id} not ready, waiting 15 seconds: {task_result}")
                time.sleep(15)
                continue
