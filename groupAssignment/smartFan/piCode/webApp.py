from flask import Flask, render_template, redirect, request, current_app, g
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired
import requests, json
import serial
import sqlite3 as sql
import datetime

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

  def write(self,value):
    value = str( value )
    s1.write( str( value + '\r' ).encode() )

  def read(self):
    # make sure there is some data to read
    if s1.inWaiting():
      # there could be more then one message in the queue
      # not sure if this is how it works
      # but get most reacent message (i think, test!)
      while s1.inWaiting():
        # read the last message
        result = str( s1.readline() )[2:-5]
        # split into parts, each part having some of the data
        # print( 'serial string: ' + result )
        parts = result.split(', ')
        # for each of the datas
        for part in parts:
          # print( 'part: ' + part )
          # take data name and assign it to its value
          vals = part.split(':')
          # print( 'vals: ' + vals[0] + ' ' + vals[1] )
          if vals[0] == 'temp':
            # print( 'vals is temp' )
            if 't' not in vals[1]:
              self.temp = float(vals[1])
          elif vals[0] == 'fanStatus':
            # print( 'vals is fanStatus' )
            self.fanStatus = True if int(vals[1]) > 0 else False
          elif vals[0] == 'threshold':
            # print( 'vals is threshold' )
            self.threshold = float(vals[1])
        # print( 'local memory: ' + 'temp: ' + str( self.temp ) + ', fanStatus: ' + str( self.fanStatus ) + ', threshold: ' + str( self.threshold ) )

    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("INSERT INTO temps (temp,date) VALUES (?,?)",(self.temp,datetime.datetime.now()) )
    conn.commit()
    return self.temp, self.fanStatus, self.threshold

# instace of Arduino class
ard = Arduino()

# class for the form to change the city
class CityForm(FlaskForm):
  city = StringField('C I T Y', validators=[DataRequired()])
  submit = SubmitField('Submit')


# class for the form to change temp threshold
class TempForm(FlaskForm):
  tempTreshold = DecimalField('Temperature Threshold', validators=[DataRequired()])
  submit = SubmitField('Submit')


def getDBConnection():
  conn = sql.connect('database.db')
  conn.execute('CREATE TABLE if not exists temps (temp REAL, date TEXT)')
  return conn


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
  formTemp.tempTreshold.data = arduinoThreshold
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
    tempTreshold = request.form['tempTreshold']
    try:
      # try and change value
      # probably don't need the try catch for our needs here
      # but goot to make sure value ented into form is an int
      ard.write( tempTreshold )
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


@app.route('/list')
def list():
  conn = getDBConnection()
  conn.row_factory = sql.Row
  cur = conn.cursor()
  cur.execute("select * from temps")
  rows = cur.fetchall();
  # return the webpage and pass it all of the information
  return render_template( 'list.html', rows=rows )


# run the app
# this if chechs to make sure this is the python file is the one that is being run
# this is one way to do testing
if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')
