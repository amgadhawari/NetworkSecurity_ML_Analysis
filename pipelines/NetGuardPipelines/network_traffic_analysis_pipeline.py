# File: network_traffic_analysis_pipeline.py

from netunicorn.base import Pipeline
from netunicorn.library.tasks.capture.tcpdump import StartCapture, StopNamedCapture, AnalyzeCapture
from netunicorn.library.tasks.upload.fileio import UploadToFileIO

def network_traffic_analysis_pipeline() -> Pipeline:
    """
    Captures network traffic, analyzes it for congestion patterns, and uploads the capture file.
    :return: pipeline to run
    """
    pipeline = (
        Pipeline()
        .then(StartCapture(filepath="/tmp/traffic_capture.pcap", name="network_capture"))
        .then(AnalyzeCapture(start_capture_task_name="network_capture", analysis_type="congestion"))
        .then(StopNamedCapture(start_capture_task_name="network_capture"))
        .then(UploadToFileIO(filepath="/tmp/traffic_capture.pcap", expires="7d"))
    )
    return pipeline
