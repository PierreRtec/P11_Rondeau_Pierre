from assertpy import assert_that

import server


class TestLoadClubs:
    def test_load_clubs_data(self):
        # initialisation
        clubs_json = [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]

        # expected
        expected_result = clubs_json

        # method call
        result = server.loadClubs()

        # assertions
        assert_that(result).is_equal_to(expected_result)


class TestLoadCompetitions:
    def test_load_competitions_nominal(self):
        # initialisation
        competitions_json = [
            {
                "name": "Spring Festival",
                "date": "2022-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2022-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]

        # expected
        expected_result = competitions_json

        # method call
        result = server.loadCompetitions()

        # assertions
        assert_that(result).is_equal_to(expected_result)
