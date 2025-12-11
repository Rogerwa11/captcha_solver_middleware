import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.solver_name = os.getenv("SOLVER_NAME")
        self.captcha_type = os.getenv("CAPTCHA_TYPE")
        print(self.captcha_type)
        self.capsolver_api_key = os.getenv("CAPSOLVER_API_KEY")
        self.capmonster_api_key = os.getenv("CAPMONSTER_API_KEY")
        self.anticaptcha_api_key = os.getenv("ANTICAPTCHA_API_KEY")

    def get_client_json(self) -> dict:
        if self.solver_name == "capsolver" or self.solver_name == "anticaptcha":
            if 'V2' in self.captcha_type and 'proxyless' in self.captcha_type:
                captcha_type = 'ReCaptchaV2TaskProxyLess'
            elif 'V3' in self.captcha_type and 'proxyless' in self.captcha_type:
                captcha_type = 'ReCaptchaV3TaskProxyLess'
            elif 'V2' in self.captcha_type and 'enterprise' in self.captcha_type:
                captcha_type = 'ReCaptchaV2EnterpriseTaskProxyLess'
            elif 'V3' in self.captcha_type and 'enterprise' in self.captcha_type:
                captcha_type = 'ReCaptchaV3EnterpriseTaskProxyLess'
            else:
                raise ValueError(f"Captcha type {self.captcha_type} not found")

            return {
                "api_url": "https://api.capsolver.com" if self.solver_name == "capsolver" else "https://api.anticaptcha.com",
                "api_key": self.capsolver_api_key,
                "captcha_type": captcha_type
            }

        elif self.solver_name == "capmonster":
            if 'V2' in self.captcha_type:
                captcha_type = 'RecaptchaV2Task'
            elif 'V3' in self.captcha_type:
                captcha_type = 'RecaptchaV3Task'
            else:
                raise ValueError(f"Captcha type {self.captcha_type} not found")

            return {
                "api_url": "https://api.capmonster.cloud",
                "api_key": self.capmonster_api_key,
                "captcha_type": captcha_type
            }

        else:
            raise ValueError(f"Solver name {self.solver_name} not found")
