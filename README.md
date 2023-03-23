# MAE-148

The run.py file, when run, will load our model (hosted on an API using RoboFlow) and begin detection. Once a basketball is detected in the frame, it will calculate an angle from the camera centerline to the ball and steer in that direction. Once it steers, it runs the motor for a while and inches in that direction. The pyvesc module is used to steer and throttle the car.

The 148remote/ folder has some code for our camera mount. The camera mount is controlled using an arduino board. Th script in that file gets the mount to do a cool head nod and also allows remote control of the camera's angle.

Team 6:
Saathvik Dirisala
Victor Chen
Yang Song
