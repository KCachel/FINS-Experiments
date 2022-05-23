import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import FINS as fas

burke_county = pd.read_csv('geocoded_burke_county_clean.csv', header=0, na_values='?')

np_voter_lat = np.array(burke_county["voter_lat"])
np_voter_long = np.array(burke_county["voter_long"])
voter_geometry = np.vstack((np_voter_lat, np_voter_long)).transpose()

np_precint_lat = np.array(burke_county["precinct_lat"])
np_precint_long = np.array(burke_county["precinct_long"])
precinct_geometry = np.vstack((np_precint_lat, np_precint_long)).transpose()
distance = np.full_like(np_precint_lat, np.Inf)
for i in range(0, len(precinct_geometry)):
    distance[i] = np.linalg.norm(precinct_geometry[i] - voter_geometry[i])


burke_county['d_to_precinct'] = distance

precincts = np.unique(burke_county['precinct_id']).tolist()

unique_groups = np.unique(burke_county['race_id'].to_numpy())
DEMOCRAT = []
REPUBLICAN = []
PARITY = []
PRECINCT_ID = []
PRECINCT_ABBRV = []
PPL_COUNT = []
output_file = "burke_county_party_parity.csv"
dems_reps = [0,2]
burke_county_dems_rs = burke_county.query("party_cd == @dems_reps")
pool_items = np.arange(0,burke_county_dems_rs.shape[0])
pool_groups = burke_county_dems_rs['party_cd'].to_numpy()
for prec_i in precincts:
    print("Working on precinct....", prec_i)
    precinct_data = burke_county.query("precinct_id == @prec_i")
    precinct_data = precinct_data.query("party_cd == @dems_reps")
    subset_scores = precinct_data['d_to_precinct'].to_numpy()
    subset_items = np.arange(0, precinct_data.shape[0])
    subset_groups = precinct_data['party_cd'].to_numpy()
    #May need to recode groups if not all groups are present in the subset
    present_grps = np.unique(subset_groups)
    num_present_grps = len(present_grps)
    recoded_present_groups = np.arange(0,num_present_grps)
    recoded_subset_groups = np.array([np.argwhere(present_grps == item)[0][0] for item in subset_groups.tolist()])
    recoded_pool_groups = np.array([np.argwhere(present_grps == item)[0][0] for item in pool_groups.tolist()])

    grp_data, score = fas.parity(pool_items, recoded_pool_groups, subset_items, recoded_subset_groups)

    # coded_back_grp_data = []
    # for grp_i in unique_groups:
    #     if grp_i in present_grps:
    #         loc = np.argwhere(present_grps == grp_i)[0][0]
    #         coded_back_grp_data.append(grp_data[loc])
    #     else:
    #         coded_back_grp_data.append(None)
    DEMOCRAT.append(grp_data[0])
    REPUBLICAN.append(grp_data[1])
    PARITY.append(score)
    PRECINCT_ID.append(prec_i)
    PPL_COUNT.append(len(subset_items))
    PRECINCT_ABBRV.append(precinct_data['precinct_abbrv'].to_list()[0])

    # dictionary of lists
    dict = {'DEMOCRAT': DEMOCRAT, 'REPUBLICAN': REPUBLICAN,
            'PARITY': PARITY,
            'PRECINCT_ID': PRECINCT_ID, 'PPL_COUNT':PPL_COUNT,
            'PRECINCT_ABBRV': PRECINCT_ABBRV}

    results = pd.DataFrame(dict)
    print(results)
    results.to_csv(output_file, index=False)


