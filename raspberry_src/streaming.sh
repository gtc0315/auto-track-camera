#!/bin/bash
# script to run MJPG streamer
# change the path /home/pi/stream to the location that you save the image in the auto-track-camera.py

LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /home/pi/stream -n pic.jpg" -o "output_http.so -w /usr/local/www"
