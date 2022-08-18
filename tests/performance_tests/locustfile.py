from locust import HttpUser, task

class ProjectPerfTest(HttpUser):

    @task
    def on_start(self):
        self.client.post("showSummary", {"email": "admin@irontemple.com"})

    @task
    def club_table(self):
        self.client.get("displayboard")

    @task
    def perf_index(self):
        self.client.get("/")

    @task
    def booking(self):
        self.client.get("book/Fall Classic/She Lifts")
        self.client.get("book/Spring Festival/Iron Temple")

    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Iron Temple",
                "places": 4,
            })

    def on_stop(self):
        self.client.get("logout")
