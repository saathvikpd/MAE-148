from roboflowoak import RoboflowOak
import cv2
import time
import numpy as np
from pyvesc import VESC
import subprocess
import os

# def steer(motor, angle):
#     # serial port that VESC is connected to. Something like "COM3" for windows and as below for linux/mac


#     # sweep servo through full range
# #     for i in range(100):
# #         time.sleep(0.01)
# #         motor.set_servo(i/100)
#     steer_input = (angle + 85) / 170
#     if steer_input < 0:
#         steer_input = 0
#     if steer_input > 1:
#         steer_input = 1

#     motor.set_servo(steer_input)

#     # IMPORTANT: YOU MUST STOP THE HEARTBEAT IF IT IS RUNNING BEFORE IT GOES OUT OF SCOPE. Otherwise, it will not
#     #            clean-up properly.
#     motor.stop_heartbeat()

# def throttle(rpm):
#     return None

serial_port = '/dev/ttyACM0'

motor = VESC(serial_port=serial_port)
print('motor detect')

# instantiating an object (rf) with the RoboflowOak module
rf = RoboflowOak(model="basketball-detection-s1n00", confidence=0.2, overlap=0.05,
version="1", api_key="2BobK1pwIsrmsOnyp12s", rgb=True,
depth=True, device=None, blocking=True)
# Running our model and displaying the video output with detections

# motor.set_duty_cycle(.)
print('model loaded')
for _ in range(1000):
    t0 = time.time()
    # The rf.detect() function runs the model inference
    result, frame, raw_frame, depth = rf.detect()
    predictions = result["predictions"]
    #{
    #    predictions:
    #    [ {
    #        x: (middle),
    #        y:(middle),
    #        width:
    #        height:
    #        depth: ###->
    #        confidence:
    #        class:
    #        mask: {
    #    ]
    #}
    #frame - frame after preprocs, with predictions
    #raw_frame - original frame from your OAK
    #depth - depth map for raw_frame, center-rectified to the center camera

    preds = [p.json() for p in predictions]

    bottom = (frame.shape[0] // 2, frame.shape[1])

    def dist(p1, p2):
        return (((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))**0.5
    
    mean_angle = 0
    
    break_ = False
    if len(preds) >= 1:
        for p in preds:
            x = p['x']
            y = p['y']

#             cv2.line(frame, (frame.shape[0] // 2, frame.shape[1]), (int(x), int(y)), color = (0, 0, 0), thickness = 1)

            adj = frame.shape[1] - y
            hyp = dist((x, y), bottom)
            cos = adj / hyp
            angle = np.arccos(cos)
            if x < bottom[0]:
                angle = -1 * angle 
            mean_angle += angle
        
        pred_size = preds[0]['width']
        frame_size = frame.shape[0]
        
        print('rel pred size', pred_size / frame_size)
        
        if (pred_size / frame_size) >= 0.3:
            break_ = True
        
        mean_angle = mean_angle / len(preds)
        
        mean_angle *= (180 / np.pi)
    
        steer_input = (mean_angle + 85) / 170
        if steer_input < 0:
            steer_input = 0
        if steer_input > 1:
            steer_input = 1
            
            
        
        #print("Firmware: ", motor.get_firmware_version())

    #     time.sleep(0.01)
   
        motor.set_duty_cycle(0.01)

        motor.set_servo(steer_input)
        # run motor and print out rpm for ~2 seconds
        for i in range(2):
            time.sleep(0.1)
            
            temp_var = None
            while temp_var == None:        
                try:
                    print(motor.get_measurements().rpm)
                    temp_var = 0
                except:
                    try:
                        os.system("$S")
                        motor = VESC(serial_port=serial_port)
                    except:
                        print('retrying')
        try:
            motor.set_rpm(0)
        except:
            continue
            
    temp_var = None
    while temp_var == None:        
        try:
            os.system("$S")
            motor = VESC(serial_port=serial_port)
            temp_var = 0
        except:
            print('retrying')
    if break_:
        break
#     os.system("$S")
#     motor = VESC(serial_port=serial_port)
        
#         motor.set_duty_cycle(
#         motor.set_rpm(100)
#         print(motor.get_rpm())
#         for i in range(30):
#             time.sleep(0.1)
#             print(motor.get_measurements().rpm)
#         motor.set_rpm(0)
#         
    # run motor and print out rpm for ~2 seconds
    
    
   

    print('Steering angle:', mean_angle)

    # timing: for benchmarking purposes
#         t = time.time()-t0
#         print("INFERENCE TIME IN MS ", 1/t)
#         print("PREDICTIONS ", preds)

    

#         cv2.line(frame, (frame.shape[0] // 2, frame.shape[1]), (frame.shape[0] // 2, 0), color = (0, 0, 0), thickness = 1)

#         cv2.putText(frame, str(mean_angle * 180 / np.pi) + " degrees", org = (0, 25), color = (0, 0, 0), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.7, thickness = 1)

#         # setting parameters for depth calculation
#         max_depth = np.amax(depth)
#         cv2.imshow("depth", depth/max_depth)
#         # displaying the video feed as successive frames
#         cv2.imshow("frame", frame)

#         # how to close the OAK inference window / stop inference: CTRL+q or CTRL+c
#     if cv2.waitKey(1) == ord('q'):
#         break

motor.stop_heartbeat()


