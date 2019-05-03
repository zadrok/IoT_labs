import serial

device = "/dev/ttyUSB0"
arduino = serial.Serial(device, 9600)
answers = []

def check_input():
    i = 0
    three_correct = False
    while  not (three_correct):
        data = arduino.readline()
        print(data)
        answer = arduino.readline()
        input = arduino.readline()
        print(input)
        if answer == input:
            print("Correct!")
            answers.insert(i, 1)
            print(answers[i])
        else:
            print("Wrong")
            answers.insert(i, 0)
        print(i)
        if i >= 3:
            if answers[i] + answers[i - 1] + answers [i - 2] == 3:
                three_correct = True
                Serial.write('1')
        i += 1

while True:
    check_input()