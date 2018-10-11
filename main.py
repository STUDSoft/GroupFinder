from dataset_parser import *
from staypoint_detector import staypoint_detection

userlist = get_dataset()
print("Dataset extracted")
sp = []
for user in userlist:
    trajectorylist = user.get_trajectorylist()
    for trajectory in trajectorylist:
        sp += staypoint_detection(trajectory.get_pointlist(), 200, 30)

print("Staypoints detected")
for sp in sp:
    print(sp)
