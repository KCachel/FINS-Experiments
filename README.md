# FINS-Experiments
Code and datasets for our paper FINS Auditing Framework: Group Fairness in Subset Selection. For the actual FINS framework see the [fins repository](https://github.com/KCachel/fins).


FINS:

All FINS toolkit code is available in the "FINS" directory. "[metric style].py" contains corresponding functions for each FINS measure and "utils_error_handling.py" contains helper functions to perform error handling.

EXPERIMENTS:


AirBnB case study

All datasets, code and results are available in the "AirBnB_Case" directory. 'cityname'Raw.csv contains the raw data downloaded from http://insideairbnb.com/get-the-data.html. 'cityname'.csv contains the cleaned locality dataset used for analysis (hosts given ids, and sorted by decreasing reviews per month). The scripts "run_qualified_balance_airbnb.py", "run_qualified_parity_airbnb.py", and "run_relevance_parity_airbnb.py" contain the driver code to audit the selected subsets and results are in correspondingly titled csv files. 


NC Burke County. 

All datasets, code and results in the "NC" directory. "precinct_data_cleaning.R" contains code to geocode precinct addresses from "precinct_info.xlsx" accessed from https://www.burkenc.org/DocumentCenter/View/880/Polling-Place-Master-List-PDF. Then "clean_nc_data.R" performed geocoding of voter addresses and saves to csvs labelled "geocoded_burke_county[#]/csv", it geocodes the addresses of voters from  "ncvoter12.txt" downloaded from https://www.ncsbe.gov/results-data/voter-registration-data. Finally, "generate_geocoded_party_data.R" generate the final dataset "geocoded_burke_county_clean.csv". "run_NC_balance.py", "run_NC_score_parity.py", and "run_NC_statp.py" contains the driver code for auditing the precincts with FINS. The csvs "burke_county_balance.csv", "burke_county_score_parity.csv", and "burke_county_party_parity.csv" contain the results.


standard python libraries needed for FINS:

numpy

pandas

standard python libraries needed for experiments:

numpy

pandas
