"""Score Metrics
    ----------

"""

# Authors: Anonymous


import numpy as np

def score_parity(subset_items, subset_scores, subset_groups):
    """Compute score parity.
    Parameters
    ----------
    subset_items : numpy array of shape = (n_items)
        The items in the subset(sorted by relevance score).
    subset_scores : numpy array of shape = (n_items)
        The scores of the items in the subset(sorted by relevance score).
    subset_groups: numpy array of shape = (n_items)
        The group identity of the items in the subset (corresponding to order of items in subset_items).
    q: float
        The relevance score for which items in the pool that have score >= q are "relevant".
    Returns
    ----------
    AvgScore: numpy array of shape = (n_groups)
        The average score of a group
    sp_val: float
        fairness.
    Examples
    --------
    --------
    >>> subset_items = np.asarray([2,4])
    >>> subset_scores = np.asarray([85,12])
    >>> subset_groups = np.asarray([0, 1])
    >>> print(score_parity(subset_items, subset_scores, subset_groups))
    array([85., 12.]), 0.1411764705882353
    """

    unique_grps = np.unique(subset_groups)
    num_unique_grps = unique_grps.shape[0]
    AvgScore = np.full((num_unique_grps,), -np.Inf)
    for grp in unique_grps:
        subset_mask = subset_groups == grp
        num_grp_items_in_subset = np.count_nonzero(subset_mask)
        total_grp_score = np.sum(subset_scores[subset_mask])
        AvgScore[grp] = total_grp_score / num_grp_items_in_subset

    min_group_selection_prop = np.min(AvgScore)
    max_group_selection_prop = np.max(AvgScore)
    sp_val = min_group_selection_prop / max_group_selection_prop
    return AvgScore, sp_val


def score_balance(subset_items, subset_scores, subset_groups):
    """Compute score balance.
    Parameters
    ----------
    subset_items : numpy array of shape = (n_items)
        The items in the subset(sorted by relevance score).
    subset_scores : numpy array of shape = (n_items)
        The scores of the items in the subset(sorted by relevance score).
    subset_groups: numpy array of shape = (n_items)
        The group identity of the items in the subset (corresponding to order of items in subset_items).
    q: float
        The relevance score for which items in the pool that have score >= q are "relevant".
    Returns
    ----------
    TotalScore: numpy array of shape = (n_groups)
        The average score of a group
    sp_val: float
        fairness.
    Examples
    --------
    --------
    >>> subset_items = np.asarray([2,4, 3])
    >>> subset_scores = np.asarray([85,12, 54])
    >>> subset_groups = np.asarray([0, 1, 1])
    >>> print(score_balance(subset_items, subset_scores, subset_groups))
array([85., 66.]), 0.7764705882352941
    """

    unique_grps = np.unique(subset_groups)
    num_unique_grps = unique_grps.shape[0]
    TotalScore = np.full((num_unique_grps,), -np.Inf)
    for grp in unique_grps:
        subset_mask = subset_groups == grp
        num_grp_items_in_subset = np.count_nonzero(subset_mask)
        total_grp_score = np.sum(subset_scores[subset_mask])
        TotalScore[grp] = total_grp_score

    min_group_selection_prop = np.min(TotalScore)
    max_group_selection_prop = np.max(TotalScore)
    sb_val = min_group_selection_prop / max_group_selection_prop
    return TotalScore, sb_val


