# Robot-Controller

This repo is the main software repo for the project

# Table of Contents
1. [Overview](#overview)
2. [Setup and Materials Required](#setup-and-materials-required)
3. [Computer Vision](#computer-vision)
4. [Controller](#controller)
5. [Visualizer](#visualizer)
6. [Motion Planner](#motion-planner)
7. [Future Work](#future-work)


## Overview

This project was attempted for our ECE capstone 2022 at Carnegie Mellon by Saral Tayal, Prithu Pareek, and Omkar Savkur

This project won Apple's best project award. Given that the members of the project have since graduated, the project will no longer be maintained by the original members, however, anyone is welcome to make a pull request and we would love to include community contributions to this project.

This project dosen't require power compute. Thanks to our efforts in optimizing the algorithms and parallizing the sense-plan-act loop, the code-base runs well on low-end machines. We achieved ~15fps on a base model, fanless, 2020 MacBook Air that had to translate x86 instructions to ARM. Running on a well-specced 2019 16" MacBook Pro and 2019 XPS-15 didn't yield noticable improvements to performance. 

The project has various constants to tune the various parts of the algorithms in the constants.py file. Anyone attempting this project should familiarize themselves with the contents of the files and what each of those constants do.

## Setup and Materials Required

The project requires both Python and C++. The path planner algorithms run in C++ and the rest of the code-base runs in Python. Pybind is used as a bridge between C++ and Python.

One important note is that the codebase uses the opencv-contrib version of the opencv python libraries instead of the regular opencv.

In terms of physical materials, one will need to either build robots per our open-source design or use off-the-shelf robots and modify the codebase to support it. One will also need to create ferous 'pallets' via some sort of sheet metal. Additionally, aruco markers will need to be printed and afixed to the robots and the ferous pallets.

Lastly one will need some sort of a webcam (or iPhone with Continuity Camera) for the vision side of the project

## Computer Vision

More details on the algorithmic design of the comptuer vision system can be found in the paper linked at the top of the Readme. Upon reading the codebase, one will see that the codebase still has support for running the computer vision localization system via the neopixel LEDs and an inverse-affine-transformation. While this functionality exists, the codebase was optimized to use the Aruco Markers. There is also a computer vision debug flag in the constants file which will output images from various parts of the algorithm to help debug any issues one might encounter. 

## Controller

The controller's job is to interpolate the discrete steps outputed by the path planner into smooth continous time for the robots such that the controlelr can correct for errors regardless on where the robot is at any arbitary timestep. This is done with cubic hermite spine interpolation. One can find some helper diagrams, and simulation code in the controllerFragments folder of the repo

## Visualizer
The visualizer is a function within the computer vision part of the codebase. The visualizer will show the current pose of the robot, the control commands from the controller to close any error, and the paths outputed by the path planner for the robots. Do note that the visualizer is computationally expensive and disabling it does improve performance a little bit. However, the visualizer provided enough value to us that it was worth the slight performance hit we encountered.

## Motion Planner
The motion planner is the one part of the codebase that is written in C++, the implementation for it can be found within the src folder of the repo. The planner was implemented using a 4D state-space A* search and more information on its design can be found in our research paper

## Future Work

Creators of the project,

Sridhar (Bobby Bash)
Harshavardhan 
Magunthan 