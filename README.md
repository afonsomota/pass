# PASS - Preemption-aware Slice Scheduler

This repository contains scripts and results to use and test PASS. The system was tested in Ubuntu 16.04 with low-latency kernel. The scripts take into account most of these folders in the home folder of a user named `oai`. Exceptions are `bin`, that contains binary files that are considered to be in one of the system's `PATH` folder. 

The code used to validate PASS can be consulted here: <REPOSITORY_URL_TO_ADD>.


bin
---

Files in `bin` folder should be copied to `/usr/local/bin` or similar. Otherwise, their calls in all script files must be updated, specifying the path where they are located. Other possibility is to add this folder to `PATH`. 



docker
------

Change Dockerfile for the right route and IP address
