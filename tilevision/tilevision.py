"""
NOTE: Requires either python -u, or sys.stdout.flush() after every write, to work correctly with websocketd
"""

from dataclasses import dataclass
import json
import sys
from typing import Optional


@dataclass
class Label:
    x: float
    y: float
    text: str
    color: str
    fontsize: float = 1.0


@dataclass
class Path:
    d: str
    linedash: Optional[list] = None
    linewidth: Optional[float] = 1.0
    stroke: Optional[str] = None
    fill: Optional[str] = None


# Note: websocketd can be detected via CGI environment variables, see https://datatracker.ietf.org/doc/html/rfc3875.html#page-2
class TV:
    def send_hello(self, *, w: int, h: int, bg: list[str]):
        assert len(bg) == w * h
        obj = dict(command="HELLO", w=w, h=h, bg=bg)
        sys.stdout.write(json.dumps(obj) + "\n")

    def send_annotations(self, labels: list[Label], paths: list[Path]):
        obj = dict(command="LABELS",
                   labels=[l.__dict__ for l in labels],
                   paths=[l.__dict__ for l in paths])
        sys.stdout.write(json.dumps(obj) + "\n")

    def send_report(self, text: str):
        obj = dict(command="REPORT", text=text)
        sys.stdout.write(json.dumps(obj) + "\n")

    def send_state(self, paused):
        obj = dict(command="STATE", paused=paused)
        sys.stdout.write(json.dumps(obj) + "\n")

    def send_window_title(self, title: str):
        obj = dict(command="SET-TITLE", title=title)
        sys.stdout.write(json.dumps(obj) + "\n")
