import serial
import MySQLdb

device = "/dev/ttyACM0"
arduino = serial.Serial(device,9600)
arduino.flushInput()

data = arduino.readline()
print(data)

dbConn = MySQLdb.connect('localhost','root','tempdb') or die("couldn't connect to the database")
print(dbConn)

while dbConn:
  cursor = dbConn.cusor()
  cursor.execute("INSERT INTO tempLog (Temprature) VALUES (%s)" % (data))
  dbConn.commit()
  cursor.close()
