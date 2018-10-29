import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
import hdbscan as hdbscn


def plot_clusters(data, algorithm, args, kwds):
    start_time = time.time()
    labels = algorithm(*args, **kwds).fit_predict(data)
    end_time = time.time()
    palette = sns.color_palette('deep', np.unique(labels).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
    plot_kwds = {'alpha': 0.25, 's': 80, 'linewidths': 0}
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    plt.title('Clusters found by {}'.format(str(algorithm.__name__)), fontsize=24)
    plt.text(-0.5, 0.7, 'Clustering took {:.2f} s'.format(end_time - start_time), fontsize=14)
    plt.show()


def hdbscan(data, min_pts, metric):
    plot_clusters(data, hdbscn.HDBSCAN, (), {'min_cluster_size': min_pts, 'metric': metric})
