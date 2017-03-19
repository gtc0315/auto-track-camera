# auto-track-camera
A camera that can track human face physically

In this project, I want to implement an autonomous facial tracking camera system that runs face tracking algorithm, motorize itself on a 2-DOF pan/tilt mechanism to face toward a person at all time, and streams the HD video to the connected laptop via Bluetooth. 

In current TV reality show, especially in South Korean, cameramen are widely used for recording assigned guests, my application can assist or even replace those cameramen. Also, the system can be implemented in humanoid robot application to imitate human eyes. The system can also replace the manual-controlled pan/tilt security camera to reduce the cost of security maintenance.

There were many projects around using pan/tilt camera and facial tracking. I believe that the uniqueness/difficulty of my project is that my camera can track a particular face using facial recognition and face tracking algorithms. The algorithms need to run in specified time constraints so that the entire tracking response can be made under several deciseconds to eliminate the delayed feeling observed by the human. 

Also, the pan/tilt camera around used mini servo motor that was easy to control and can run with the power from rpi pinouts but slow in movement. I will use the high-speed servo motors with PID control to achieve the fast response that system needs.

In my system, I will use the following hardware from Amazon
1.    Raspberry Pi camera module v2
2.    Two high-speed digital servo motors with the operating speed at ~0.15 sec/60 degree (5v)
3.    Standard U-shape mounting case (multiple)
4.    Breadboard for motor circuits
5.    H-bridge

The software I will implement are
1.    Face detection algorithm based on OpenCV
2.    Face recognition algorithm if it can be done in deciseconds time constraints
3.    Digital servo motor control (PID control)
4.    Feedback control loop for face tracking camera system
5.    Optimized scheduler for fast tracking response
6.    Video streaming via Bluetooth

Metrics of success:
1.    Tracking response less than a second
2.    Fluent and zero-delay user experience
3.    Streaming of HD video to laptop

I will run experiments to see how long do the facial recognition, and face tracking take to give an acceptable result. I will count the CPU time from the time of first image coming into CPU to the time pixel location of the face calculated. I will also find out if the pan/tilt system can reach the target location in several deciseconds. I will test the speed, and try PID control loop if the time limitation exceeds. I will test if camera tracking works, and count the time duration of the whole process. 

By the mid-project report, I will deliver the successful face detection algorithm, tracking system without time limitation constraints. Basic video streaming function will be implemented to visualize the tracking system.

My final project demo will be highly fluent face tracking with the zero-delay user experience. HD video streaming will be provided to simulate its application in TV reality show. The final report will include response time and time delay in three parts in the whole tracking system: face detection, pan/tilt mechanism, and video streaming.
