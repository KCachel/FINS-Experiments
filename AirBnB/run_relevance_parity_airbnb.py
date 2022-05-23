import pandas as pd
import numpy as np
import FINS as fas

output_file = "relevance_parity_airbnb.csv"



datasets = ["Bangkok.csv",
            "Berlin.csv",
            "NewZealand.csv"]

location = ["Bangkok",
            "Berlin",
            "NewZealand"]


LOCALITY = []
RELEVANCE_PARITY = []
SINGLE = []
SMALL = []
PROFESSIONAL = []




for i in range(len(datasets)):
    data =pd.read_csv(datasets[i])
    pool_items = np.arange(0, len(data))
    pool_scores = np.array(data.reviews_per_month)
    pool_groups = np.array(data.host)
    num_items = len(pool_items)
    k_val = 50

    subset_items = pool_items[:k_val]
    subset_scores = pool_scores[:k_val]
    subset_groups = pool_groups[:k_val]

    grp_data, score = fas.relevance_parity(pool_items,pool_scores,pool_groups, subset_items, subset_scores, subset_groups)

    LOCALITY.append(location[i])
    RELEVANCE_PARITY.append(score)
    SINGLE.append(grp_data[0])
    SMALL.append(grp_data[1])
    PROFESSIONAL.append(grp_data[2])

    # dictionary of lists
    dict = {'LOCALITY': LOCALITY, 'RELEVANCE_PARITY': RELEVANCE_PARITY,
            'SINGLE': SINGLE,
            'SMALL': SMALL, 'PROFESSIONAL': PROFESSIONAL}

    results = pd.DataFrame(dict)
    print(results)
    results.to_csv(output_file, index=False)
