import pandas as pd
import numpy as np
import FINS as fas

output_file = "qualified_parity_airbnb.csv"



datasets = ["Bangkok.csv",
            "Berlin.csv",
            "NewZealand.csv"]

location = ["Bangkok",
            "Berlin",
            "NewZealand"]
qs = [.59, .81, 1.77]

LOCALITY = []
QUALIFIED_PARITY = []
SINGLE = []
SMALL = []
PROFESSIONAL = []




for i in range(len(datasets)):
    data =pd.read_csv(datasets[i])
    pool_items = np.arange(0, len(data))
    pool_scores = np.array(data.reviews_per_month)
    pool_groups = np.array(data.host)
    num_items = len(pool_items)
    q_val = qs[i]
    k_val = 50

    subset_items = pool_items[:k_val]
    subset_scores = pool_scores[:k_val]
    subset_groups = pool_groups[:k_val]

    grp_data, score = fas.qualififed_parity(pool_items, pool_scores,pool_groups, subset_items, subset_scores, subset_groups, q_val)

    LOCALITY.append(location[i])
    QUALIFIED_PARITY.append(score)
    SINGLE.append(grp_data[0])
    SMALL.append(grp_data[1])
    PROFESSIONAL.append(grp_data[2])

    # dictionary of lists
    dict = {'LOCALITY': LOCALITY, 'QUALIFIED_PARITY': QUALIFIED_PARITY,
            'SINGLE': SINGLE,
            'SMALL': SMALL, 'PROFESSIONAL': PROFESSIONAL}

    results = pd.DataFrame(dict)
    print(results)
    results.to_csv(output_file, index=False)
