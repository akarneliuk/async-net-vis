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
import logging
import os


# Variables
path_inventory = 'inventory/inventory.yaml'
path_drawing = 'output/network.html'
path_log = 'log/execution.log'
path_temp = 'output/results.json'


# User-defined function
def get_creds(input_type):
    """
    This function collects the credentails to connect to the network elements.
    Input: source of collection: 'cli', 'file', or 'api' 
    """
    logging.info('Collecting credentials...')
    result ={}

    if input_type == 'cli':
        print('Please, provide the credentials for the network functions: ')
        result['user'] = str(input('Username > '))
        result['pass'] = getpass('Password > ')

    logging.info('Credentials are collected.')
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
        logging.error('The input variables has wrong data type.')
        sys.exit(1)


async def ssh_to_device(host, creds):
    """
    This function runs the connects to the network functions over SSH in sync mode.
    Input: inventory entry(dict) and credentials(dict)
    """
    try:
        async with asyncssh.connect(host['ip_address'], username=creds['user'], password=creds['pass'],
                                    known_hosts=None) as conn:
            result = await conn.run('net show lldp json', check=True)
            parsed_output = json.loads(result.stdout)
            parsed_output['host'] = host['hostname']

            logging.info(f'Polling from {host["ip_address"]} SUCCEEDED.')
            return parsed_output

    except:
        logging.error(f'Polling from {host["ip_address"]} FAILED.')


async def ssh_client(inv, creds):
    """
    This function creates a list of tasks launched in the async mode to the network functions.
    Input: inventory(dict) and credentials(dict)
    """
    logging.info(f'Collecting info from {len(inv)} devices over SSH...')
    tasks = []

    for inv_entry in inv: 
        tasks.append(ssh_to_device(inv_entry, creds))

    output = await asyncio.gather(*tasks, return_exceptions=True)

    return output

# Body
if __name__ == '__main__':
    # Setting logging
    if not os.path.exists(path_log.split('/')[0]):
        os.mkdir(path_log.split('/')[0])

    logging.basicConfig(filename=path_log, level=logging.INFO, format='%(asctime)s.%(msecs)03dZ,%(levelname)s,%(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
    logging.info('Starting application...')

    # Collecting input
    credentials = get_creds('cli')   
    inventory = get_dict(path_inventory)
    
    # Polling devices
#    logging.info('Starting polling data from devices...')
#    collected_data = asyncio.run(ssh_client(inventory, credentials))

#    logging.info(f'Information is collected successfully from {len(collected_data)} devices.')

    # Saving collected output to a file if necessary
 #   logging.info(f'Saving the collected data into {path_temp}...')
 #   with open(path_temp, 'w') as f:
 #       f.write(json.dumps(collected_data, sort_keys=True, indent=4))

#    logging.info(f'File {path_temp} is saved succesfully.')

    # Reading the output from file if necessary
    logging.info(f'Reading data from {path_temp}...')
    try:
        with open(path_temp, 'r') as f:
            collected_data = json.loads(f.read())

        logging.info(f'Data from {path_temp} is imported successfully.')

    except:
        logging.error(f'The import from {path_temp} FAILED.')
        sys.exit(1)

    # Building and visualing graph
    dc = Topology(collected_data)
    dc.buildGraph()
    dc.saveGraph(path_drawing)

    logging.info('The execution is complete successfully')