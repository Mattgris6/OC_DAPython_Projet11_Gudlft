import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

MAX_PLACES = 12

controle_club = {}
for club in clubs:
    controle_club[club['name']] = {}
    for competition in competitions:
        controle_club[club['name']][competition['name']] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash("Sorry, that email was not found.", 'error')
        return redirect(url_for('index'))
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    alreadyBooked = controle_club[club['name']][competition['name']]
    # Checks if club has enough points
    if placesRequired > int(club["points"]):
        flash(f'You do not have enough points.')
        return render_template('booking.html',club=club,competition=competition)
    # Checks if place booked > 12
    print(alreadyBooked)
    placesBooked = placesRequired + alreadyBooked
    if placesBooked > MAX_PLACES:
        flash(f"""You can not purchase more than 12 places per competition,
        and you have already booked {alreadyBooked} in this one.""")
        return render_template('booking.html',club=club,competition=competition)
    # Update the counters
    controle_club[club['name']][competition['name']] += placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))