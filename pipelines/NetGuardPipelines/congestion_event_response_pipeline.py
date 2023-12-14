# File: congestion_event_response_pipeline.py

from netunicorn.base import Pipeline
from netunicorn.library.tasks.capture.tcpdump import StartCapture, StopNamedCapture
from netunicorn.library.tasks.network_management import AdjustBandwidth

def congestion_event_response_pipeline() -> Pipeline:
    """
    Responds to network congestion by adjusting bandwidth.
    :return: pipeline to run
    """
    pipeline = (
        Pipeline()
        .then(StartCapture(filepath="/tmp/congestion_event.pcap", name="congestion_capture"))
        .then(AdjustBandwidth(new_bandwidth_limit="100mbps"))  # Adjust bandwidth to 100mbps
        .then(StopNamedCapture(start_capture_task_name="congestion_capture"))
    )
    return pipeline
