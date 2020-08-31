# Efficient Network Functions Management
Collection and visualisation of the information collected from the network functions is a crucial component of the network operation. This repository contains a demo consisting of two components: 
- SSH client written leveraging the coroutine and AsyncIO framework. The intention is to optimise the performance of the network management application in a way more efficient to threading and much more efficient that a linear code. 
- Construction of the network graph and its visualisation into an interactive webpage.

## Requirements
### Python
Created and tested in Python 3.7

### Used libraries
- asyncio
- asyncssh
- pyvis
- networkx
- pyyaml

## Supported platforms
### Currently
- Cumulus Linux `{'nos': 'cumulus'}`

### Work in progress
- Arista EOS
- Nokia SRL
- Microsoft Azure SONiC
- Nokia SR OS
- Cisco IOS XR

## Usage
1. Install the modules from `requirements.txt` using `pip`.
2. Modify the `inventory.yaml` file inside the `inventory` directory per your topology.
3. Execute the script as `./main.py`.
4. Open in the `output` directory file `network.html` to watch your topology based on LLDP.

## License
[By using this product you accept the license agreement](LICENSE)

## Want to automate networks like profi?
If you want to learn how to create such a Python program (and many others), [join our netwotk automation training](http://bit.ly/2mP3SJy) 

## Dev Log
Release `0.3.0`:
- A visualisation now is done in a structured scheme rather than chaotic and using device-specific icons.
- The execution of the script is now logged and stored. The log file is stored across multiple executions.
- Minor bug fixing.

Release `0.2.1`:
- Minor bug fixing.

Release `0.2.0`:
- Added functionality of building topology using networkx (for modelling) and pyvis for (visualisation).

Release `0.1.0`:
- First release
