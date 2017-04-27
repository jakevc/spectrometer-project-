import serial
import time
import numpy as np

'''This program runs the spectrometer made on an Arduinio Uno.
   First, a series of functions are defined to interface with the
   arduino serial monitor. Then a function that acts as the spectrometer
   program when run asks for what LED to use, then calculates the
   absorbance of a blank (cuvette with H20), the absorbance of a sample
   (iron o-phenanthroline was used here)'''

ser = serial.Serial('/dev/cu.usbmodemFA131', timeout=1)
# open the serial port interfacing with the Arduino Uno


def closePort():
    '''Closes the serial port'''
    ser.close()


def GLED():
    '''Waits one second, then turns on the green LED'''
    time.sleep(1)
    ser.write(b'G')


def RLED():
    '''Waits one second, then turns on the red LED'''
    time.sleep(1)
    ser.write(b'R')


def offLED():
    '''Waits one second, then turns off any on LED'''
    time.sleep(1)
    ser.write(b'F')


def measure():
    '''Takes a measurement on from the photoresistor on the Arduino'''
    ser.write(b'M')
    time.sleep(0.10)
    value = int(ser.readlines()[0])
    return value


# calucluate Po, P, Abs

def CalcAbs():
    ''' Takes difference in the intensity measurement from the
    photoresistor to calculate Po, P, the Absorbance of the Blank,
    and the Absorbance of the Sample'''

    print('Insert Blank')
    command = input('MeasureBlank!:(enter R or G)')
    if command == 'R':
        RLED()  # turn on the led wait, then measure
        time.sleep(0.5)
        iblank_on = measure()
        time.sleep(0.25)

        offLED()  # turn off the led then wait, then measure
        time.sleep(0.5)
        iblank_off = measure()
        time.sleep(0.25)
        Po = iblank_on - iblank_off
        BlankAbs = -np.log(Po/Po)
    elif command == 'G':
        GLED()
        time.sleep(0.5)
        iblank_on = measure()
        time.sleep(0.25)

        offLED()
        time.sleep(0.5)
        iblank_off = measure()
        time.sleep(0.25)
        Po = iblank_on - iblank_off
        BlankAbs = -np.log(Po/Po)
    else:
        print('You did not type R or G')

    print('Insert Sample')
    command = input('MeasureSample!:(enter R or G)')
    if command == 'R':
        RLED()
        time.sleep(0.5)
        isample_on = measure()
        time.sleep(0.25)

        RLED()
        time.sleep(0.5)
        isample_off = measure()
        time.sleep(0.25)

        P = isample_on - isample_off
        SampleAbs = -np.log(P/Po)

    elif command == 'G':
        GLED()
        time.sleep(0.5)
        isample_on = measure()
        time.sleep(0.25)

        GLED()
        time.sleep(0.5)
        isample_off = measure()
        time.sleep(0.25)

        P = isample_on - isample_off
        SampleAbs = -np.log(P/Po)
    else:
        print('You did not type R or G (CASE SENSITIVE)')
    return BlankAbs, SampleAbs

    closePort()  # make sure to close the serial port!


BlankAbs, SampleAbs = CalcAbs()
print('BlankAbs: ' + str(BlankAbs) + ', SampleAbs: '+str(SampleAbs))
