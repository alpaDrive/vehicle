import obd

connection = obd.OBD("/dev/ttyUSB0")

while True:
    try:
        rpm = connection.query(obd.commands.RPM).value
        speed = connection.query(obd.commands.SPEED).value
        temperature = connection.query(obd.commands.COOLANT_TEMP).value
        odometer = connection.query(obd.commands.DISTANCE_SINCE_DTC_CLEAR).value

        print(f'Vehicle is travelling at a speed of {speed}. It has run {odometer} until last DTC code was cleared.')
        print(f'Engine is running at {rpm} at is {temperature}.')
    except:
        print("Something bad just happened. You have to debug more immediately!")