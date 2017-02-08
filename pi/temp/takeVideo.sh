#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

raspivid -o /home/pi/camera/$DATE.h264 -t 60000
