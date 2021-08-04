#!/bin/bash
cp -r banana blue_box cat_picture green_box pizza red_box walls ~/.gazebo/models
sudo cp *.launch /opt/ros/melodic/share/turtlebot3_gazebo/launch/
sudo cp *.world /opt/ros/melodic/share/turtlebot3_gazebo/worlds/
echo "-----done------"
