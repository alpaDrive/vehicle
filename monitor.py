import obd

class OBDInterface:
    def __init__(self, vehicle_id, message_sender):
        self.vehicle_id = vehicle_id
        self.message_sender = message_sender
        self.connection = obd.OBD('/dev/ttyUSB0')
        self.current_rpm = None
        self.current_speed = None

    async def start(self):
        # Start continuous monitoring of values
        self.connection.watch(obd.commands.RPM)
        self.connection.watch(obd.commands.SPEED)
        self.connection.start()

        while True:
            # Get current values
            rpm = self.connection.query(obd.commands.RPM).value
            speed = self.connection.query(obd.commands.SPEED).value

            # If values have changed, send broadcast message
            if rpm != self.current_rpm:
                self.current_rpm = rpm
                self.message_sender.send_message("broadcast", "RPM changed to {}".format(rpm))

            if speed != self.current_speed:
                self.current_speed = speed
                self.message_sender.send_message("broadcast", "Speed changed to {}".format(speed))
    
    def get_rpm(self):
        return self.connection.query(obd.commands.RPM).value

    def get_speed(self):
        return self.connection.query(obd.commands.SPEED).value
