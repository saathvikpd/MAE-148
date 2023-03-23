# MAE-148

The run.py file, when run, will load our model (hosted on an API using RoboFlow) and begin detection. Once a basketball is detected in the frame, it will calculate an angle from the camera centerline to the ball and steer in that direction. Once it steers, it runs the motor for a while and inches in that direction. The pyvesc module is used to steer and throttle the car.

The 

