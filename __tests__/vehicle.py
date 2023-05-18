import obd

connection = obd.OBD("/dev/ttyUSB0")

while True:
    try:
        rpm = connection.query(obd.commands.RPM).value.magnitude
        speed = connection.query(obd.commands.SPEED).value.magnitude
        temperature = connection.query(obd.commands.COOLANT_TEMP).value.magnitude
        odometer = connection.query(obd.commands.DISTANCE_SINCE_DTC_CLEAR).value.magnitude

        print(rpm, speed, temperature, odometer)

    except KeyboardInterrupt:
        quit()
    except Exception as e:
        print("Something bad just happened. You have to debug more immediately!")
        print(e)