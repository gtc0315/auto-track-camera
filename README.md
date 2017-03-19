# auto-track-camera
A camera that can physically track human face

Targets:
Raspberry pi model 3B (native Raspbian Jessie)
Arduino Uno

Raspberry will run the face detection algorithm and send encoded servo directions and speeds to 
the Arduino via GPIO pins. Raspberry also run the streaming module.

Arduino will decode the motor directions and speeds. It will use decoded data and PWM to control servos.

Steps to run the face tracking camera:
1. Create a local folder in Raspberry for storing the image.
2. Upload the Arduino code (auto-track-camera-servo.ino) to Arduino and provide power.
3. Modify the image path in both auto-track-camera.py and streaming.sh
4. Run auto-track-camera.py in a new Raspberry terminal by typing:
	$python /YOURPATH/auto-track-camera
5. Run streaming.sh in a new Raspberry terminal by typing:
	$./YOURPATH/streaming.sh
6. Push the button connected to the Arduino to enable auto tracking mode (LED will be on).
7. Watch live podcast with any mobile device that is in the same WiFi network as Raspberry.
   Go the link on the webbrower: http://RPiIPADDRESS:8080/stream.html
8. To reset the position of the camera, push the button connected to the Arduino to enable manual mode (LED will be off).
   Click the joystick. Follow step 6 to get back to tracking mode.
