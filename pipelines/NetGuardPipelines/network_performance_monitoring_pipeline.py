# File: network_performance_monitoring_pipeline.py

from netunicorn.base import Pipeline
from netunicorn.library.tasks.measurements.ping import ContinuousPing
from netunicorn.library.tasks.measurements.ookla_speedtest import SpeedTest

def network_performance_monitoring_pipeline() -> Pipeline:
    """
    Continuously monitors network performance using ping and speed tests.
    :return: pipeline to run
    """
    pipeline = (
        Pipeline()
        .then(ContinuousPing(target="www.example.com", interval=60))  # Pings every 60 seconds
        .then(SpeedTest())
    )
    return pipeline
