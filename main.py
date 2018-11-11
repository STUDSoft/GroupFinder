from Algorithms.dataset_parser import get_dataset
from Algorithms.staypoint_detector import staypoint_detection
from Algorithms.clustering import hdbscan_clust
from File.serializer import save, load
from pathlib import Path
from Algorithms.sequence_manager import extract_sequencies, calculate_similarities
from Algorithms.point_utilities import get_number_of_sp_per_user
import Classes.parameters as par

if not Path(par.clusterable_sp_file).is_file() or not Path(par.sp_file).is_file():
    print("Extracting dataset...")
    userlist = get_dataset()
    print("Dataset extracted.")

    print("Detecting staypoints...")
    sp, staypoints = staypoint_detection(userlist, par.dist_tresh, par.time_tresh)
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
sim = calculate_similarities(seq, num_sp, par.max_length, par.eps)
