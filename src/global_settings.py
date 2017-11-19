"""
Top-Level project file that holds config variables
"""
import os


# ======================#
# FILE PATHS            #
# ======================#

# File path of the source code
SRC_DIR = os.path.abspath(__file__)

# Path of the base project folder
BASE_DIR = os.path.abspath(os.path.join(SRC_DIR, '..'))

# Path for data
DATA_DIR = os.path.abspath(os.path.join(SRC_DIR, '..', 'data'))


# ======================#
# DATA RELATED VARS     #
# ======================#

# Currently Valid Report Years(last update: 11-13-2017)
VALID_REPORT_YEARS = range(1977, 2017)
