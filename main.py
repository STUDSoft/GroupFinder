from Algorithms.dataset_parser import get_dataset
from Algorithms.staypoint_detector import staypoint_detection
from Algorithms.clustering import hdbscan_clust
from File.serializer import save, load
from pathlib import Path
from Algorithms.sequence_manager import extract_sequencies, sequence_matching, compute_similarity
from Algorithms.point_utilities import get_number_of_sp_per_user
import Classes.parameters as par

if not Path(par.clusterable_sp_file).is_file() or not Path(par.sp_file).is_file():
    print("Extracting dataset...")
    userlist = get_dataset()
    print("Dataset extracted.")

    print("Detecting staypoints...")
    sp, staypoints = staypoint_detection(userlist, par.dist_threh, par.time_threh)
    print("Staypoints detected.")

    print("Saving staypoints...")
    save(staypoints, par.sp_file)
    print("Staypoints saved.")

    print("Saving clusterable staypoints...")
    save(sp, par.clusterable_sp_file)
    print("Clusterable staypoints saved.")

else:
    print("Loading staypoints...")
    staypoints = load(par.sp_file)
    print("Staypoints, loaded.")

    print("Loading clusterable staypoints...")
    sp = load(par.clusterable_sp_file)
    print("Clusterable staypoints loaded.")

print("HDBSCAN going on...")
clusterer = hdbscan_clust(sp, par.min_pts, par.hdbscan_metric)
print("Clusters extracted.")

labels = clusterer.labels_.tolist()

print("Extracting sequencies...")
seq = extract_sequencies(staypoints, labels)
print("Sequencies extracted.")

num_sp = get_number_of_sp_per_user(staypoints)

print("Calculating similarities...")
sim=[]
#il calcolo tra 147 e 157 è molto lungo 20 min+
k = 0
while k < len(seq) - 1:
    if k is not 4:
        k+=1
        continue
    print("Comparing " + str(k) + " len: " + str(len(seq[k].get_nodes())) + " with:")
    i = 0
    sim_row=[]
    while i < len(seq):
        if i>10:
            break
        print("\t " + str(i) + " len: " + str(len(seq[i].get_nodes())))
        if i is k:
            sim_row+=[1]
        elif num_sp[k] == 0 or num_sp[i] == 0:#if there is no data
            sim_row+=[0]
        else:
            match = sequence_matching(seq[k], seq[i], par.max_length, par.eps)
            sim_row+=[float(compute_similarity(match, num_sp[k], num_sp[i]))]
            
        i += 1
    k += 1
    sim+=[sim_row]
    
print(sim)
