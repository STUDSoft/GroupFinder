from Algorithms.dataset_parser import get_dataset
from Algorithms.staypoint_detector import staypoint_detection
from Algorithms.clustering import optics, extract_dbscan_clustering
from Classes.entities import Cluster

print("Extracting dataset...")
userlist = get_dataset()
print("Dataset extracted.")
print("Detecting staypoints...")
sp = []
for user in userlist:
    trajectorylist = user.get_trajectorylist()
    for trajectory in trajectorylist:
        sp += staypoint_detection(trajectory.get_pointlist(), 200, 30)

print("Staypoints detected.")

eps = 500
min_pts = 2

print("Optics going on...")
opt = optics(sp, eps, min_pts)
print("Optics has finished running.")

print("Clustering points...")
clusters = extract_dbscan_clustering(opt, eps)
print("Clusters extracted")

for c in clusters:
    if c.get_cluster_id() is Cluster.NOISE:
        print("Noise:")
    else:
        print("Cluster " + str(c.get_cluster_id()))
    for p in c.get_objects():
        print(p)
