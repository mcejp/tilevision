import argparse
from dataclasses import dataclass
from io import StringIO
import logging
import sys
from threading import Condition, Thread
import time

from .tilevision import TV


logger = logging.getLogger(__name__)


@dataclass
class RunState:
    running: bool
    step: bool


def run_kernel(kernel_class):
    cv = Condition()
    run_state = RunState(running=True, step=False)

    def _process_stdin():
        for line_raw in sys.stdin:
            line = line_raw.strip()

            if line == "PAUSE":
                with cv:
                    run_state.running = not run_state.running
                    cv.notify()
            elif line == "STEP":
                with cv:
                    run_state.step = True
                    cv.notify()

    parser = argparse.ArgumentParser()

    if hasattr(kernel_class, "register_args"):
        kernel_class.register_args(parser)

    args = parser.parse_args()

    t = Thread(target=_process_stdin)
    t.start()

    tv = TV()

    kernel = kernel_class(args, tv)

    logger.info("Sim loop")

    sim_time = 0

    for step in range(1000):
        with cv:
            while not run_state.running:
                if run_state.step:
                    run_state.step = False
                    break

                tv.send_state(paused=True)

                f = StringIO()
                kernel.report(f)
                tv.send_report(f.getvalue())

                cv.wait()

        tv.send_state(paused=False)

        time_start = time.time()

        kernel.step(tv)

        time_end = time.time()
        sim_time = time_end - time_start
        tv.send_window_title(f"Kernel: {kernel.name}, step {step}, sim time {sim_time:.1f} sec")
        print(f"Step simulation time: {sim_time:.2f}")
