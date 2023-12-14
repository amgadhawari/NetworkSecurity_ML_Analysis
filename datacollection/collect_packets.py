import random
import json

def collect_packet_traces(output_file):
    """
    Simulate the collection of packet traces.
    Args:
    - output_file: File to store the collected packet traces
    """
    simulated_data = []
    for _ in range(500):  # Simulate 500 packet traces
        packet_trace = {
            "source_ip": f"192.168.1.{random.randint(1, 255)}",
            "destination_ip": f"10.0.0.{random.randint(1, 255)}",
            "source_port": random.randint(1024, 65535),
            "destination_port": random.randint(1024, 65535),
            "protocol": random.choice(["TCP", "UDP"]),
            "timestamp": f"{random.randint(1, 28)}/03/2022",
            "data_length": random.randint(40, 1500)  # In bytes
        }
        simulated_data.append(packet_trace)

    with open(output_file, 'w') as file:
        json.dump(simulated_data, file, indent=4)

collect_packet_traces('simulated_packet_traces.json')
