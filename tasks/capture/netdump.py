import signal
import subprocess
import time
from typing import List, Optional

from netunicorn.base import Architecture, Failure, Node, Result, Success, Task, TaskDispatcher
from netunicorn.library.tasks.tasks_utils import subprocess_run

class StartCapture(TaskDispatcher):
    """
    Dispatcher for starting a network capture using tcpdump.
    """
    def __init__(self, filepath: str, arguments: Optional[List[str]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepath = filepath
        self.arguments = arguments or ["-i", "any"]

        self.linux_implementation = StartCaptureLinuxImplementation(
            filepath=self.filepath, arguments=self.arguments, *args, **kwargs
        )

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation
        raise NotImplementedError(f"StartCapture is not implemented for {node.architecture}")

class StartCaptureLinuxImplementation(Task):
    """
    Linux-specific implementation of the StartCapture task.
    """
    requirements = ["sudo apt-get install -y tcpdump"]

    def __init__(self, filepath: str, arguments: Optional[List[str]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepath = filepath
        self.arguments = arguments

    def run(self) -> Result:
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        cmd = ["tcpdump"] + self.arguments + ["-w", self.filepath]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        if (exit_code := proc.poll()) is None:
            return Success(proc.pid)

        output = (proc.stdout.read().decode("utf-8") + "\n" + proc.stderr.read().decode("utf-8")).strip()
        return Failure(f"Tcpdump terminated with return code {exit_code}: {output}")

class StopNamedCapture(TaskDispatcher):
    """
    Dispatcher for stopping a named tcpdump capture.
    """
    def __init__(self, start_capture_task_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_capture_task_name = start_capture_task_name
        self.linux_implementation = StopNamedCaptureLinuxImplementation(
            capture_task_name=self.start_capture_task_name, *args, **kwargs
        )

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation
        raise NotImplementedError(f"StopNamedCapture is not implemented for {node.architecture}")

class StopNamedCaptureLinuxImplementation(Task):
    """
    Linux-specific implementation of the StopNamedCapture task.
    """
    requirements = ["sudo apt-get install -y tcpdump", "sudo apt-get install -y procps"]

    def __init__(self, capture_task_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capture_task_name = capture_task_name

    def run(self):
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        pid_result = self.previous_steps.get(self.capture_task_name, [Failure("Named StartCapture not found")])[-1]
        if isinstance(pid_result, Failure):
            return pid_result

        pid = pid_result.unwrap()
        return subprocess_run(["kill", str(pid)])

class StopAllTCPDumps(TaskDispatcher):
    """
    Dispatcher for stopping all tcpdump processes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.linux_implementation = StopAllTCPDumpsLinuxImplementation(*args, **kwargs)

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation
        raise NotImplementedError(f"StopAllTCPDumps is not implemented for {node.architecture}")

class StopAllTCPDumpsLinuxImplementation(Task):
    """
    Linux-specific implementation of the StopAllTCPDumps task.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        return subprocess_run(["killall", "-w", "tcpdump"])
