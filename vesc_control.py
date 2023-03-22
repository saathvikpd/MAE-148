from pyvesc import VESC
import time

def steer(angle):
    # serial port that VESC is connected to. Something like "COM3" for windows and as below for linux/mac
    serial_port = '/dev/ttyACM0'

    motor = VESC(serial_port=serial_port)
    print("Firmware: ", motor.get_firmware_version())

    # sweep servo through full range
#     for i in range(100):
#         time.sleep(0.01)
#         motor.set_servo(i/100)
    steer_input = (angle + 85) / 170
    if steer_input < 0:
        steer_input = 0
    if steer_input > 1:
        steer_input = 1
        
    motor.set_servo(steer_input)

    # IMPORTANT: YOU MUST STOP THE HEARTBEAT IF IT IS RUNNING BEFORE IT GOES OUT OF SCOPE. Otherwise, it will not
    #            clean-up properly.
    motor.stop_heartbeat()
    
def throttle(rpm):
    return None
    