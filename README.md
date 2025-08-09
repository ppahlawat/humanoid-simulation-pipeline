Humanoid Perception and Interaction Project (ROS 2 Humble)
This ROS 2 workspace contains a collection of packages that build a complete perception-to-action pipeline for a simulated humanoid robot. The project progresses from fundamental ROS 2 concepts to a final system where the robot visually detects objects in a Gazebo simulation and performs a gesture in response.

Project Overview
The primary goal of this project is to simulate a humanoid robot that can:

Observe its environment using a simulated camera in Gazebo.

Process the visual feed using OpenCV to detect red, green, or blue objects.

Determine if an object is "close" based on its size in the camera's view.

Send a trigger message when a close object is detected.

React to the trigger by performing a "nodding" gesture, visualized in RViz.

Packages in this Workspace
This workspace is structured into several packages, each with a specific role.

Core Humanoid Packages
humanoid_description: (C++) Contains the URDF/XACRO model of the humanoid robot, including its physical links, joints, and simulated sensors (Camera, IMU).

humanoid_perception: (Python) The vision processing package. It contains the node that subscribes to the camera feed, uses OpenCV to detect colored objects, and publishes their position and a proximity trigger.

humanoid_final_control: (Python) The motion control package. It contains the node that subscribes to the perception trigger and publishes JointState messages to animate the robot's gesture in RViz.

Learning & Foundational Packages
my_py_pkg: A basic Python package containing simple publisher and subscriber nodes, used for learning core ROS 2 concepts.

my_sensor_package: A package demonstrating how to work with simulated sensor data.

my_robot_bringup: A package used for learning how to use ROS 2 launch files to start multiple nodes at once.

Prerequisites
Ubuntu 22.04

ROS 2 Humble

Gazebo Simulator (ros-humble-gazebo-ros-pkgs)

OpenCV for Python (opencv-python)

Build Instructions
To build all the packages in this workspace, navigate to the root directory (ros2_ws) and run the following command:

cd ~/ros2_ws
colcon build

How to Run the Final Project
To run the complete, end-to-end simulation, you only need to run a single master launch file.

Source the workspace:

source install/setup.bash

Run the final launch file:

ros2 launch humanoid_final_control final_pipeline.launch.py

RViz First-Time Setup
When RViz opens for the first time, you will need to configure the display to see the robot and the camera feed.

Set the Fixed Frame: In the Displays panel on the left, find the Global Options. Change the Fixed Frame from map to torso_link.

Add the Robot Model:

Click the Add button at the bottom-left.

Select RobotModel from the list and click OK. You should now see your humanoid model. Change Description topic to /robot_description

Add the Camera Feed:

Click the Add button again.

Select Image from the list and click OK.

In the Displays panel, expand the new Image topic.

Change the Topic to /humanoid/color_detection/processed_image. You will now see the processed video feed from the robot's camera.