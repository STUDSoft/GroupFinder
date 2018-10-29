from Classes.side import StayPointClust
from Algorithms.point_utilities import haversine_distance
from Classes.queue import PriorityQueue
from Classes.entities import Cluster
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


def set_points_to_unproc(set_of_objects):
    objects_unprocessed = []
    for obj in set_of_objects:
        objects_unprocessed.append(StayPointClust(obj))
    return objects_unprocessed


def optics(set_of_objects, eps, min_pts):
    set_of_objects = set_points_to_unproc(set_of_objects)
    ordered_list = []
    for obj in set_of_objects:
        if not obj.get_processed():
            ordered_list = expand_cluster_order(set_of_objects, obj, eps, min_pts, ordered_list)
    return ordered_list


def expand_cluster_order(set_of_objects, obj, eps, min_pts, ordered_list):
    neighbors = get_neighbors(set_of_objects, obj, eps)
    obj.set_processed(True)
    obj.set_reach_dist(None)
    obj.set_core_dist(core_distance(set_of_objects, obj, eps, min_pts))
    ordered_list.append(obj)
    order_seeds = PriorityQueue()
    if obj.get_core_dist() is not None:
        order_seeds = update(order_seeds, neighbors, obj)
        while not order_seeds.empty():
            current_obj = order_seeds.pop()
            neighbors = get_neighbors(set_of_objects, current_obj, eps)
            current_obj.set_processed(True)
            current_obj.set_core_dist(core_distance(neighbors, current_obj, eps, min_pts))
            ordered_list.append(current_obj)
            if current_obj.get_core_dist() is not None:
                order_seeds = update(order_seeds, neighbors, current_obj)
    return ordered_list


def update(order_seeds, neighbors, center_obj):
    c_dist = center_obj.get_core_dist()
    for o in neighbors:
        if not o.get_processed():
            new_r_dist = max(c_dist, haversine_distance(center_obj, o))
            if o.get_reach_dist() is None:
                o.set_reach_dist(new_r_dist)
                order_seeds.push(o, new_r_dist)
            else:
                if new_r_dist < o.get_reach_dist():
                    o.set_reach_dist(new_r_dist)
                    order_seeds.remove(o)
                    order_seeds.push(o, new_r_dist)
    return order_seeds


def get_neighbors(set_of_objects, obj, eps):
    neighbors = []
    for o in set_of_objects:
        if haversine_distance(o, obj) <= eps:
            neighbors.append(o)
    return neighbors


def core_distance(set_of_objects, obj, eps, min_pts):
    for core_dist in range(eps):
        n = get_neighbors(set_of_objects, obj, core_dist)
        if len(n) >= min_pts:
            return core_dist
    return None


def extract_dbscan_clustering(ordered_objs, eps):
    cluster_id = Cluster.NOISE
    clusters = [Cluster(Cluster.NOISE)]
    for obj in ordered_objs:
        if obj.get_reach_dist() is None or obj.get_reach_dist() > eps:
            if obj.get_core_dist() is not None and obj.get_core_dist() <= eps:
                cluster_id += 1
                curr_clust = Cluster(cluster_id)
                curr_clust.add_object(obj)
                obj.set_cluster_id(cluster_id)
                clusters.append(curr_clust)
            else:
                obj.set_cluster_id(Cluster.NOISE)
                clusters[Cluster.NOISE].add_object(obj)
        else:
            obj.set_cluster_id(cluster_id)
            clusters[cluster_id].add_object(obj)

    return clusters
