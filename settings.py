from datetime import datetime

# Initial parameters to set period of data extraction
start_date = '2018-07-01'
end_date = '2019-06-30'

# Initial parameters to run the script
from_database = False        # Retrieve data from database (True) or from pickle (False)
local_production = True     # Run locally (True) or run production (False)

# Paths
path_data_folder = 'data/'  # Path to local data folder, relative to main script
path_input_folder = 'input/' # Path to local input folder, relative to main script
path_log_folder = 'log/' # Path to local log folder, relative to main script

# Filenames
filename_log = 'logfile ' + datetime.now().strftime("%Y-%m-%d_%H-%M")
datetime_log = datetime.now().strftime("%Y-%m-%d_%H-%M")

file_log = filename_log + datetime_log

# Runs of models
run_baseline = False
run_ridge = False
run_forest = False
run_neural = True

# Set type of authentication for DWH. Values:
# - ActiveDirectoryPassword: For Azure Active Directory username/password authentication to SQL Azure.
# - SqlPassword: For username/password authentication to SQL Server (Azure or otherwise).
if from_database:
    dwh_authn = 'ActiveDirectoryPassword'
else:
    dwh_authn = 'SqlPassword'

files = {'pricing_data': 'pricing.xlsx',
         'prices_data': 'prices.xlsx'}