import json
import trex_controller

def main:
	trex = TRexController(trex_server_ip = 192.168.122.117)
	
	trex_command = {'command' : 'start', 'flow': 'flow1', 'rate': 100}
	
	trex.parseCommand(json_object = json.dumps(trex_command))
	