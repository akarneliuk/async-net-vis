#!/usr/bin/env python

# Modules
import networkx
from pyvis.network import Network
import re
import logging

# Classes
class Topology(object):
    """
    This class builds the topology graph using networkx module
    and visualise it using visjs
    """
    def __init__(self, raw):
        self.__raw = raw
        self.__G = networkx.Graph(label='Data Centre', title='Data Plane')

        logging.info('Visualiser object created')

    def buildGraph(self):
        for node_entry in self.__raw:
            if re.match('^H.*', node_entry['host']):
                group = 1
                image = 'https://karneliuk.com/wp-content/uploads/2020/08/ka-vis-server-338.png'
                descr = 'host'
            elif re.match('^L.*', node_entry['host']):
                group = 2
                image = 'https://karneliuk.com/wp-content/uploads/2020/08/ka-vis-switch-300.png'
                descr = 'leaf'
            elif re.match('^S.*', node_entry['host']):
                group = 3
                image = 'https://karneliuk.com/wp-content/uploads/2020/08/ka-vis-switch-300.png'
                descr = 'spine'
            elif re.match('^E.*', node_entry['host']):
                group = 4
                image = 'https://karneliuk.com/wp-content/uploads/2020/08/ka-vis-switch-300.png'
                descr = 'border'
            elif re.match('^I.*', node_entry['host']):
                group = 5
                image = 'https://karneliuk.com/wp-content/uploads/2020/08/ka-vis-router-300.png'
                descr = 'router'
            else:
                group = 6
                image = None
                descr = 'Not recornized'

            shape = 'image' if image else 'circle'

            self.__G.add_node(node_entry['host'], label=node_entry['host'], title=descr,
                              group=group, shape=shape, image=image, level=group)

        for node_entry in self.__raw:
            for link_entry in node_entry['lldp'][0]['interface']:
                if not link_entry['chassis'][0]['name'][0]['value'] in self.__G.adj[node_entry['host']] and link_entry["name"] != 'eth0':
                    self.__G.add_edge(node_entry['host'], link_entry['chassis'][0]['name'][0]['value'], 
                                      title=f'{link_entry["name"]} - {link_entry["port"][0]["id"][0]["value"]}')

    def saveGraph(self, target_file):
        nt = Network(height="700px", width="1000px", heading='Connectivity map', layout=True)
        nt.from_nx(self.__G)
        nt.show(target_file)