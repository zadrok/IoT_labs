import serial

device = "/dev/ttyUSB0"
arduino = serial.Serial(device, 9600)

def check_input():
    score = 0
    data = arduino.readline()
    print(data)
    answer = arduino.readline()
    input = arduino.readline()
    print(input)
    if answer == input:
        print("Correct!")
        score+=1
        print("Score : ")
        print(score)
    else:
        print("Wrong!")

while True:
    check_input()
