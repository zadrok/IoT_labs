from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired
import requests, json
import serial

port = "/dev/ttyACM0"

# open the serial port to talk over
s1 = serial.Serial(port,9600)
# clean the serial port
s1.flushInput()

# create the Flask instance
app = Flask(__name__)
# set a key used for the form
app.config['SECRET_KEY'] = 'a-good-password'

# this class us used to interface with the Arduino
class Arduino:
  def __init__(self):
    self.city = 'melbourne'
    self.temp = None
    self.fanStatus = None
    self.threshold = 20

  def write(self,obj):
    s1.write(obj)

  def read(self):
    # make sure there is some data to read
    if s1.inWaiting():
      # there could be more then one message in the queue
      # not sure if this is how it works
      # but get most reacent message (i think, test!)
      while s1.inWaiting():
        # read the last message
        result = s1.read()
        # split into parts, each part having some of the data
        parts = result.split(', ')
        # for each of the datas
        for part in parts:
          # take data name and assign it to its value
          vals = part.split(':')
          if vals[0] is 'temp':
            self.temp = vals[1]
          elif vals[0] is 'fanStatus':
            self.fanStatus = vals[1]
          elif vals[0] is 'threshold':
            self.threshold = vals[1]
        print( 'temp: ' + str( self.temp ) + ', fanStatus: ' + str( self.fanStatus ) + ', threshold: ' + str( self.threshold ) )

    return self.temp, self.fanStatus, self.threshold

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
  arduinoTemp, arduinoFanStatus, arduinoThreshold = ard.read()
  outsideTemp = getTemp(ard.city)
  formTemp = TempForm()
  formTemp.tmepTreshold.data = arduinoThreshold
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
      ard.write( str( tmepTreshold ) )
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
  app.run(host='0.0.0.0')
