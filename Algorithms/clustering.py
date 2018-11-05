import hdbscan


def hdbscan_clust(data, min_pts, metric):
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_pts, metric=metric, gen_min_span_tree=True)
    clusterer.fit_predict(data)

    return clusterer
