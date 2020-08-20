#!/usr/bin/env python

# Modules
import asyncio
import asyncssh
import yaml
import json
import sys
import re
from getpass import getpass
from bin.visualiser import Topology

# Variables
path_inventory = 'inventory/inventory.yaml'
path_drawing = 'output/network.html'

# User-defined function
def get_creds(input_type):
    """
    This function collects the credentails to connect to the network elements.
    Input: source of collection: 'cli', 'file', or 'api' 
    """
    result ={}

    if input_type == 'cli':
        print('Please, provide the credentials for the network functions: ')
        result['user'] = str(input('Username > '))
        result['pass'] = getpass('Password > ')

    return result


def get_dict(file_path):
    """
    This function opens the external file in JSON or YAML format and imports the data as dictionary.
    Input: path to the file with the format YAML or JSON.
    """
    if re.match('^.*\.(yaml|yml)$', file_path):
        with open(file_path, 'r') as f:
            temp_dict = yaml.load(f.read(), Loader=yaml.FullLoader)

        return temp_dict

    elif re.match('^.*\.json$', file_path):
        with open(file_path, 'r') as f:
            temp_dict = json.loads(f.read())

        return temp_dict

    else:
        sys.exit('Wrong data type.')


async def ssh_to_device(host, creds):
    """
    This function runs the connects to the network functions over SSH in sync mode.
    Input: inventory entry(dict) and credentials(dict)
    """
    async with asyncssh.connect(host['ip_address'], username=creds['user'], password=creds['pass'],
                                known_hosts=None) as conn:
        result = await conn.run('net show lldp json', check=True)
        parsed_output = json.loads(result.stdout)
        parsed_output['host'] = host['hostname']

        return parsed_output


async def ssh_client(inv, creds):
    """
    This function creates a list of tasks launched in the async mode to the network functions.
    Input: inventory(dict) and credentials(dict)
    """
    print(f'Collecting info from {len(inv)} devices over SSH.')
    tasks = []

    for inv_entry in inv: 
        tasks.append(ssh_to_device(inv_entry, creds))

    output = await asyncio.gather(*tasks, return_exceptions=True)

    return output

# Body
if __name__ == '__main__':
    # Collecting input
    credentials = get_creds('cli')   
    inventory = get_dict(path_inventory)
    
    # Polling devices
    collected_data = asyncio.run(ssh_client(inventory, credentials))

    # Saving collected output to a file if necessary    
#    with open('output/results.json', 'w') as f:
#        f.write(json.dumps(collected_data, sort_keys=True, indent=4))

    print(f'Information is collected successfully from {len(collected_data)} devices.')

    # Reading the output from file if necessary
#    with open('output/results.json', 'r') as f:
#        collected_data = json.loads(f.read())

    # Building and visualing graph
    dc = Topology(collected_data)
    dc.buildGraph()
    dc.saveGraph(path_drawing)