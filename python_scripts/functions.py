import pandas as pd
import numpy as np
import os
import sys

################################################################################
############################# Path Directories #################################


def ensure_directory(path):
    """Ensure that the directory exists. If not, create it."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory exists: {path}")

