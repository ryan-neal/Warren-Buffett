"""
Top-Level project file that holds config variables
"""
import os

# File path of the source code
SRC_DIR = os.path.abspath(__file__)

# Path of the base project folder
BASE_DIR = os.path.abspath(os.path.join(SRC_DIR, '..'))

# Path for data
DATA_DIR = os.path.abspath(os.path.join(SRC_DIR, '..', 'data'))
