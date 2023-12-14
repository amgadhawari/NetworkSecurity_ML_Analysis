import json
import pandas as pd

def extract_features(packet_trace_file):
    """
    Extract features from packet traces.
    Args:
    - packet_trace_file: File containing packet trace data

    Returns:
    - DataFrame with extracted features
    """
    with open(packet_trace_file, 'r') as file:
        packet_traces = json.load(file)
    
    # Convert list of packet traces to DataFrame
    df = pd.DataFrame(packet_traces)

    # Additional feature extraction can be performed here

    return df


extracted_features = extract_features('simulated_packet_traces.json')
print(extracted_features.head())
