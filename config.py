import os


class Config:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
        self.default_location = "United States"
        self.max_results = 20
        self.delay_between_requests = 2
        self.timeout = 30

        # 🔥 NEW
        self.headless = True
        self.category_filter = None

        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        )

    def get_user_agent(self):
        return self.user_agent

    def get_max_results(self):
        return self.max_results
