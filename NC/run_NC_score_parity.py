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
ASIAN = []
BLACK = []
AMINDIAN = []
MULTI = []
OTHER = []
UNDESIGNATED = []
WHITE = []
SCORE_PARITY = []
PRECINCT_ID = []
PRECINCT_ABBRV = []
PPL_COUNT = []
output_file = "burke_county_score_parity.csv"
for prec_i in precincts:
    print("Working on precinct....", prec_i)
    precinct_data = burke_county.query("precinct_id == @prec_i")
    subset_scores = precinct_data['d_to_precinct'].to_numpy()
    subset_items = np.arange(0, precinct_data.shape[0])
    subset_groups = precinct_data['race_id'].to_numpy()
    #May need to recode groups if not all groups are present in the subset
    present_grps = np.unique(subset_groups)
    num_present_grps = len(present_grps)
    recoded_present_groups = np.arange(0,num_present_grps)
    recoded_subset_groups = np.array([np.argwhere(present_grps == item)[0][0] for item in subset_groups.tolist()])

    grp_data, score = fas.score_parity(subset_items, subset_scores, recoded_subset_groups)

    coded_back_grp_data = []
    for grp_i in unique_groups:
        if grp_i in present_grps:
            loc = np.argwhere(present_grps == grp_i)[0][0]
            coded_back_grp_data.append(grp_data[loc])
        else:
            coded_back_grp_data.append(None)
    ASIAN.append(coded_back_grp_data[0])
    BLACK.append(coded_back_grp_data[1])
    AMINDIAN.append(coded_back_grp_data[2])
    MULTI.append(coded_back_grp_data[3])
    OTHER.append(coded_back_grp_data[4])
    UNDESIGNATED.append(coded_back_grp_data[5])
    WHITE.append(coded_back_grp_data[6])
    SCORE_PARITY.append(score)
    PRECINCT_ID.append(prec_i)
    PPL_COUNT.append(len(subset_items))
    PRECINCT_ABBRV.append(precinct_data['precinct_abbrv'].to_list()[0])

    # dictionary of lists
    dict = {'ASIAN': ASIAN, 'BLACK': BLACK,
            'AMINDIAN': AMINDIAN, 'MULTI': MULTI,
            'OTHER': OTHER, 'UNDESIGNATED': UNDESIGNATED,
            'WHITE': WHITE, 'SCORE_PARITY': SCORE_PARITY,
            'PRECINCT_ID': PRECINCT_ID, 'PPL_COUNT':PPL_COUNT,
            'PRECINCT_ABBRV': PRECINCT_ABBRV}

    results = pd.DataFrame(dict)
    print(results)
    results.to_csv(output_file, index=False)


