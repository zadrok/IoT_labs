from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import IntegerField, validators, SubmitField
from wtforms.validators import Length
import requests, json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-good-password'

class player(FlaskForm):
    playerID = IntegerField('Enter player ID: ', validators=[Length(min=5, max = 5, message='ID must be 5 numbers long.')])
    playerLVL = IntegerField('Player Level', [validators.NumberRange(min=0, max=7)])
    submit = SubmitField('Submit')

# route used by Flask to show the main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    title= 'Memory Game'
    formID = player()
    return render_template('index.html', title=title, formID=formID)

# when submit btn is clicked
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        title= 'Memory Game'
        formID = player()
        playerID = request.form['playerID']
    return render_template('index.html',title=title, formID=formID, playerID=playerID)


if __name__ == '__main__':
    app.run(debug=True)
