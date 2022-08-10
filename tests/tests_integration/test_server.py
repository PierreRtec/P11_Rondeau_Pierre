from datetime import datetime

from assertpy import assert_that

import server


class TestShowSummary:
    def test_show_summary_unknown_email_address(
        self,
        client,
    ):
        # expectations
        expected_status_code = 200

        # method_call
        result = client.post("/showSummary", data={"email": "unknown@random.com"})

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)

    def test_show_summary_unknown_email_address_not_found(
        self,
        client,
    ):
        # initialisation
        email_not_found = "Sorry, that email wasn&#39;t found. Try again."

        # method_call
        result = client.post("/showSummary", data={"email": "unkezezanown@zae.com"})

        # assertions
        assert_that(result.data.decode()).contains(email_not_found)


class TestPurchasePlaces:
    def test_purchase_places_nominal(self, client):
        # expectations
        expected_status_code = 200

        # method_call
        result = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Iron Temple",
                "places": 12,
            },
        )

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)

    def test_purchase_places_over_12(self, client):
        # initialisation
        competition = server.competitions[1]
        club = server.clubs[2]
        # expectations
        expected_status_code = 200

        # method_call
        result = client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": 15,
            },
        )

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)

    def test_purchase_places_pts_club_nominal(self, client):
        # initialisation
        competition = server.competitions[1]
        club = server.clubs[2]
        # expectations
        expected_status_code = 200

        # method_call
        result = client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": 12,
                "points": 4,
            },
        )

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)


class TestBook:
    def test_book_nominal_date(self, client):
        # expected
        expected_status_code = 200

        # method_call
        result = client.get("/book/Fall Classic/Simply Lift")

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)

    def test_book_date_past(self, client):
        # expected
        expected_status_code = 200
        error_message = "Something went wrong-please try again"
        # method_call
        result = client.get("/book/Spring Festival/Simply Lift")

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)
        assert_that(result.data.decode()).contains(error_message)