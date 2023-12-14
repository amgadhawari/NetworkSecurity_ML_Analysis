import pandas as pd
import os
from scapy.all import rdpcap, Packet
from typing import List

class NetworkDataAnalyzer:
    """
    Analyze network data captured by tcpdump.
    """

    def __init__(self, capture_file_path: str):
        self.capture_file_path = capture_file_path

    def _parse_packets(self) -> List[Packet]:
        """
        Parse packets from the capture file.
        """
        if not os.path.exists(self.capture_file_path):
            raise FileNotFoundError(f"Capture file not found: {self.capture_file_path}")
        
        packets = rdpcap(self.capture_file_path)
        return packets

    def analyze_traffic(self):
        """
        Analyze the network traffic from the captured data.
        """
        packets = self._parse_packets()

        # Example analysis: Count packets by protocol
        protocol_counts = {}
        for packet in packets:
            protocol = type(packet).__name__
            protocol_counts[protocol] = protocol_counts.get(protocol, 0) + 1

        return protocol_counts

    def save_analysis_report(self, report_path: str):
        """
        Save the analysis report to a file.
        """
        traffic_data = self.analyze_traffic()
        df = pd.DataFrame(list(traffic_data.items()), columns=['Protocol', 'Count'])
        df.to_csv(report_path, index=False)
        print(f"Analysis report saved to: {report_path}")

# Example Usage
analyzer = NetworkDataAnalyzer('/path/to/capture_file.pcap')
analyzer.save_analysis_report('/path/to/analysis_report.csv')
