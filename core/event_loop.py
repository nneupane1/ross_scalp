"""Simple event loop for running engine in session windows."""
import time
from core.engine import Engine
from utils.time_utils import in_session


def main_loop(poll_seconds: int = 5):
    engine = Engine()
    while True:
        if in_session():
            engine.run_cycle()
        time.sleep(poll_seconds)


if __name__ == "__main__":
    main_loop()
