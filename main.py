from Algorithms.dataset_parser import get_dataset
from Algorithms.staypoint_detector import staypoint_detection
from Algorithms.clustering import hdbscan_clust
from File.serializer import save, load
from pathlib import Path
from Algorithms.sequence_manager import extract_sequencies, sequence_matching, compute_similarity
from Algorithms.point_utilities import get_number_of_sp_per_user

min_pts = 2

clusterable_sp_file = "File/clusterable_sp.npy"
sp_file = "File/sp.npy"

if not Path(clusterable_sp_file).is_file() or not Path(sp_file).is_file():
    print("Extracting dataset...")
    userlist = get_dataset()
    print("Dataset extracted.")

    print("Detecting staypoints...")
    sp, staypoints = staypoint_detection(userlist, 200, 30)
    print("Staypoints detected.")

    print("Saving staypoints...")
    save(staypoints, sp_file)
    print("Staypoints saved.")

    print("Saving clusterable staypoints...")
    save(sp, clusterable_sp_file)
    print("Clusterable staypoints saved.")

else:
    print("Loading staypoints...")
    staypoints = load(sp_file)
    print("Staypoints, loaded.")

    print("Loading clusterable staypoints...")
    sp = load(clusterable_sp_file)
    print("Clusterable staypoints loaded.")

print("HDBSCAN going on...")
clusterer = hdbscan_clust(sp, min_pts, 'haversine')
print("Clusters extracted.")

labels = clusterer.labels_.tolist()

print("Extracting sequencies...")
seq = extract_sequencies(staypoints, labels)
print("Sequencies extracted.")

num_sp = get_number_of_sp_per_user(staypoints, 182)

print("Calculating similarities...")
sim=[]
#per debugging k=147 (157)
k = 147
while k < len(seq) - 1:
    print("Comparing " + str(k) + " len: " + str(len(seq[k].get_nodes())) + " with:")
    i = 0
    if k is 147:
        i=156
    sim_row=[]
    while i < len(seq):
        print("\t " + str(i) + " len: " + str(len(seq[i].get_nodes())))
        if i is not k:
            match = sequence_matching(seq[k], seq[i], 4, 10)
            sim_row+=[compute_similarity(match, num_sp[k], num_sp[i])]
        else:
            match = set()
            sim_row+=[1]
        i += 1
    k += 1
    sim+=sim_row
    
print(sim)
