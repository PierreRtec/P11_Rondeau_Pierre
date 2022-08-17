import json
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()

actual_date = str(datetime.now())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary() -> str:
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template(
            "welcome.html", club=club, competitions=competitions, date=actual_date
        )
    except IndexError:
        return render_template(
            "index.html", error_message="Sorry, that email wasn't found. Try again."
        )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition and foundCompetition["date"] >= actual_date:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=club, competitions=competitions, date=actual_date
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    placesCompetition = int(competition["numberOfPlaces"])
    clubPoints = int(club["points"])
    if placesRequired <= 0:
        flash("Ne peut être inférieur ou égal à 0")
    elif placesRequired > 12:
        flash("Vous ne pouvez pas réserver plus de 12 places à la fois.")
    elif placesRequired > placesCompetition:
        flash(
            "Attention, vous avez selectionner plus de places que le nombre de place maximum."
        )
    elif clubPoints < placesRequired:
        flash("Vous n'avez pas assez de points")
    else:
        competition["numberOfPlaces"] = placesCompetition - placesRequired
        club["points"] = int(club["points"]) - placesRequired
        flash("Great-booking complete!")
    return render_template(
        "welcome.html", club=club, competitions=competitions, date=actual_date
    )


@app.route("/displayboard")
def club_table():
    return render_template("displayboard.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
