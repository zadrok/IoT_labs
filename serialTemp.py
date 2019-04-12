import serial
import MySQLdb

device = "/dev/ttyACM0"
arduino = serial.Serial(device,9600)
arduino.flushInput()

data = arduino.readline()
print(data)

dbConn = MySQLdb.connect('localhost','root','root','tempdb') or die("couldn't connect to the database")
print(dbConn)

with dbConn:
  cursor = dbConn.cursor()
  cursor.execute("INSERT INTO tempLog (Temprature) VALUES (%s)" % (data))
  dbConn.commit()
  cursor.close()
