# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 17:01:02 2018

@author: Daniele
"""

# the dataset file
# used in dataset_parser
dataset_file = "Geolife Trajectories 1.3.zip"

# the file destination for the clusterable staypoints
clusterable_sp_file = "File/clusterable_sp.npy"

# the file destination for the staypoints
sp_file = "File/sp.npy"

# the distance threshold in meters necessary to consider two points as in the same staypoint
# from main to staypoint_detection
dist_tresh = 200

# the time threshold in minutes necessary to consider two points as in the same staypoint
# from main to staypoint_detection
time_tresh = 30

# the number of minimum points needed to create a cluster
# from main to hdbscan_clust
min_pts = 2

# the metric used in hadbscan_clust
hdbscan_metric = 'haversine'

# the max length of a similar sequence
max_length = 4

# the time constraint, denotes two similar transition times between the same region
eps = 10
