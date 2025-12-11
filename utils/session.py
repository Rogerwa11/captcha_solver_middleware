from requests import Session
from fake_useragent import UserAgent

class UseSession:
    def __init__(self):
        self.session = Session()
        self.session.headers.update({
            "User-Agent": UserAgent().random,
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Charset": "utf-8",
        })

    def get_session(self) -> Session:
        return self.session
