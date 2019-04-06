from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired
import requests, json

# create the Flask instance
app = Flask(__name__)
# set a key used for the form
app.config['SECRET_KEY'] = 'a-good-password'

# this class us used to interface with the Arduino
class Arduino:
  def __init__(self):
    self.threshold = 20

# instace of Arduino class
ard = Arduino()

# class for the form
class TempForm(FlaskForm):
  tmepTreshold = DecimalField('Temperature Threshold', validators=[DataRequired()])
  submit = SubmitField('Submit')

# covert the temp received from API from kelvin to celsius
def k2c(k):
  return k - 273.15

# get temp from web API
def getTemp():
  api_key = '9fa3fb4430697b4e1df38a932096bdaa'
  base_url = 'http://api.openweathermap.org/data/2.5/weather?'
  city_name = 'melbourne'
  complete_url = base_url + 'appid=' + api_key + '&q=' + city_name

  response = requests.get(complete_url)
  x = response.json()

  if x['cod'] != '404':
    y = x['main']
    current_temperature = y['temp']
    return k2c(current_temperature)
  else:
    return 'City Not Found'

# route used by Flask to show the main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  title = 'Fan Controller'
  arduinoTemp = None
  arduinoFanStatus = None
  outsideTemp = getTemp()
  form = TempForm()
  form.tmepTreshold.data = ard.threshold
  return render_template( 'index.html', title=title, arduinoTemp=arduinoTemp, arduinoFanStatus=arduinoFanStatus, outsideTemp=outsideTemp, form=form )

# route used when button is clicked, the user never sees this
@app.route('/changeTempThreshold', methods=['GET', 'POST'])
def changeTempThreshold():
  if request.method == 'POST':
    tmepTreshold = request.form['tmepTreshold']
    try:
      ard.threshold = int( tmepTreshold )
    except:
      pass
  return redirect('/')

# run the app
# this if chechs to make sure this is the python file is the one that is being run
# this is one way to do testing
if __name__ == '__main__':
  app.run()
