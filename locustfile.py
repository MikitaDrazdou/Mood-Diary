import random
from datetime import datetime

from locust import HttpUser, task, between


class MoodDiaryUser(HttpUser):
    wait_time = between(1, 3)
    user_id = None
    token = None

    def on_start(self):
        username = f"test_user_{random.randint(1, 1000000)}"
        email = f"{username}@test.com"
        password = "testpassword123"

        response = self.client.post(
            "/register",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )

        if response.status_code == 201:
            # login with the new user
            login_response = self.client.post(
                "/login",
                json={
                    "username": username,
                    "password": password
                }
            )
            if login_response.status_code == 200:
                self.user_id = login_response.json().get("user_id")

    @task(3)
    def create_mood_entry(self):
        if not self.user_id:
            return

        date = datetime.now().date()
        mood_score = random.randint(1, 10)
        emoji = random.choice(["😊", "😐", "😢", "😡", "😴"])
        notes = "Test entry"
        activities = "reading,walking,sleeping"

        self.client.post(
            "/mood-entry",
            json={
                "date": str(date),
                "mood_score": mood_score,
                "emoji": emoji,
                "notes": notes,
                "activities": activities
            },
            params={"user_id": self.user_id}
        )

    @task(2)
    def get_mood_entries(self):
        # get all mood entries for the user
        if not self.user_id:
            return

        self.client.get(f"/mood-entries/{self.user_id}")

    @task(1)
    def get_monthly_entries(self):
        if not self.user_id:
            return

        current_date = datetime.now()
        self.client.get(
            f"/mood-entries/{self.user_id}/{current_date.year}/{current_date.month}"
        )

    @task(1)
    def get_stats(self):
        if not self.user_id:
            return

        self.client.get(f"/stats/{self.user_id}")

    @task(1)
    def check_health(self):
        self.client.get("/health")
