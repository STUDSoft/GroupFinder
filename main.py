from Algorithms.dataset_parser import get_dataset
from Algorithms.staypoint_detector import staypoint_detection
from Algorithms.clustering import hdbscan
from File.serializer import save_dataset, load_dataset
from pathlib import Path

min_pts = 2

dataset_file = "File/data.npy"

if not Path(dataset_file).is_file():
    print("Extracting dataset...")
    userlist = get_dataset()
    print("Dataset extracted.")

    print("Detecting staypoints...")
    sp = staypoint_detection(userlist, 200, 30)
    print("Staypoints detected.")

    print("Saving dataset...")
    save_dataset(sp, dataset_file)
    print("Dataset saved")
else:
    print("Loading dataset...")
    sp = load_dataset(dataset_file)
    print("Dataset loaded.")

print("HDBSCAN going on...")
hdbscan(sp, min_pts, 'haversine')
print("Clusters extracted.")