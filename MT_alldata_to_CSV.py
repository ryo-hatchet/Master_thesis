import serial
import re
import csv
from getch import getch, pause

ser = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=1)
f = open('./time_pa/time_and_pa_slow.csv', 'w')
writer = csv.writer(f)
data = []
time = []
sensor = []
def main():
    #ser.write("*".encode())
    while True:
        data = ser.readline().decode('utf-8')
        data = data.strip().split(",")
        if(len(data) > 0):
            print(data)
            writer.writerow(data)

    ser.close()
    f.close()

if __name__== "__main__":
    main()