import importlib.resources
import subprocess
import sys

import tilevision


def main():
    assert sys.executable  # in principle, it could be None or empty

    with importlib.resources.path(tilevision, "static") as static_path:
        rc = subprocess.call(["websocketd",
                              "--address=localhost",
                              # it might be OK to just inherit everything, I guess the point is to prevent accidental leaks of sensitive environment to clients?
                              # more discussion: https://github.com/joewalnes/websocketd/issues/4
                              "--passenv=PATH,DYLD_LIBRARY_PATH,PYTHONPATH",
                              "--port=4000",
                              f"--staticdir={static_path}",
                              sys.executable] + sys.argv[1:])
    sys.exit(rc)


if __name__ == "__main__":
    main()
