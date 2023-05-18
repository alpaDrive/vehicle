import serial
import pynmea2

ser = serial.Serial("/dev/ttyS0")

while True:
    line = ser.readline().decode('latin-1')  # Read a line of NMEA data and decode it
    if line.startswith('$GPGGA'):  # Example: Use GGA sentence for latitude and longitude
        data = pynmea2.parse(line)
        print(data)
        latitude = data.latitude
        longitude = data.longitude
        print("Latitude:", latitude)
        print("Longitude:", longitude)
