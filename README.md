# PASS - Preemption-aware Slice Scheduler

UNDER CONSTRUCTION

This repository contains scripts and results to use and test PASS. The system was tested in Ubuntu 16.04 with low-latency kernel. The scripts take into account most of these folders in the home folder of a user named `oai`. Exceptions are `bin`, that contains binary files that are considered to be in one of the system's `PATH` folder. 

The code used to validate PASS can be consulted here: <REPOSITORY_URL_TO_ADD>.



## bin

Files in `bin` folder should be copied to `/usr/local/bin` or similar. Otherwise, their calls in all script files must be updated, specifying the path where they are located. Other possibility is to add this folder to `PATH`.

**cell-docker** - Starts the docker container 

**run_enb** - Runs eNB.

**run_ue** - Runs UE. Mandatory argument with the number of nodes.

**start-pass-tracer** - Runs T tracer filtered to PASS related information. Mandatory argument is the file to output tracer information. 

**cell-setup** - Starts the UE (`/home/oai/ue_folder`) and eNB(`/home/oai/enb_folder`), and sends ssh command to start CN. 



## docker


The docker container is here to run the application servers to which the UEs are connected. A docker container was required as the container has not direct access to UE interfaces, otherwise there would be a problem with routes.

The docker container is initiated through `bin/cell-docker`.

For the current setup a `macvlan` network is required and is not initiated in the scripts. The network name should be `bridge-net`, and if the network is not `192.168.1.0/24` change `bin/cell-docker` accordingly. To create a docker `macvlan` network use:

``` 
docker network create -d macvlan \
  --subnet=<YOUR_NETWORK> \
  --gateway=<YOUR_GATEWAY \
  -o parent=<YOUR_INTERFACE_CONNECTED_TO_CN> bridge-net
```

In the dockerfile a `route add` command is inserted to add a route to the UEs through the CN. Adjust this command to fit your network settings.


## cell-client


This folder contains the master script to run the simulations as well as eNB configurations and the code to run in the UEs (that is the code containing the sockets that attach to UE interfaces).


