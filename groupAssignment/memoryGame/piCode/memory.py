import serial

device = "/dev/ttyUSB0"
arduino = serial.Serial(device, 9600)
answers = [] # create a list to store answers

def check_input():
    i = 0
    three_correct = False
    while  not (three_correct):
        data = arduino.readline()
        print(data)
        answer = arduino.readline() # get correct answer
        input = arduino.readline()  # get user input
        print(input)
        if answer == input:
            print("Correct!")
            answers.insert(i, 1)
        else:
            print("Wrong")
            answers.insert(i, 0)
        if (i >= 2):
            if (answers[i] + answers[i - 1] + answers [i - 2] == 3):
                three_correct = True
                return three_correct
        i += 1

while True:
    level_up = check_input()
    if (level_up):
        print("Starting level 2...")
        for i in range(1):
            arduino.write(b'y')
    level_three = check_input()
    if (level_three):
        print("Starting level 3...")
        for i in range(1):
            arduino.write(b'z')
    mario = check_input()
    if (mario):
        print("WINNER!!!")
            arduino.write(b'm')
    