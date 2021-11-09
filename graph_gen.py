#!/usr/bin/python

import pefile
import sys
import argparse
import os
import pprint
import networkx
import re
from networkx.drawing.nx_agraph import write_dot
import collections
import json
from networkx.algorithms import bipartite

args = argparse.ArgumentParser("Darkside-BlackMatter Remote Server Network")
args.add_argument('target_path', help='directory with malware samples')
args.add_argument('output_file', help='file to write DOT file to')
args.add_argument('malware_projection', help='file to write DOT file to')
args.add_argument('server_projection', help='file to write DOT file to')
args = args.parse_args()
network = networkx.Graph()


# blackmatter C2_URLS, darkside C2_URL
def find_remote_server(json_file_path):
    result = []
    sample_config_json = json.loads(open(json_file_path, 'rb').read())
    remote_server_list = None
    
    if 'C2_URLS' not in sample_config_json and 'C2_URL' not in sample_config_json:
        return (0, set([]))
    
    if 'BLACK' in sample_config_json['RANSOM_NOTE'][0]['']:
        remote_server_list = sample_config_json['C2_URLS']
    else:
        remote_server_list = sample_config_json['C2_URL']
    for remote_server in remote_server_list:
        if len(remote_server['']) > 1:
            result.append(remote_server[''].replace('https://', '').replace('http://', ''))
    if 'BLACK' in sample_config_json['RANSOM_NOTE'][0]['']:
        return (1, set(result))
    
    return (0, set(result))
for root, dirs, files in os.walk(args.target_path):
    for path in files:
        if '.json' in path:
            full_path = os.path.join(root, path)
            is_blackmatter, remote_servers = find_remote_server(full_path)
            if len(remote_servers):
                color = ''
                if is_blackmatter:
                    color = 'red'
                else:
                    color = 'blue'
                network.add_node(path, label=path[:32], color=color, penwidth=5, bipartite=0)
            for remote_server in remote_servers:
                network.add_node(remote_server, label=remote_server, color='green', penwidth=10, bipartite=1, shape='diamond')
                network.add_edge(remote_server, path, penwidth=2)
write_dot(network, args.output_file)
malware = set(n for n,d in network.nodes(data=True) if d['bipartite'] == 0)
remote_server = set(network) - malware

malware_network = bipartite.projected_graph(network, malware)
remote_server_network = bipartite.projected_graph(network, remote_server)

write_dot(malware_network, args.malware_projection)
write_dot(remote_server_network, args.server_projection)