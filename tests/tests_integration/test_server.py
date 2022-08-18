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

    def test_show_summary_ok(
        self,
        client,
    ):
        # initialisation
        email = "admin@irontemple.com"

        # expectation
        expected_status_code = 200

        # method_call
        result = client.post("/showSummary", data={"email": email})

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)


class TestPurchasePlaces:
    def test_purchase_places_zero(self, client):
        # expectations
        expected_status_code = 200
        club = server.clubs[1]
        comp = server.competitions[1]

        # method_call
        result = client.post(
            "/purchasePlaces",
            data={
                "competition": comp["name"],
                "club": club["name"],
                "places": 0,
            },
        )
        error_message = "Ne peut être inférieur ou égal à 0"

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)
        assert_that(result.data.decode()).contains(error_message)

    def test_purchase_places_over_12(self, client):
        # expectations
        expected_status_code = 200
        club = server.clubs[0]
        comp = server.competitions[0]

        # method_call
        result = client.post(
            "/purchasePlaces",
            data={
                "competition": comp["name"],
                "club": club["name"],
                "places": 13,
            },
        )
        error_message = "Vous ne pouvez pas réserver plus de 12 places à la fois."

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)
        assert_that(result.data.decode()).contains(error_message)

    def test_purchase_places_over_places_comp(self, client):
        # initialisation
        competition = server.competitions[1]
        club = server.clubs[0]

        # expectations
        expected_status_code = 200

        # method_call
        result = client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": 27,
            },
        )

        error_message = "Attention, vous avez selectionner plus de places que le nombre de place maximum."

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)
        assert_that(result.data.decode()).contains(error_message)

    def test_purchase_places_not_enought_club_points(self, client):
        # initialisation
        competition = server.competitions[1]
        club = server.clubs[1]

        # expectations
        expected_status_code = 200

        # method_call
        result = client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": 5,
            },
        )

        error_message = "Vous n&#39;avez pas assez de points"

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)
        assert_that(result.data.decode()).contains(error_message)

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


class TestClubTable:
    def test_club_table_nominal(self, client):
        # expected
        expected_status_code = 200

        # method_call
        result = client.get("/displayboard")

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)


class TestLogout:
    def test_logout_nominal(self, client):
        # expected
        expected_status_code = 302

        # method_call
        result = client.get("/logout")

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)


class TestIndex:
    def test_index_nominal(self, client):
        # expected
        expected_status_code = 200

        # method_call
        result = client.get("/")

        # assertions
        assert_that(result.status_code).is_equal_to(expected_status_code)
