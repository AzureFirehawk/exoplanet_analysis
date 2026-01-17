"""
Docstring for spinner

Purpose: Module for creating a simple spinner animation.
"""

import time
import sys

def spinner(message="Standby...", duration=3.0, interval=0.2):
  chars = "|/-\\"
  end_time = time.time() + duration
  i = 0

  while time.time() < end_time:
    sys.stdout.write(
      f"\r{message} {chars[i % len(chars)]}"
    )
    sys.stdout.flush()
    time.sleep(interval)
    i += 1

  sys.stdout.write(f"\r{message} done!\n")


