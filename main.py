##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 
import pyfirmata
import time

##Define variables
GreenLEDoutput = 13         ##define digital output PIN
RedLEDoutput = 14           ##define digital output PIN
Buttoninput = 10            ##define digital input PIN
Sensorinput = 5             ##define analog input PIN
state = False               ## state variable for the while loop
write_to_file_path = "datavalues.txt"   ##create outputfile
output_file = open(write_to_file_path, "w+");   ##open output file

board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)             ##assigns an iterator that will be used to read the status of the inputs of the circuit.
it.start()                                      ##starts the iterator, which keeps a loop running in parallel with your main code. The loop executes board.iterate() to update the input values obtained from the Arduino board.
board.digital[Buttoninput].mode = pyfirmata.INPUT        ##sets buttoninput as a digital input with pyfirmata.INPUT
board.analog[Sensorinput].mode = pyfirmata.INPUT

output_file = open(write_to_file_path, "w+");   ##open output file


def readbutton():
    buttonstate = board.digital[Buttoninput].read()
    return buttonstate

def indicateinprocess():
    board.digital[GreenLEDoutput].write(0)
    board.digital[RedLEDoutput].write(1)

def indicatereadytostart():
    board.digital[GreenLEDoutput].write(1)
    board.digital[RedLEDoutput].write(0)
    
def readsensorvalues():
    sensorvalue = board.analog[Sensorinput].read()
    print(sensorvalue)
    return sensorvalue
    
def writetooutputfile(sensorvalue):
    output_file.write(sensorvalue);
    

while True:
    while(state == False):
        if(readbutton() == 1):
            indicatereadytostart()
            state = True
    while(state == True):
        indicateinprocess()
        sensorvalue = readsensorvalues()
        writetooutputfile(sensorvalue)
        if(readbutton() == 1):
            state = False
        
        
