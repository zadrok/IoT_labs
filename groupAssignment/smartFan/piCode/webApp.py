from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
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
    self.city = 'melbourne'

# instace of Arduino class
ard = Arduino()

# class for the form to change the city
class CityForm(FlaskForm):
  city = StringField('City', validators=[DataRequired()])
  submit = SubmitField('Submit')

# class for the form to change temp threshold
class TempForm(FlaskForm):
  tmepTreshold = DecimalField('Temperature Threshold', validators=[DataRequired()])
  submit = SubmitField('Submit')

# covert the temp received from API from kelvin to celsius
def k2c(k):
  return k - 273.15

# get temp from web API
def getTemp(city):
  api_key = '9fa3fb4430697b4e1df38a932096bdaa'
  base_url = 'http://api.openweathermap.org/data/2.5/weather?'
  complete_url = base_url + 'appid=' + api_key + '&q=' + city

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
  # collect all information to show to user
  title = 'Fan Controller'
  arduinoTemp = None
  arduinoFanStatus = None
  outsideTemp = getTemp(ard.city)
  formTemp = TempForm()
  formTemp.tmepTreshold.data = ard.threshold
  formCity = CityForm()
  formCity.city.data = ard.city
  # return the webpage and pass it all of the information
  return render_template( 'index.html', title=title, arduinoTemp=arduinoTemp, arduinoFanStatus=arduinoFanStatus, outsideTemp=outsideTemp, formTemp=formTemp, formCity=formCity )

# route used when button to submit temp threshold is clicked, the user never sees this
@app.route('/changeTempThreshold', methods=['GET', 'POST'])
def changeTempThreshold():
  # make sure this has been accessed from a POST
  # form submited
  if request.method == 'POST':
      # grab data from form
    tmepTreshold = request.form['tmepTreshold']
    try:
      # try and change value
      # probably don't need the try catch for our needs here
      # but goot to make sure value ented into form is an int
      ard.threshold = int( tmepTreshold )
    except:
      pass
  # return the user to the main page
  return redirect('/')

# route used when button to submit city is clicked, the user never sees this
@app.route('/changeCity', methods=['GET', 'POST'])
def changeCity():
  # make sure this has been accessed from a POST
  # form submited
  if request.method == 'POST':
    # grab data from form
    city = request.form['city']
    try:
      # try and change value
      # probably don't need the try catch for our needs here
      ard.city = str( city )
    except:
      pass
  # return the user to the main page
  return redirect('/')

# run the app
# this if chechs to make sure this is the python file is the one that is being run
# this is one way to do testing
if __name__ == '__main__':
  app.run()
