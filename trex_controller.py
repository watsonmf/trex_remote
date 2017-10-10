
from .trex_stl_lib.api import *


class TRexController(object):
	"""
		Basic controller object to integrate a TRex client with the Stateless Infrastructure Controller.
	"""
	
	def __init__(self, trex_server_ip = '127.0.0.1'):
		self.trex_client = STLClient(server = trex_server_ip)
		self.flows  = {"flow1": TCPFlow(trex_client = self.trex_client, 
													tx_port = 0, rx_port = 1,
													client_ip = "19.0.0.1",
													client_port = 19000,
													server_ip = "19.0.0.19",
													server_port = 19019),
							"flow2": TCPFlow(trex_client = self.trex_client, 
													tx_port = 2, rx_port = 3,
													client_ip = "19.0.1.1",
													client_port = 19100,
													server_ip = "19.0.1.19",
													server_port = 19119) }
		
		
	def __startFlow(self, flow: TCPFlow, rate = 1, force = False):
		flow.setupFlow()
		
		self.trex_client.add_streams(flow.getFlow, ports = flow.tx_port)
		self.trex_client.start(ports = flow.tx_port, mult = "%dmbps" % rate)
	
	def __updateFlow(self, flow: TCPFlow, rate):
		self.trex_client.update(ports = flow.tx_port, mult = "%dmbps" % rate)
	
	def __stopFlow(self, flow: TCPFlow):
		self.trex_client.stop(ports = [flow.tx_port, flow.rx_port])
	
	def parseCommand(self, json_object):
		pass
	
	
	
class TCPFlow(object):
	frame_size = 9000
	
	def __init__(self, trex_client, tx_port, rx_port, client_ip, client_port, server_ip, server_port):
		self.trex_client = trex_client
		self.tx_port = tx_port
		self.rx_port = rx_port
		self.client_ip = client_ip
		self.client_port = client_port
		self.server_ip = server_ip
		self.server_port = server_port
	
	def setupFlow(self):
		syn_pkt  = Ether()/IP(src=self.client_ip, dst=self.server_ip)/
							TCP(sport=self.client_port, dport=self.server_port, flags="S", seq=100)
		syn_ack_pkt = Ether()/IP(src=self.server_ip, dst=self.client_ip)/
							TCP(sport=self.server_port, dport=self.client_port, flags="SA", seq=101)
		ack_pkt = Ether()/IP(src=self.client_ip, dst=self.server_ip)/
							TCP(sport=self.client_port, dport=self.server_port, flags="PA", seq=102)
		
		self.trex_client.reset(ports=[self.tx_port, self.rx_port])
		
		self.trex_client.push_packets(ports = self.tx_port, pkts = syn_pkt)
		self.trex_client.wait_on_traffic(ports = self.tx_port)
		
		self.trex_client.push_packets(ports = self.rx_port, pkts = syn_ack_pkt)
		self.trex_client.wait_on_traffic(ports = self.rx_port)
		
		self.trex_client.push_packets(ports = self.tx_port, pkts = ack_pkt)
		self.trex_client.wait_on_traffic(ports = self.tx_port)
	
	
	def getFlow():
		pkt_header = Ether()/IP(src=self.client_ip, dst=self.server_ip)/TCP(sport=self.client_port,dport=self.server_port, seq=200)
		
		data_length = frame_size - len(data_pkt)
		packet_data = "\x00" * data_length
		
		data_packet = STLPktBuilder(pkt = pkt_header/packet_data)
		
		return STLStream(packet = data_packet, mode = STLTXCont(pps = 100))